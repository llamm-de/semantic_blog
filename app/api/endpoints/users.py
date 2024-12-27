from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.database.session import get_db
from app.models.user import User
from app.models.post import Post
from app.schemas.user import UserCreate, User as UserSchema, Token, UserUpdate
from app.schemas.post import Post as PostSchema
from datetime import timedelta
from typing import List

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    hashed_password = security.get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"} 

@router.get("/me", response_model=UserSchema)
def read_current_user(
    current_user: User = Depends(deps.get_current_active_user)
):
    return current_user

@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    # Check email uniqueness if it's being updated
    if user_update.email is not None:
        db_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
    
    # Check username uniqueness if it's being updated
    if user_update.username is not None:
        db_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = security.get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me/posts", response_model=List[PostSchema])
def read_user_posts(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    posts = db.query(Post).filter(
        Post.author_id == current_user.id
    ).offset(skip).limit(limit).all()
    return posts 