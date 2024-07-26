# routes.py
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from table.table import Post
from engine.engine import Base, engine, SessionLocal
from typing import List
from model.Post import ResponseClass
import base64

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


@router.get("/get-all-post/{user_id}", status_code=status.HTTP_200_OK, response_model=List[ResponseClass])
async def get_all_post(user_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.user_id == user_id).all()  # Use Post.user_id instead of Post.id

    if not posts:
        raise HTTPException(status_code=404, detail="Data is not found")

    post_list: List[ResponseClass] = []
    for post in posts:
        images_str = ""
        if isinstance(post.images, bytes):
            images_str = base64.b64encode(post.images).decode('utf-8')  # Encode to base64 string
        elif isinstance(post.images, list):
            # Concatenate all images into one base64 string if list
            images_str = ''.join(
                base64.b64encode(img).decode('utf-8') if isinstance(img, bytes) else img for img in post.images)

        post_dict = post.__dict__

        # Ensure id is a string
        post_dict['id'] = str(post_dict.get('id', ''))

        # Ensure captions is a string
        post_dict['captions'] = post_dict.get('captions', '') or ''  # Default to empty string if None

        post_dict['images'] = images_str
        post_list.append(ResponseClass(**post_dict))

    return post_list
