import pytest 
from core.security import hash_password, verify_password, create_new_access_token
def test_password_hashing_and_verification():
    "Test that password hashing and verification works correcltly."
    plain_password = "my_secret_password"
    hashed = hash_password(plain_password)

    assert hashed != plain_password
    
def test_verify_password():
    "Test that password verification returns True for correct password and False for incorrect password."
    plain_password = "my_secret_password"
    hashed_password = hash_password(plain_password)

    is_valid = verify_password(plain_password, hashed_password)
    assert is_valid == True

def test_create_new_access_token():
    user_id = 123
    token = create_new_access_token(data={"sub": user_id})

    assert isinstance(token, str)
    assert len(token) > 20
