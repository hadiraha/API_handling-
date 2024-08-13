#SQLAlchemy models
from sqlalchemy import Column, Integer, Text, DateTime, func, UniqueConstraint
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index= True)
    username = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_arg__ = (
        UniqueConstraint()
    )

class Profile(Base):
    __tablename__ = "fetched"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text)
    name = Column(Text)
    pic_s = Column(Text)
    follower_cnt = Column(Text)
    follow_cnt = Column(Text)
    url = Column(Text)
    video_cnt = Column(Text)
    video_visit = Column(Text)
    description = Column(Text)
    follower_cnt_num = Column(Text)