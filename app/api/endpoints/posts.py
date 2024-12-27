from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.database.session import get_db
from app.database.vector_store import vector_store
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, Post as PostSchema, PostSearch, PostWithScore
import uuid

router = APIRouter()

@router.post("/", response_model=PostSchema)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    vector_id = str(uuid.uuid4())
    db_post = Post(
        title=post.title,
        content=post.content,
        author_id=current_user.id,
        vector_id=vector_id
    )
    
    # Add to SQL database
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Add to vector database
    vector_store.add_post(
        post_id=vector_id,
        content=post.content,
        metadata={"title": post.title, "author_id": current_user.id}
    )
    
    return db_post

@router.get("/", response_model=List[PostSchema])
def get_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostSchema)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update SQL database
    for field, value in post_update.dict(exclude_unset=True).items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    
    # Update vector database
    if post_update.content is not None:
        vector_store.update_post(
            post_id=db_post.vector_id,
            content=db_post.content,
            metadata={"title": db_post.title, "author_id": current_user.id}
        )
    
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Delete from vector database
    vector_store.delete_post(db_post.vector_id)
    
    # Delete from SQL database
    db.delete(db_post)
    db.commit()

@router.post("/search", response_model=List[PostWithScore])
def search_posts(
    search: PostSearch,
    db: Session = Depends(get_db)
):
    # Search in vector database
    results = vector_store.search_posts(search.query, search.limit)
    
    # Combine results with similarity scores
    response = []
    for i, vector_id in enumerate(results["ids"][0]):
        post = db.query(Post).filter(Post.vector_id == vector_id).first()
        if post:
            response.append({
                "post": post,
                "similarity_score": 1 - (i / len(results["ids"][0]))  # Simple ranking-based score
            })
    
    return response 