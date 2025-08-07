from .. import model, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix='/posts',
    tags=['Posts']  # This will group the endpoints under the "Posts" tag in the API documentation
)

# Using SQLAlchemy ORM to fetch post by id
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0,
              search: Optional[str]= ""): # id: int it defines that id which is coming as str type converts it to int
    post = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all() # filter the post by id
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Posts not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) # status_code is used to set the response status code for create i.e. 201 instead of 200
def create_posts(post: schemas.Post, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)): # read the data as Post model from the request body
    print(current_user)
    new_post = model.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post


# Using SQLAlchemy ORM to fetch post by id
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)): # id: int it defines that id which is coming as str type converts it to int
    post = db.query(model.Post).filter(model.Post.id == id).first() # filter the post by id
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post


# Using SQLAlchemy ORM to delete post by id
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == id)  # delete the post by id

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully!"}


# Using SQLAlchemy ORM to update post by id
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post:schemas.Post, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    updated_post = db.query(model.Post).filter(model.Post.id == id)  # filter the post by id

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()



# @app.get("/get-posts")
# def get_posts():
#     cursor.execute("Select * from public.posts")
#     data = cursor.fetchall()
#     return {"data": data}

# @app.get("/get-post/{id}")
# def get_post(id: int, response: Response): # id: int it defines that id which is coming as str type converts it to int
#     id = find_post(id)
#     if not id:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"Post with id {id} not found"} # instead of this we can use HTTPException which is more elegant
#     return {"data": id}

# @app.get("/get-post/{id}")
# def get_post(id: int): # id: int it defines that id which is coming as str type converts it to int
#     cursor.execute("""Select * from public.posts where id = %s""", (str(id),))
#     id = cursor.fetchone()
#     if not id:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     return {"data": id}


# @app.post("/create-post", status_code=status.HTTP_201_CREATED) # status_code is used to set the response status code for create i.e. 201 instead of 200
# def create_item(item: dict=Body(...) ): # read the data as dict from the request body
# --------------------------------------------------
# def create_posts(post: Post): # read the data as Post model from the request body
#     cursor.execute("""Insert into public.posts (title, content, published) values (%s, %s, %s) returning *""",(post.title, post.content, post.published))
#     data = cursor.fetchone()
#     conn.commit()
# ---------------------------------------------------
    # post_data = post.dict() # get the data through the dictionary
    # post_data['id'] = randrange(1,100000)
    # data.append(post_data)
    # ---------------------------------------------------
    # return {"message": "Post created successfully!", "data": data}
    # ---------------------------------------------------

# @app.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     post = find_index_post(id)
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     data.pop(post)
#     return Response(content=f"Post with id {id} deleted successfully")

# @app.delete("/delete-post/{id}")
# def delete_post(id: int, response: Response):
#     cursor.execute("""Delete from public.posts where id = %s returning *""", (str(id),))
#     data = cursor.fetchone()
#     conn.commit()
#     return {"message": "Post deleted successfully!", "data": data}


# @app.put("/update-post/{id}")
# def update_post(id: int, post: Post):
#     post_index = find_index_post(id)
#     if post_index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     updated_post = post.dict()
#     updated_post['id'] = id
#     data[post_index] = updated_post
#     return {"message": "Post updated successfully!", "data": updated_post}

# @app.put("/update-post/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute("""Update public.posts set title = %s, content = %s, published = %s where id = %s returning *""", (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     return {"message": "Post updated successfully!", "data": updated_post}

