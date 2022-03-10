from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Index, Integer, Sequence, Text, Unicode, func,
                        text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import FetchedValue

from db import Base


class BlogTable(Base):
    __tablename__ = "blog"
    __table_args__ = (
        Index('blog_idx', "blog",
              postgresql_ops={"blog": "gin_trgm_ops"},
              postgresql_using='gin'),
        Index('title_idx', "title",
              postgresql_ops={"title": "gin_trgm_ops"},
              postgresql_using='gin'),
    )
    blog_id_seq = Sequence('blog_id_seq', metadata=Base.metadata)
    id = Column(Integer, blog_id_seq,
                server_default=blog_id_seq.next_value(), primary_key=True)
    title = Column(Unicode(length=255, collation='th_TH'),
                   index=True, nullable=False)
    slug = Column(Unicode(length=255, collation='th_TH'),
                  nullable=True, index=True)
    tags = Column(JSONB, default=text("'[]'::jsonb"),
                  server_default=text("'[]'::jsonb"), nullable=True)
    blog = Column(Text, nullable=False)
    disabled = Column(Boolean, nullable=True, server_default=text("False"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now(),
                        server_onupdate=FetchedValue(), onupdate=func.now())


class BlogClickTable(Base):
    __tablename__ = "blog_click"
    blog_click_id_seq = Sequence('blog_stat_id_seq', metadata=Base.metadata)
    id = Column(BigInteger, blog_click_id_seq,
                server_default=blog_click_id_seq.next_value(), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def blog_id(cls):
        return Column(Integer, ForeignKey("blog.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)


class BlogStarTable(Base):
    __tablename__ = "blog_star"
    blog_star_id_seq = Sequence('blog_star_id_seq', metadata=Base.metadata)
    id = Column(BigInteger, blog_star_id_seq,
                server_default=blog_star_id_seq.next_value(), primary_key=True)
    star = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def blog_id(cls):
        return Column(Integer, ForeignKey("blog.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=False, index=True)


class BlogBase(BaseModel):
    title: str
    tags: Optional[list] = []
    blog: str
    disabled: Optional[bool] = False

    class Config:
        orm_mode = True


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    tags: Optional[list] = None
    blog: Optional[str] = None
    disabled: Optional[bool] = None


class Blog(BlogBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None


class BlogClickBase(BaseModel):
    blog_id: int

    class Config:
        orm_mode = True


class BlogClickCreate(BlogClickBase):
    pass


class BlogClick(BaseModel):
    blog_id: int
    click: int


class BlogStarBase(BaseModel):
    blog_id: int
    star: int

    class Config:
        orm_mode = True


class BlogStarCreate(BlogStarBase):
    pass


class BlogStar(BaseModel):
    blog_id: int
    star: float
