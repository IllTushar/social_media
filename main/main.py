from fastapi import FastAPI
from router import post, comments, like, users, follower

app = FastAPI()

# User
app.include_router(users.router)

# Post
app.include_router(post.router)

# Comments
app.include_router(comments.router)

# Like
app.include_router(like.router)

# Follower
app.include_router(follower.router)
