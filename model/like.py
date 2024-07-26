from pydantic import BaseModel


class CreateLike(BaseModel):
    user_id: int
    post_id: int
    like: int


class ResponseLike(BaseModel):
    like_id: int
    user_id: int
    post_id: int
    like: int

    class Config:
        orm_mode = True
