from pydantic import BaseModel, constr, validator
from typing import Optional
from datetime import datetime
import re
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    
    def handle_data(self, d):
        self.text.append(d)
    
    def get_data(self):
        return ''.join(self.text)

def strip_html(text: str) -> str:
    stripper = HTMLStripper()
    stripper.feed(text)
    return stripper.get_data()

class PostBase(BaseModel):
    title: constr(min_length=1, max_length=200)
    content: constr(min_length=1, max_length=10000)

    @validator('content')
    def sanitize_content(cls, v):
        # Strip HTML tags
        v = strip_html(v)
        # Remove multiple spaces
        v = re.sub(r'\s+', ' ', v)
        return v.strip()

    @validator('title')
    def sanitize_title(cls, v):
        # Strip HTML and special characters
        v = strip_html(v)
        v = re.sub(r'[^\w\s-]', '', v)
        return v.strip()

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=200)] = None
    content: Optional[constr(min_length=1, max_length=10000)] = None

    @validator('content')
    def sanitize_content(cls, v):
        if v is not None:
            v = strip_html(v)
            v = re.sub(r'\s+', ' ', v)
        return v.strip() if v else v

    @validator('title')
    def sanitize_title(cls, v):
        if v is not None:
            v = strip_html(v)
            v = re.sub(r'[^\w\s-]', '', v)
        return v.strip() if v else v

class PostInDB(PostBase):
    id: int
    author_id: int
    vector_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Post(PostInDB):
    pass

class PostSearch(BaseModel):
    query: str
    limit: Optional[int] = 10 

class PostWithScore(BaseModel):
    post: Post
    similarity_score: float 