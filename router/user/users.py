from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from model.UserModel import CreateUser
from engine.engine import Base, engine, SessionLocal
from typing import Annotated
from passlib.context import CryptContext
from table.table import UserTable
from datetime import date

router = APIRouter(prefix="/users", tags=['User Registration'])

Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_Session = Annotated[Session, Depends(connect_db)]


def validation_method(password: str):
    if not len(password) >= 5:
        return False, password
    else:
        return True, password


def dob(DOB: date) -> bool:
    # Define the cutoff date as January 1, 2007
    cutoff_date = date(2007, 1, 1)
    # Check if the given DOB is greater than the cutoff date
    return DOB > cutoff_date


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUser, db: db_Session):
    password_status, password = validation_method(request.password)
    date_of_birth = dob(request.DOB)
    if password_status and date_of_birth:
        create_user = UserTable(
            name=request.name,
            email=request.email,
            password=pwd_context.hash(password),
            DOB=request.DOB
        )
        db.add(create_user)
        db.commit()
        db.refresh(create_user)
        return create_user
    elif not password_status and date_of_birth:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Password is too short!->{password}")
    elif password_status and not date_of_birth:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only users born after 2007 can create an account!")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Check your credentials!")
