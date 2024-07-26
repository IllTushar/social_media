from pydantic import BaseModel


class CreateFollower(BaseModel):
    user_id: int
    follower_id: int


class Follower(BaseModel):
    id: int
    user_id: int
    follower_id: int

    class Config:
        orm_mode = True
