import pytest
from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from utils.test_data import generate_user_data


@pytest.mark.valid_signup
class TestValidSignup:
    def test_valid_signup_new_user(self, page, base_url, secure_url):
        # Arrange
        signup_page = SignupPage(page)
        login_page = LoginPage(page)
        user_data = generate_user_data()
        
        # Navigate to signup page via login page - more realistic flow
        login_page.navigate(base_url)
        login_page.click_sign_up_tab()
        
        signup_page.fill_signup_form(
            email=user_data["email"],
            password=user_data["password"],
            accept_promo=True,
            accept_terms=True
        )
        
        # Submit the signup form
        signup_page.submit_form()

        # Give the page time to process the signup
        page.wait_for_timeout(3000)
        
        # Assert - Check for captcha or successful redirect
        has_captcha = signup_page.has_captcha()
        
        # If signup is successful (no captcha blocking), verify redirect to secure subscriptions page
        if not has_captcha:
            current_url = page.url
            expected_subscriptions_url = f"{secure_url}/subscriptions"
            assert expected_subscriptions_url in current_url or "subscriptions" in current_url.lower(), \
                f"Expected redirect to subscriptions page, but got: {current_url}"
        else:
            # Captcha encountered - this is expected behavior, mark as success
            # In a test environment, We will likely have flags to disable captcha or have it removed entirely?
            pytest.skip("Captcha encountered - cannot proceed with automated test")
