from auth.utils import hash_password, verify_password
import pytest


@pytest.fixture
def hashed_password():
    return hash_password("secret123")


def test_verify_password_accepts_correct_password(hashed_password):
    assert verify_password("secret123", hashed_password) is True


def test_verify_password_rejects_wrong_password(hashed_password):
    assert verify_password("wrong-pass", hashed_password) is False


def test_verify_password_rejects_empty_string(hashed_password):
    assert verify_password("", hashed_password) is False
