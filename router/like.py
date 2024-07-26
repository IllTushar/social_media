from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from model.like import CreateLike, ResponseLike
from sqlalchemy.orm import Session
from table.table import UserTable, Post, LikeTable

from engine.engine import Base, SessionLocal, engine

router = APIRouter(prefix="/likes", tags=['Like'])

Base.metadata.create_all(bind=engine)


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_Session = Annotated[Session, Depends(connect_db)]


@router.post("/create-like", status_code=status.HTTP_201_CREATED)
async def create_like(request: CreateLike, db: db_Session):
    user = db.query(UserTable).filter(UserTable.id == request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User is not found!!")

    post = db.query(Post).filter(Post.id == request.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post is not found!!")
    if user and post:
        try:
            create_like_data = LikeTable(**request.dict())
            db.add(create_like_data)
            db.commit()
            db.refresh(create_like_data)
            return {"data": create_like_data}
        except Exception as e:
            raise HTTPException(status_code=403, detail=f"Not found!!{e}")


@router.get("/all-like/{user_id}/{post_id}", status_code=status.HTTP_200_OK, response_model=List[ResponseLike])
async def get_all_like(user_id: int, post_id: int, db: db_Session):
    data = db.query(LikeTable).filter(LikeTable.user_id == user_id, LikeTable.post_id == post_id).all()
    like_list: List[ResponseLike] = []
    if not data:
        raise HTTPException(status_code=404, detail="Data is not found!!")

    for like in data:
        like_dict = {
            "like_id": like.like_id,
            "user_id": like.user_id,
            "post_id": like.post_id,
            "like": like.like
        }
        like_list.append(ResponseLike(**like_dict))
    return like_list
