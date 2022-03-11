from typing import Union

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete, insert, select, update

from blog_click import create_blog_click
from db import db
from models import Blog, BlogBase, BlogTable, BlogUpdate

router = APIRouter()


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: BlogBase):
    sql = insert(BlogTable).values(blog.dict())
    try:
        return await db.execute(sql)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))


@router.get("/", response_model=Union[list[Blog], Blog])
async def get_blog(id: int = None, disabled: bool = False):
    """
        # รายละเอียด
        
        * ถ้าไม่มี `id` จะได้ผลลัพธ์เป็น `Array` ของ `Object` Blog ทั้งหมด
        * ถ้ามี `id` จะได้ผลลัพธ์เป็น `Object` ของ Blog
        
    """
    sql = select(BlogTable).where(BlogTable.disabled == disabled)

    if id is not None:
        sql = sql.where(BlogTable.id == id)
        await create_blog_click(id)
        

    try:
       return await db.fetch_one(sql) if id else await db.fetch_all(sql)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))
        
        
@router.put("/", response_model=None)
async def update_blog(blog: BlogUpdate):
    sql = update(BlogTable).where(BlogTable.id == blog.id).values(blog.dict())
    try:
        return await db.execute(sql)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))
        
@router.delete("/", response_model=None)
async def delete_blog(id: int):
    sql = delete(BlogTable).where(BlogTable.id == id)
    try:
        return await db.execute(sql)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))
