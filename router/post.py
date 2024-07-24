# routes.py
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from table.table import Post
from engine.engine import Base, engine, SessionLocal

router = APIRouter(prefix="/post", tags=['Create Post'])

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create-post/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_post(user_id: str, file: UploadFile = File(...), captions: str = Form(None),
                      db: Session = Depends(get_db)):
    content = await file.read()

    # Validate the file size (limit to 100KB)
    MAX_FILE_SIZE = 100 * 1024  # 100KB
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size exceeds 100KB limit")

    try:
        image_record = Post(user_id=user_id, captions=captions, images=content)
        db.add(image_record)
        db.commit()
        db.refresh(image_record)
        return {
            "id": image_record.id,
            "user_id": image_record.user_id,
            "captions": image_record.captions,
            "message": "Image uploaded successfully"
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to upload image")
