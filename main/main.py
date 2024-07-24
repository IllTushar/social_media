from fastapi import FastAPI
from router.user import users
from router import post

app = FastAPI()

app.include_router(users.router)

app.include_router(post.router)
