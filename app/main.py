from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import users, posts
from app.database.session import create_tables

app = FastAPI(
    title="Blog API",
    description="A REST API backend for a web blog",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])

@app.on_event("startup")
async def startup():
    create_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API"} 