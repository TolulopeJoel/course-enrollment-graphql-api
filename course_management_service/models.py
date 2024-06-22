from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .database import Base


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    title = Column(String(225), unique=True, nullable=False)
    description = Column(Text)
    author_id = Column(Integer, nullable=False)
