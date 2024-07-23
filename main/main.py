from fastapi import FastAPI
from router.user import users

app = FastAPI()

app.include_router(users.router)