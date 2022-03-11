from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, insert, select

from db import db
from models import BlogClick, BlogClickTable

router = APIRouter()

@router.get("/", response_model=BlogClick)
async def get_blog_click(blog_id: int):
    sql = select(
        [BlogClickTable.blog_id,
         func.count(BlogClickTable.blog_id).label("click")]
    ).where(BlogClickTable.blog_id == blog_id).group_by(BlogClickTable.blog_id)
    
    try:
        return await db.fetch_one(sql)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))


@router.post("/")
async def create_blog_click(blog_id: int):
    sql = insert(BlogClickTable).values(blog_id=blog_id)
    try:
        return await db.execute(sql)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail)
    