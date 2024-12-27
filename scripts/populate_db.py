import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal, create_tables
from app.models.user import User
from app.models.post import Post
from app.core.security import get_password_hash
from app.database.vector_store import vector_store
import uuid

# Sample data
users = [
    {
        "email": "john@example.com",
        "username": "john_doe",
        "password": "Test123!@#",
        "posts": [
            {
                "title": "Introduction to Python",
                "content": "Python is a high-level programming language known for its simplicity and readability. It's great for beginners and professionals alike."
            },
            {
                "title": "Web Development with FastAPI",
                "content": "FastAPI is a modern web framework for building APIs with Python. It's fast, easy to use, and provides automatic API documentation."
            },
            {
                "title": "Understanding Bear Markets",
                "content": "A bear market occurs when stock prices fall 20% or more from recent highs. These periods often coincide with economic downturns and require careful investment strategies."
            },
            {
                "title": "The Majesty of Redwood Trees",
                "content": "Redwood trees are among the oldest living organisms on Earth. These giants can grow over 300 feet tall and live for thousands of years, creating unique ecosystems."
            },
            {
                "title": "African Elephants: Gentle Giants",
                "content": "African elephants are the largest land animals on Earth. These intelligent creatures live in complex social groups and display remarkable emotional intelligence."
            }
        ]
    },
    {
        "email": "jane@example.com",
        "username": "jane_smith",
        "password": "Test123!@#",
        "posts": [
            {
                "title": "Data Science Basics",
                "content": "Data science combines statistics, programming, and domain knowledge to extract insights from data. Python is a popular language for data science."
            },
            {
                "title": "Machine Learning Introduction",
                "content": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed."
            },
            {
                "title": "Stock Market Indicators",
                "content": "Technical analysis uses various indicators like moving averages, RSI, and MACD to predict market movements. Understanding these tools is crucial for traders."
            },
            {
                "title": "Rainforest Biodiversity",
                "content": "Tropical rainforests contain over half of the world's plant and animal species. The complex canopy structure creates multiple habitats for diverse life forms."
            },
            {
                "title": "Big Cats of the World",
                "content": "From lions to snow leopards, big cats are apex predators that play crucial roles in their ecosystems. Each species has unique adaptations for survival."
            }
        ]
    },
    {
        "email": "sarah@example.com",
        "username": "sarah_nature",
        "password": "Test123!@#",
        "posts": [
            {
                "title": "Ancient Olive Trees",
                "content": "Some olive trees in the Mediterranean are over 1000 years old. These ancient trees continue to produce olives and represent living history."
            },
            {
                "title": "Bonsai: Living Art",
                "content": "Bonsai is the Japanese art of growing and training miniature trees. It requires patience, skill, and deep understanding of tree biology."
            },
            {
                "title": "Endangered Species Recovery",
                "content": "Conservation efforts have helped species like the California Condor and Black Rhino recover from near extinction. These success stories show the importance of wildlife protection."
            }
        ]
    },
    {
        "email": "mike@example.com",
        "username": "mike_trader",
        "password": "Test123!@#",
        "posts": [
            {
                "title": "Cryptocurrency Markets",
                "content": "Digital currencies have created a new frontier in financial markets. Understanding blockchain technology is essential for modern investors."
            },
            {
                "title": "Value Investing Principles",
                "content": "Warren Buffett's approach to finding undervalued companies has proven successful over decades. Key principles include margin of safety and long-term thinking."
            },
            {
                "title": "Market Volatility",
                "content": "Volatility is a natural part of financial markets. Understanding how to manage risk during turbulent times is crucial for investment success."
            }
        ]
    },
    {
        "email": "lisa@example.com",
        "username": "lisa_wildlife",
        "password": "Test123!@#",
        "posts": [
            {
                "title": "Marine Mammals",
                "content": "Whales and dolphins are among the most intelligent animals on Earth. Their complex social structures and communication systems continue to amaze scientists."
            },
            {
                "title": "Urban Wildlife",
                "content": "Cities provide unique habitats for adaptable species. From raccoons to peregrine falcons, many animals have learned to thrive in urban environments."
            },
            {
                "title": "Migratory Birds",
                "content": "Bird migration is one of nature's most impressive phenomena. Some species travel thousands of miles each year between breeding and wintering grounds."
            }
        ]
    },
    {
        "email": "tom@example.com",
        "username": "tom_green",
        "password": "Test123!@#",
        "posts": [
            {
                "title": "Sacred Trees",
                "content": "Many cultures have sacred trees that play important roles in their traditions and beliefs. These trees often serve as focal points for communities."
            },
            {
                "title": "Urban Forests",
                "content": "City trees provide essential ecosystem services including air purification, temperature regulation, and stormwater management."
            },
            {
                "title": "Seasonal Changes",
                "content": "Trees in temperate regions undergo remarkable transformations throughout the year, from spring blooms to autumn colors."
            }
        ]
    }
]

def populate_db():
    db = SessionLocal()
    try:
        # Create tables if they don't exist
        create_tables()
        
        print("Creating users and posts...")
        for user_data in users:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                print(f"User {user_data['email']} already exists, skipping...")
                continue
            
            # Create user
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=get_password_hash(user_data["password"])
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created user: {user.username}")
            
            # Create posts for user
            for post_data in user_data["posts"]:
                vector_id = str(uuid.uuid4())
                post = Post(
                    title=post_data["title"],
                    content=post_data["content"],
                    author_id=user.id,
                    vector_id=vector_id
                )
                db.add(post)
                db.commit()
                
                # Add to vector database
                vector_store.add_post(
                    post_id=vector_id,
                    content=post_data["content"],
                    metadata={
                        "title": post_data["title"],
                        "author_id": user.id
                    }
                )
                print(f"Created post: {post.title}")
        
        print("Database populated successfully!")
    
    except Exception as e:
        print(f"Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_db() 