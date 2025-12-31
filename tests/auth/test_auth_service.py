import pytest
from jose import jwt
from src.auth import service


def test_access_token_expire_minutes():
    assert service.access_token_expire_minutes() == 30


def test_create_access_token():
    token = service.create_access_token("123")
    assert {"sub": "123"}.items() <= jwt.decode(
        token, key=service.SECRET_KEY, algorithms=[service.ALGORITHM]
    ).items()


def test_password_hashes():
    password = "password"
    assert service.verify_password(password, service.get_password_hash(password))


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await service.get_user(registered_user["email"])

    assert user["email"] == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await service.get_user("test@email.com")

    assert user is None


@pytest.mark.anyio
async def test_authenticate_user(registered_user: dict):
    user = await service.authenticate_user(registered_user["email"], registered_user["password"])
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_authenticate_user_not_found():
    with pytest.raises(service.HTTPException):
        await service.authenticate_user("test@example.net", "1234")


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(registered_user: dict):
    with pytest.raises(service.HTTPException):
        await service.authenticate_user(registered_user["email"], "wrong_password")


@pytest.mark.anyio
async def test_get_current_user(registered_user: dict):
    token = service.create_access_token(registered_user["email"])
    user = await service.get_current_user(token)
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_current_user_invalid_token():
    with pytest.raises(service.HTTPException):
        await service.get_current_user("invalid token")
