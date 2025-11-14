from playwright.sync_api import Page, expect
from typing import Literal


class SignupPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Locators for signup form elements
        self.login_tab = page.locator("a:has-text('Log in'), a:has-text('Login')")
        
        # Form inputs (placeholders visible in screenshots)
        self.email_input = page.locator('input[placeholder="Email Address"], input[type="email"]')
        self.password_input = page.locator('input[placeholder="Password"], input[type="password"]')
        
        # Checkboxes - filter by visible checkboxes only (excludes cookie banner checkboxes)
        visible_checkboxes = 'input[type="checkbox"]:visible'
        self.promo_checkbox = page.locator(visible_checkboxes).nth(0)
        self.terms_checkbox = page.locator(visible_checkboxes).nth(1)
        
        # Buttons
        self.sign_up_button = page.locator('button:has-text("Sign up"), button:has-text("SIGN UP")')
        
        # Google sign in button
        self.google_signin_button = page.locator('text=Continue with Google')
        
        # Error message locators - the red text below input fields
        self.error_message = page.locator('.text-danger, [class*="text-danger"]')
        self.email_error = page.locator('text="Please specify a valid email address"')
        self.terms_error = page.locator('text="You must agree to our Terms and Conditions in order to proceed"')
        
        # Success indicators
        self.success_message = page.locator('.success, .success-message, [class*="success"]')
        self.verification_notice = page.locator('text=/verify|verification|check your email/i')
        self.captcha = page.locator('iframe[src*="recaptcha/api2/bframe"]')
        
    def navigate(self, base_url: str):
        """Navigate to the signup page from base URL."""
        signup_url = f"{base_url.rstrip('/')}/signup"
        self.page.goto(signup_url, wait_until="domcontentloaded")
            
    def fill_signup_form(
        self, 
        email: str, 
        password: str, 
        accept_promo: bool = True,
        accept_terms: bool = True
    ):
        """Fill out the signup form with provided details."""
            
        # Wait for form to be visible and interactable
        self.email_input.wait_for(state="visible", timeout=10000)
        
        # Clear and fill email with explicit focus
        self.email_input.click() 
        self.email_input.clear()
        self.email_input.fill(email)
        
        # Clear and fill password
        self.password_input.click() 
        self.password_input.clear()
        self.password_input.fill(password)
        
        # Handle checkboxes - check the input elements
        if accept_promo:
            try:
                self.promo_checkbox.wait_for(state="attached", timeout=5000)
                self.promo_checkbox.check(force=True)
            except Exception as e:
                print(f"Warning: Could not check promo checkbox: {e}")
        
        if accept_terms:
            try:
                self.terms_checkbox.wait_for(state="attached", timeout=5000)
                self.terms_checkbox.check(force=True)
            except Exception as e:
                print(f"Warning: Could not check terms checkbox: {e}")
                
    def submit_form(self):
        self.sign_up_button.first.click()
        self.page.wait_for_load_state("networkidle")
        
    def click_login_tab(self):
        self.login_tab.wait_for(state="visible", timeout=5000)
        self.login_tab.click()
    
        self.email_input.wait_for(state="visible", timeout=5000)
            
    def has_error(self, error_type: str = None) -> bool:

        # Map error types to their locators
        error_locators = {
            'email': (self.email_error, 3000),
            'terms': (self.terms_error, 3000),
        }
        
        error_text = ""
        error_found = False
        
        # Check specific error type or all if none specified
        types_to_check = [error_type] if error_type else error_locators.keys()
        
        for etype in types_to_check:
            locator, timeout = error_locators[etype]
            try:
                if locator.is_visible(timeout=timeout):
                    error_text = locator.text_content()
                    if not error_type:  # Only print when checking all types
                        print(f"{etype.capitalize()} error found: {error_text}")
                    error_found = True
                    break
            except:
                continue
        
        return error_found
        
    def has_captcha(self) -> bool:
        """Check if captcha is present on the page."""
        try:
            return self.captcha.first.is_visible(timeout=5000)
        except:
            return False
        
    def has_success_indicator(self) -> bool:
        """Check if any success indicator is present."""
        # Check for URL change (redirect)
        current_url = self.page.url
        if any(keyword in current_url for keyword in ["dashboard", "welcome", "verify", "subscriptions"]):
            return True
            
        # Check for success message
        if self.success_message.is_visible(timeout=3000):
            return True
            
        # Check for verification notice
        if self.verification_notice.is_visible(timeout=3000):
            return True
            
        return False
        
    def assert_no_authentication(self):
        # Should still be on login/signup page
        current_url = self.page.url
        assert any(keyword in current_url.lower() for keyword in ["login", "signup"])
        
        # Should not be redirected to authenticated pages
        assert "dashboard" not in current_url.lower()
        assert "account" not in current_url.lower()
