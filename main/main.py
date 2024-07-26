from fastapi import FastAPI
from router.user import users
from router import post, comments

app = FastAPI()

# User
app.include_router(users.router)

# Post
app.include_router(post.router)

# Comments
app.include_router(comments.router)
