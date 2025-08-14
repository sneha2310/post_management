from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import  settings
from app import model
from alembic import command

# client = TestClient(app)

engine = create_engine(f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test")  # echo=True for debugging SQL queries
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def session():
    #  With alembic
    # command.upgrade("head")
    # command.upgrade("base")

    # Without alembic

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user1(client):
    user_data = {"email": "hello123@gmail.com", "password": "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = "1234"
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello@gmail.com", "password": "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = "1234"
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post(test_user, session, test_user1):
    post_data = [
        {"title": "first title", "content": "first content", "owner_id":test_user["id"]},
        {"title": "second title", "content": "second content", "owner_id": test_user["id"]},
        {"title": "third title", "content": "third content", "owner_id": test_user["id"]},
        {"title": "fourth title", "content": "fourth content", "owner_id": test_user1["id"]},
        {"title": "fifth title", "content": "fifth content", "owner_id": test_user1["id"]}
    ]
    def create_post_model(post):
        return model.Post(**post)

    posts = list(map(create_post_model, post_data))
    session.add_all(posts)
    session.commit()
    posts = session.query(model.Post).all()
    return posts