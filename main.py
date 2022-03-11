import os
import sys

import blog_star
import uvicorn
from fastapi import FastAPI, status

import blog
import blog_click
from db import database, init_db
from settings import cfg

version = f"{sys.version_info.major}.{sys.version_info.minor}"


app = FastAPI(
    title="Workshop FastAPI",
    description="API สำหรับ Workshop",
    version="1.0",
    root_path=os.getenv("ROOT_PATH", "")
)

if cfg.MODE == "dev":
    from fastapi.middleware.cors import CORSMiddleware
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI . Using Python {version}"
    return {"message": message}


app.include_router(
    blog.router,
    prefix="/blog",
    tags=["Blog"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Blog Not Found"}}
)

app.include_router(
    blog_click.router,
    prefix="/blog/click",
    tags=["Blog Click"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}}
)


app.include_router(
    blog_star.router,
    prefix="/blog/star",
    tags=["Blog Star"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}}
)

@app.on_event("startup")
async def startup():
    await database.connect()
    init_db()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        proxy_headers=True,
        forwarded_allow_ips="*",
        root_path=os.getenv("ROOT_PATH", ""),
    )
