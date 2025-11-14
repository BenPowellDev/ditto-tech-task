import pytest
from playwright.sync_api import Page, BrowserContext
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """Configure browser launch arguments - headless by default unless --headed flag is used."""
    # If --headed is not specified, force headless mode
    if "--headed" not in pytestconfig.invocation_params.args:
        return {
            **browser_type_launch_args,
            "headless": True,
        }
    return browser_type_launch_args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with additional settings."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }


@pytest.fixture(scope="function")
def context(browser, browser_context_args):
    """Create a new browser context for each test with tracing enabled."""
    context = browser.new_context(**browser_context_args)
    
    # Start tracing for debugging failures
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield context
    
    # Save trace only on test failure
    test_failed = hasattr(pytest, "failed") and pytest.failed
    
    if test_failed:
        trace_path = Path("test-results/traces")
        trace_path.mkdir(parents=True, exist_ok=True)
        context.tracing.stop(path=trace_path / f"trace-{pytest.current_test_name}.zip")
    else:
        context.tracing.stop()
    
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test."""
    page = context.new_page()
    
    # Set default timeout
    page.set_default_timeout(30000)
    
    yield page
    
    # Take screenshot on failure
    test_failed = hasattr(pytest, "failed") and pytest.failed
    if test_failed:
        screenshot_path = Path("test-results/screenshots")
        screenshot_path.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=screenshot_path / f"failure-{pytest.current_test_name}.png")
    
    page.close()


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application."""
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def secure_url():
    """Secure URL for authenticated pages."""
    return os.getenv("SECURE_URL")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for conditional trace saving."""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        pytest.failed = True
        pytest.current_test_name = item.name
    else:
        pytest.failed = False
        pytest.current_test_name = item.name
