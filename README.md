# Ditto Music - Signup Flow Automation Task

Automated testing for the Ditto Music signup flow using Playwright + Python + Pytest.

## Video of tests in action

[![Screenshot](https://img.youtube.com/vi/KRud1bawnBo/0.jpg)](https://youtu.be/KRud1bawnBo)

## Quick Start

```powershell
# 1. Clone the repository
git clone <repository-url>
cd ditto-tech-task

# 2. Set up virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install

# 5. Run tests (headless by default)
pytest -q

# 6. Run tests in headed mode (see browser)
pytest --headed
```

**Note**: The `.env` file with configuration is included in the repository for visibility.

## Test Coverage

### Valid Signup Test (`test_valid_signup.py`)
- Creates a new account with a unique email and password
- Navigates through realistic user flow (login page → sign up tab)
- Fills all required fields with valid data
- Accepts terms and conditions checkbox
- Verifies successful signup by checking:
  - Redirect to `{secure_url}/subscriptions` page
  - OR captcha appearance (indicates form was accepted)
- **Result**: Test passes on successful redirect, skips on captcha

### Invalid Signup Tests (`test_invalid_signup.py`)

#### Test 1: Invalid Email Format
- Tests with email missing @ and domain (e.g., "not-a-valid-email")
- Verifies error message appears with email-related keywords
- Most valuable because:
  - Email validation is critical for user authentication
  - Common user error scenario
  - Tests client-side validation implementation

#### Test 2: Terms Not Accepted
- Submits form without accepting terms and conditions
- Verifies error message appears with terms-related keywords
- Important because:
  - Legal requirement for service terms
  - Tests required field validation

## Approach & Design Decisions

### 1. **Page Object Model (POM) - Separated by Responsibility**
   - `pages/signup_page.py` - Signup-specific elements and actions
   - `pages/login_page.py` - Login-specific elements and actions
   - Single Responsibility Principle for better maintainability
   - Improves code reusability and makes tests more readable

### 2. **Smart Error Detection**
   - `has_error(error_type, expected_keywords)` method with:
     - Optional error type filtering ('email', 'terms')
     - Keyword validation for error message content
     - Dictionary-based error locator mapping (cleaner than a huge if/elif chain)
   - Consolidated validation logic in page objects

### 3. **Test Data Generation**
   - Uses Faker library for realistic test data
   - Timestamp-based unique emails to avoid conflicts
   - Password generation with complexity requirements
   - Centralized in `utils/test_data.py` for consistency

### 4. **Automatic Failure Debugging**
   - **Headless by default** for speed and CI/CD compatibility
   - **Screenshots captured on failure** via conftest.py fixture
   - **Traces with snapshots enabled** via conftest.py fixture
   - **Manual screenshots** at key test moments (before/after submit)
   - All artifacts saved to `test-results/` directory
   - Traces only saved on failure

### 5. **Environment Configuration**
   - `.env` file for environment-specific settings
   - `BASE_URL` for public pages (https://dittomusic.com/en)
   - `SECURE_URL` for authenticated pages (https://dashboard.dittomusic.com)

### 6. **CI/CD Integration**
   - **Two separate workflows**:
     - `signupTestsLocal.yml` - Matrix testing (3 OS × 3 browsers)
     - `signupTestsBrowserstack.yml` - Cloud testing integration
   - Artifact upload for test results with 30-day retention
   - Python 3.11 with pip caching for faster builds

## Configuration

### Run Options

```powershell
# Run in headless mode (default)
pytest -q

# Run in headed mode (see browser)
pytest --headed

# Run specific browser
pytest --browser firefox
pytest --browser webkit

# Run specific test file
pytest tests/test_valid_signup.py
pytest tests/test_invalid_signup.py

# Run specific test
pytest tests/test_valid_signup.py::TestValidSignup::test_valid_signup_new_user

# Run with markers
pytest -m valid_signup
pytest -m invalid_signup

# Verbose output
pytest -v
```

## Project Structure

```
ditto-tech-task/
├── .github/
│   └── workflows/
│       └── PROD-Signup-Tests.yml       # GitHub Actions CI/CD
├── pages/
│   ├── __init__.py
│   ├── signup_page.py                  # Signup Page Object
│   └── login_page.py                   # Login Page Object
├── tests/
│   ├── __init__.py
│   ├── test_valid_signup.py            # Valid signup test
│   └── test_invalid_signup.py          # Invalid signup tests
├── utils/
│   ├── __init__.py
│   └── test_data.py                    # Test data generators
├── scripts/
│   └── run_browserstack.py             # BrowserStack integration (optional)
├── test-results/                       # Generated test artifacts
│   ├── screenshots/                    # Screenshots
│   └── traces/                         # Playwright traces
├── conftest.py                         # Pytest fixtures & hooks
├── pytest.ini                          # Pytest configuration
├── requirements.txt                    # Python dependencies
├── .env                                # Environment variables (included in repo)
├── .gitignore
└── README.md
```

## Environment Configuration

The `.env` file contains environment-specific configuration:

```dotenv
BASE_URL=https://dittomusic.com/en
SECURE_URL=https://dashboard.dittomusic.com
```

**Note**: The `.env` file is included in the repository for convenience. In a production scenario, I/We would typically:
- Keep `.env` in `.gitignore`
- Store sensitive values in GitHub Secrets or CI/CD environment variables

## Assumptions

1. **Email uniqueness**: Each test run generates a unique email using timestamps
2. **Captcha handling**: 
   - Reaching captcha means the form was accepted (success indicator)
   - Tests skip when captcha blocks further automation
   - In production, testing environment typically has captcha disabled
3. **Checkbox locators**: Uses `:visible` selector to filter form checkboxes from cookie banner checkboxes
4. **Locator strategy**: 
   - Flexible selectors (placeholder, type, has-text) to handle minor DOM changes
   - Visible checkboxes filtered using nth() after excluding hidden elements
5. **Timeouts**: 
   - Default 30s timeout for most operations
   - 3s timeout for error message checks
   - Configurable in conftest.py
6. **Test isolation**: Each test runs in a fresh browser context with clean state
7. **Error detection**: 
   - Multiple locator strategies (specific error text, .text-danger class)
   - Type-based error checking (email, terms)
   - Keyword validation in error messages
8. **Successful signup**: Redirects to `{secure_url}/subscriptions` page

## Trade-offs

1. **Locator Flexibility vs. Precision**
   - ✅ More resilient to minor HTML changes
   - ✅ Uses specific error text for validation
   - ❌ May need updates if error messages change
   - Solution: Multiple fallback locator strategies

2. **Screenshot Strategy**
   - ✅ Manual screenshots at key moments (before/after submit) for debugging
   - ✅ Automatic screenshots on failure via conftest.py
   - ❌ Increases test execution time slightly (~300ms per screenshot)
   - Rationale: Essential for debugging visual issues

3. **Invalid Test Coverage**
   - ✅ Focused on most valuable invalid cases (email format, terms acceptance)
   - ❌ Other scenarios not covered (weak password, duplicate email, field limits)
   - Rationale: These two cases cover critical validation and legal requirements

4. **Headless Default**
   - ✅ Faster execution (~5-6s vs 12-15s per test)
   - ✅ Suitable for CI/CD pipelines
   - ❌ Harder to debug during development
   - Solution: Easy toggle with `--headed` flag

5. **Page Object Separation**
   - ✅ Single Responsibility Principle (separate login/signup page objects)
   - ✅ Better maintainability and test readability
   - ❌ More initial setup and files to manage
   - Rationale: Worth it for future scalability and team collaboration

6. **Trace Collection**
   - ✅ Full traces with screenshots, snapshots, and sources
   - ✅ Only saved on failure to reduce disk usage
   - ❌ Slight performance overhead during test execution
   - Rationale: Critical for debugging complex failures

7. **Error Method Design**
   - ✅ Dictionary-based locator mapping (cleaner than if/elif chains)
   - ✅ Optional error type and keyword validation
   - ✅ Extensible for new error types
   - ❌ Requires maintenance if error structure changes significantly
   - Rationale: Balance between flexibility and maintainability

## Future Enhancements

If given more time, I would add:

1. **Additional Invalid Test Cases**
   - Duplicate email (already registered user)
   - Weak password validation (too short, no special chars)
   - Missing required fields (test each field individually)
   - Password field character limits
   - Email field with spaces or special characters
   - Terms checkbox already checked by default (edge case)

2. **Complete User Journey Tests**
   - Full signup → email verification → login flow
   - Password reset/forgot password flow
   - Social login integration (Google OAuth)
   - Account deletion/deactivation

3. **API Testing Layer**
   - Verify backend validation matches frontend rules
   - Test rate limiting and abuse protection
   - Direct API signup validation
   - Token generation and validation

4. **Enhanced Reporting**
   - Allure reporting for better visualization
   - Custom HTML reports with screenshots embedded
   - Performance metrics (page load, network timing)
   - Test trend analysis over time

5. **Data-Driven Testing**
   - Parameterized tests with CSV/JSON datasets
   - Boundary value testing for password length
   - International character support (UTF-8, emoji)
   - Multiple invalid email formats in one parameterized test

6. **Visual Regression Testing**
   - Screenshot comparison for UI consistency
   - Responsive design validation (mobile, tablet, desktop viewports)
   - Cross-browser visual parity checks

7. **Accessibility Testing**
   - ARIA label validation for screen readers
   - Keyboard navigation testing (tab order, enter to submit)
   - Color contrast ratio checks
   - Focus indicator visibility

8. **Performance Testing**
   - Page load time assertions
   - Network request monitoring
   - Bundle size tracking
   - Core Web Vitals metrics

9. **Security Testing**
   - HTTPS enforcement verification
   - Password masking in inputs
   - CSRF token validation
   - XSS/SQL injection attempt handling

10. **BrowserStack Enhancements**
    - Complete cloud execution setup
    - Local testing tunnel configuration
    - Mobile browser testing (iOS Safari, Android Chrome)
    - Parallel execution across 5+ browsers simultaneously

## Notes

- Tests are idempotent and can run multiple times safely
- Each test run uses a unique email (timestamp-based) to avoid conflicts
- Tests skip (not fail) when captcha blocks automation
- All test artifacts (screenshots, traces) are gitignored but preserved locally
- Traces only saved on failure to conserve disk space
- Environment variables loaded from `.env` file via python-dotenv
