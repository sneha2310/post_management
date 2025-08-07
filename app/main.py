from . import model
from .database import engine
from .routers import post, user, auth

from fastapi import FastAPI

# Create the database tables if they don't exist
model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)  # Include the auth router
app.include_router(post.router)
app.include_router(user.router)


# data = [
#     { "title": "Shark Tank India", "content": "This is ep1", "published": False, "rating": 8 , 'id': 1},
#     { "title": "Shark Tank India", "content": "This is ep2", "rating": 8, 'id': 2 },
# ]
#
# def find_post(id):
#     for p in data:
#         if p['id'] == id:
#             return p
#     return None
#
# def find_index_post(id):
#     for i, p in enumerate(data):
#         if p['id'] == id:
#             return i
#     return None
#
# @app.get("/")
# def root():
#     return {"message": "Welcome to the FastAPI application!"}
#
# @app.get("/sql-alchemy")
# def test_post(db: Session = Depends(get_db)):
#     return {"message": "SQL Alchemy is working!"}
