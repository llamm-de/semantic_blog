# Blog API Backend

A REST API backend for a web blog built with FastAPI, SQLAlchemy, and ChromaDB. This API allows users to create, read, update, and delete blog posts while storing user data in SQLite and blog content in a vector database (ChromaDB).

## Features

- User authentication and management
- CRUD operations for blog posts
- Vector-based content storage using ChromaDB
- SQLite database for user management
- FastAPI-powered REST API

## Project Structure

## Development

To run tests:
```
pytest
```

## Sample Data

To populate the database with sample data:
```bash
python scripts/populate_db.py
```

This will create:
- 3 users with secure passwords
- 2 blog posts per user
- Vector embeddings for semantic search

Sample users:
1. john_doe@example.com / Test123!@#
2. jane_smith@example.com / Test123!@#
3. bob_wilson@example.com / Test123!@#

## License
