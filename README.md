# Semantic Blog API Backend

A REST API backend for a semantic web blog.

## Getting Started

To run the application, you need to have Python 3.10 or later installed. Next, install the dependencies:

```bash
pip install -r requirements.txt
```

If you want to use sample data, you can populate the database with sample data:
```bash
python scripts/populate_db.py
```

To run the application backend:
```bash
uvicorn app.main:app --reload
```

## API Usage

To use the API, you can use the following endpoints:

- `POST /api/v1/users/`: Create a new user.
- `GET /api/v1/users/`: Get all users.
- `GET /api/v1/users/{user_id}`: Get a user by ID.
- `PUT /api/v1/users/{user_id}`: Update a user by ID.
- `DELETE /api/v1/users/{user_id}`: Delete a user by ID.
- `POST /api/v1/posts/`: Create a new post.
- `GET /api/v1/posts/`: Get all posts.
- `GET /api/v1/posts/{post_id}`: Get a post by ID.
- `PUT /api/v1/posts/{post_id}`: Update a post by ID.
- `DELETE /api/v1/posts/{post_id}`: Delete a post by ID.
- `POST /api/v1/posts/search/`: Search for posts.

## Frontend

To start the frontend:

```bash
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:3000

Features:
- User registration and login
- View all blog posts
- Create, edit, and delete your own posts
- Search posts using semantic search