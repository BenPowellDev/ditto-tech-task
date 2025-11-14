"""Page Object Model for Ditto Music login page."""
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Tab navigation
        self.sign_up_tab = page.locator("a:has-text('Join now'), a:has-text('Join Now')")
        
        # Form inputs
        self.email_input = page.locator('input[placeholder="Email Address"], input[type="email"]')
        self.password_input = page.locator('input[placeholder="Password"], input[type="password"]')
        
        # Buttons
        self.continue_button = page.locator('button:has-text("Continue"), button:has-text("CONTINUE")')
        self.forgot_password_link = page.locator('text=Forgot your password?, a:has-text("Forgot")')
        
        # Google sign in button
        self.google_signin_button = page.locator('text=Continue with Google')
        
        # Error message locators
        self.error_message = page.locator('.text-danger, [class*="text-danger"]')
        self.email_error = page.locator('text="Please specify a valid email address"')
        self.field_error = page.locator('.text-danger, .invalid-feedback, [class*="error"]')
        
        # Success indicators
        self.success_message = page.locator('.success, .success-message, [class*="success"]')
        self.captcha = page.locator('iframe[src*="captcha"], [class*="captcha"], #captcha')
        
    def navigate(self, base_url: str):
        login_url = f"{base_url.rstrip('/')}/login"
        self.page.goto(login_url, wait_until="domcontentloaded")

    def click_sign_up_tab(self):
        self.sign_up_tab.wait_for(state="visible", timeout=5000)
        self.sign_up_tab.click()
        self.page.wait_for_load_state("networkidle")
        
    def fill_login_form(self, email: str, password: str):
        # Wait for form to be visible
        self.email_input.wait_for(state="visible", timeout=10000)
        
        # Clear and fill email
        self.email_input.clear()
        self.email_input.fill(email)
        
        # Clear and fill password
        self.password_input.clear()
        self.password_input.fill(password)
        
    def submit_login_form(self):
        self.continue_button.first.click()
        self.page.wait_for_load_state("networkidle")
        
    def login(self, email: str, password: str):
        self.fill_login_form(email, password)
        self.submit_login_form()
        
    def has_success_indicator(self) -> bool:
        # Check for URL change (redirect to dashboard)
        current_url = self.page.url
        if "dashboard" in current_url or "welcome" in current_url or "account" in current_url:
            return True
            
        # Check for success message
        if self.success_message.is_visible(timeout=3000):
            return True
            
        return False
        
    def is_authenticated(self) -> bool:
        current_url = self.page.url
        # If we're not on login/signup page, we're likely authenticated
        is_on_auth_page = any(keyword in current_url.lower() for keyword in ["login", "signup", "sign-up"])
        return not is_on_auth_page
        
    def assert_no_authentication(self):
        # Should still be on login/signup page
        current_url = self.page.url
        assert any(keyword in current_url.lower() for keyword in ["login", "signup", "sign-up"]), \
            f"Expected to be on login page but got: {current_url}"
        
        # Should not be redirected to authenticated pages
        assert "dashboard" not in current_url.lower(), "Should not be on dashboard"
        assert "account" not in current_url.lower(), "Should not be on account page"
