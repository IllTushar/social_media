from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from model.follower import CreateFollower, Follower
from engine.engine import engine, Base, SessionLocal
from typing import Annotated
from table.table import UserTable, Post, Follower

router = APIRouter(prefix="/follower", tags=['Followers'])

Base.metadata.create_all(bind=engine)


def connection_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_Session = Annotated[Session, Depends(connection_db)]


@router.post("/create-follower", status_code=status.HTTP_201_CREATED)
async def create_follower(request: CreateFollower, db: Session = Depends(connection_db)):
    user = db.query(UserTable).filter(UserTable.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!!")

    follower = db.query(UserTable).filter(UserTable.id == request.follower_id).first()
    if not follower:
        raise HTTPException(status_code=404, detail="Follower not found!!")

    try:
        create_follower_data = Follower(user_id=request.user_id, follower_id=request.follower_id)
        db.add(create_follower_data)
        db.commit()
        db.refresh(create_follower_data)
        return {"data": create_follower_data}
    except Exception as e:
        db.rollback()  # Make sure to rollback in case of exception
        raise HTTPException(status_code=403, detail=f"Error creating follower relationship: {e}")
