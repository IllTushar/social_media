from pydantic import BaseModel


class CreateComments(BaseModel):
    user_id: int
    post_id: int
    comments: str


class ResponseComments(BaseModel):
    comment_id: int
    user_id: int
    post_id: int
    comments: str

    class Config:
        orm_mode = True
