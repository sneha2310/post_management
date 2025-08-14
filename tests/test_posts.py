from typing import List
from app import schemas
import pytest

def test_get_posts(authorized_client, test_post):
    res = authorized_client.get("/posts/")
    def validate(post):

        return schemas.PostOut(**post)
    post_data = list(map(validate, res.json()))
    assert res.status_code == 200
    assert len(res.json()) == len(test_post)

def test_unauthorized_user_get_posts(client, test_post):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_one_user_get_posts(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f'/posts/{test_post[0].id}')
    post = schemas.PostOut(**res.json()[0])
    assert post.post.id == test_post[0].id
    assert post.post.content == test_post[0].content

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("awesome new title1", "awesome new content1", False),
    ("awesome new title2", "awesome new content2", True),
])
def test_create_post(authorized_client, test_post, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content,
                                                  "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    # assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_post, test_user):
    res = authorized_client.post("/posts/", json={"title": "arbitary title", "content": "content"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitary title"
    assert created_post.content == "content"
    assert created_post.published == True
    # assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_posts(client, test_post):
    res = client.post("/posts/", json={"title": "arbitary title", "content": "content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_posts(client, test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_posts(authorized_client, test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 200

def test_delete_posts_not_exists(authorized_client, test_post):
    res = authorized_client.delete("/posts/999")
    assert res.status_code == 404

def test_delete_posts_other_user(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_post, test_user):
    data = {
        "title": "updated_title",
        "content": "updated content"
    }

    res = authorized_client.put(f"/posts/{test_post[0].id}", json=data)
    updated_data = schemas.Post(**res.json())
    assert res.status_code == 200
    assert  updated_data.title == data['title']
    assert  updated_data.content == data['content']

def test_vote_on_post(authorized_client, test_post):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_post[3].id, "dir": 1}
    )
    assert res.status_code == 201
