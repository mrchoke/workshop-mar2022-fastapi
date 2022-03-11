from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, insert, select

from db import db
from models import BlogStar, BlogStarTable, BlogStarCreate

router = APIRouter()

@router.get("/", response_model=BlogStar)
async def get_blog_star(blog_id: int):
    sql = select(
        [BlogStarTable.blog_id,
         func.avg(BlogStarTable.star).label("star")]
    ).where(BlogStarTable.blog_id == blog_id).group_by(BlogStarTable.blog_id)

    try:
        return await db.fetch_one(sql)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))


@router.post("/")
async def create_blog_start(blog_star: BlogStarCreate):
    sql = insert(BlogStarTable).values(blog_star.dict())
    try:
        return await db.execute(sql)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail)
