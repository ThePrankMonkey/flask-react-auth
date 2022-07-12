# services/users/src/tests/test_user_model.py
from src.api.users.models import User


def test_passwords_are_random(test_app, test_database, add_user):
    user_one = add_user("justatest", "test@test.com", "greaterthaneight")
    user_two = add_user("justatest2", "test@test2.com", "greaterthaneight")
    assert user_one.password != user_two.password


def test_encode_token(test_app, test_database, add_user):
    user = add_user("justatest", "test@test.com", "test")
    token_access = user.encode_token(user.id, "access")
    token_refresh = user.encode_token(user.id, "refresh")
    assert isinstance(token_access, str)
    assert isinstance(token_refresh, str)


def test_decode_token(test_app, test_database, add_user):
    user = add_user("justatest", "test@test.com", "test")
    token_access = user.encode_token(user.id, "access")
    token_refresh = user.encode_token(user.id, "refresh")
    assert isinstance(token_access, str)
    assert isinstance(token_refresh, str)
    assert User.decode_token(token_access) == user.id
    assert User.decode_token(token_refresh) == user.id
