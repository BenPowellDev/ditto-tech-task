import time
from faker import Faker

fake = Faker()

def generate_unique_email() -> str:
    timestamp = int(time.time() * 1000)
    return f"test.user.{timestamp}@dittotest.com"


def generate_valid_password() -> str:
    return "TestPassword123!"


def generate_weak_password() -> str:
    return "123"


def generate_user_data() -> dict:
    return {
        "email": generate_unique_email(),
        "password": generate_valid_password(),
    }
