from http.client import responses

from jose import jwt
from app import schemas
from app.config import settings
import pytest

def test_client(client):
    res = client.get("/")
    # assert

def test_create_user(client):
    res = client.post('/users/', json={"email": "hello@gmail.com", "password": "1234"})
    validated_data = schemas.UserResponse(**res.json())
    assert validated_data.email == "hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post('/login/', data={"username": test_user["email"], "password": test_user["password"]})
    res_validate = schemas.Token(**res.json())
    payload = jwt.decode(res_validate.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id: str = payload.get("user_id")
    assert id == test_user["id"]
    assert res_validate.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("qwer@gmail.com", "1234", 403),
    ("hello@gmail.com", "4321", 403),
    ("asdf", "1234", 403),
    (None, "1234", 403),
    ("hello@gmail.com", None, 403)
])
def test_incorrect_login_user(email, password, status_code, client, test_user):
    res = client.post('/login/', data={"username": email, "password": password})
    assert res.status_code == status_code