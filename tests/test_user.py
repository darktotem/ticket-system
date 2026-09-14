from models.user import User


def test_hash_password_produces_a_hash_not_the_raw_password():
    hashed = User.hash_password("mypassword")
    assert hashed != "mypassword"
    assert isinstance(hashed, str)


def test_hash_password_is_deterministic():
    assert User.hash_password("mypassword") == User.hash_password("mypassword")


def test_check_password_true_for_correct_password():
    user = User("Jane Doe", "jane@example.com", User.hash_password("mypassword"))
    assert user.check_password("mypassword") is True


def test_check_password_false_for_wrong_password():
    user = User("Jane Doe", "jane@example.com", User.hash_password("mypassword"))
    assert user.check_password("wrongpassword") is False


def test_role_defaults_to_user():
    user = User("Jane Doe", "jane@example.com", "somehash")
    assert user.role == "user"


def test_to_dict_contains_expected_fields():
    user = User("Jane Doe", "jane@example.com", "somehash")
    data = user.to_dict()
    assert data == {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password_hash": "somehash",
        "role": "user",
    }


def test_from_dict_roundtrip():
    original = User("Jane Doe", "jane@example.com", User.hash_password("mypassword"))
    rebuilt = User.from_dict(original.to_dict())

    assert rebuilt.name == original.name
    assert rebuilt.email == original.email
    assert rebuilt.password_hash == original.password_hash
    assert rebuilt.check_password("mypassword") is True
