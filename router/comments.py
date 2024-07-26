from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from table.table import CommentsTable, UserTable, Post
from engine.engine import Base, engine, SessionLocal
from model.comments import CreateComments, ResponseComments
from typing import Annotated, List

router = APIRouter(prefix="/comments", tags=['Comments'])

Base.metadata.create_all(bind=engine)


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_Session = Annotated[Session, Depends(connect_db)]


@router.post("/create-comments", status_code=status.HTTP_201_CREATED)
async def create_comments(request: CreateComments, db: db_Session):
    user = db.query(UserTable).filter(UserTable.id == request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User is not found!!")

    post = db.query(Post).filter(Post.id == request.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post is not found!!")

    if user and post:
        try:
            create_comment = CommentsTable(**request.dict())
            db.add(create_comment)
            db.commit()
            db.refresh(create_comment)
            return create_comment
        except Exception as e:
            raise HTTPException(status_code=403, detail=f"Comment is not created {e}")


@router.get("/get-all-comments", status_code=status.HTTP_200_OK, response_model=List[ResponseComments])
async def get_all_comments(user_id: int, post_id: int, db: Session = Depends(connect_db)):
    comments = db.query(CommentsTable).filter(CommentsTable.user_id == user_id, CommentsTable.post_id == post_id).all()

    if not comments:
        raise HTTPException(status_code=404, detail="Data is not found!!")

    comments_list: List[ResponseComments] = []
    for comment in comments:
        comment_dict = {
            "comment_id": comment.comment_id,  # Ensure the comment_id field is included
            "user_id": comment.user_id,
            "post_id": comment.post_id,
            "comments": comment.comments  # Ensure this matches the field name in ResponseComments
        }
        comments_list.append(ResponseComments(**comment_dict))

    return comments_list
