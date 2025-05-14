#! coding: utf-8
import uuid

import redis
from sqlalchemy import create_engine, Column, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import applications.chatbot.config as config


# Redis cache configuration (short term memory)
redis_client = redis.from_url(config.REDIS_URL)

# PostgreSQL database configuration (long term memory)
engine = create_engine(config.POSTGRES_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    name = Column(String)
    address = Column(Text)


class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(String, primary_key=True)
    user_id = Column(String)
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())


SessionLocal = sessionmaker(bind=engine)


def get_user_memory(user_id):
    session = SessionLocal()
    user = session.query(User).get(user_id)
    return {
        "name": user.name if user else "",
        "address": user.address if user else "",
        "history": [msg.content
                    for msg in session.query(ChatHistory).filter(ChatHistory.user_id == user_id)
                    .order_by(ChatHistory.timestamp.desc()).limit(5)]
    }


def save_user_memory(user_id, key, value):
    redis_client.hset(f'user:{user_id}', key, value)


def save_chat_history(user_id, role, content):
    session = SessionLocal()
    history = ChatHistory(id=str(uuid.uuid4()), user_id=user_id, role=role, content=content)