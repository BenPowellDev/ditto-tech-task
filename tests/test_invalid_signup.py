import pytest
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.test_data import generate_valid_password, generate_user_data


@pytest.mark.invalid_signup
class TestInvalidSignup:
    def test_signup_with_invalid_email_format(self, page, base_url):
        # Arrange
        login_page = LoginPage(page)
        signup_page = SignupPage(page)
        invalid_email = "not-a-valid-email" 
        
        # Navigate to signup page via login page - more realistic flow
        login_page.navigate(base_url)
        login_page.click_sign_up_tab()
        
        signup_page.fill_signup_form(
            email=invalid_email,
            password=generate_valid_password(),
            accept_promo=True,
            accept_terms=True
        )

        # Try to submit the form
        signup_page.submit_form()
        
        # Wait for validation to occur
        page.wait_for_timeout(2000)
        
        # User should see error message
        assert signup_page.has_error(error_type='email')
        
        # User should not be authenticated
        signup_page.assert_no_authentication()
    
    def test_signup_without_accepting_terms(self, page, base_url):
        # Arrange
        login_page = LoginPage(page)
        signup_page = SignupPage(page)
        user_data = generate_user_data()
        
        # Navigate to signup page via login page - more realistic flow
        login_page.navigate(base_url)
        login_page.click_sign_up_tab()
        
        signup_page.fill_signup_form(
            email=user_data["email"],
            password=user_data["password"],
            accept_promo=False,
            accept_terms=False  # Don't accept terms
        )
        
        # Try to submit the form
        signup_page.submit_form()
        
        # Wait for validation to occur
        page.wait_for_timeout(2000)
        
        # User should see error message
        assert signup_page.has_error(error_type='terms')
        
        # User should remain on signup page
        signup_page.assert_no_authentication()
