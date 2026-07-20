import pytest
from utils.validators import (
    validate_registration,
    validate_login,
    allowed_file,
    validate_transaction_columns,
    safe_filename,
)


def test_validate_registration_accepts_valid_input():
    errors = validate_registration("shridhar", "shridhar@example.com", "Passw0rd")
    assert errors == []


@pytest.mark.parametrize(
    "username,email,password",
    [
        ("ab", "a@b.com", "Passw0rd"),          # username too short
        ("shridhar", "not-an-email", "Passw0rd"),  # bad email
        ("shridhar", "a@b.com", "short1A"[:5]),    # password too short
        ("shridhar", "a@b.com", "alllowercase1"),  # no uppercase
        ("shridhar", "a@b.com", "NoDigitsHere"),   # no digit
    ],
)
def test_validate_registration_rejects_invalid_input(username, email, password):
    errors = validate_registration(username, email, password)
    assert len(errors) > 0


def test_validate_login_requires_email_and_password():
    assert validate_login("", "") != []
    assert validate_login("a@b.com", "somepassword") == []


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("statement.csv", True),
        ("statement.xlsx", True),
        ("statement.xls", True),
        ("statement.pdf", False),
        ("statement", False),
        ("malicious.exe", False),
    ],
)
def test_allowed_file(filename, expected):
    assert allowed_file(filename) is expected


def test_validate_transaction_columns_passes_with_required_columns():
    assert validate_transaction_columns(["date", "amount", "category"]) == []
    # Case-insensitive / extra whitespace tolerated
    assert validate_transaction_columns([" Date ", "Amount", "CATEGORY"]) == []


def test_validate_transaction_columns_flags_missing_columns():
    errors = validate_transaction_columns(["date", "amount"])
    assert errors and "category" in errors[0]


def test_safe_filename_strips_path_traversal():
    assert safe_filename("../../etc/passwd") == "passwd"
    assert safe_filename("my statement (1).csv") == "my_statement__1_.csv"
