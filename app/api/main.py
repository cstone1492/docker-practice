from typing import Union, Annotated
from pydantic import BaseModel, conint, constr, confloat, conset, validate_call, Field
from fastapi import FastAPI, Query, Path
from .app import app_create
from ..database import schema
import json

app = app_create()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@validate_call
@app.post("/post")
def create_post(
    title: Annotated[
        str, 
        Query(description="new post title", examples=['Title'])],
    content: Annotated[
        str, 
        Query(description="new post content", examples=['some content'])],
    published: Annotated[
        bool,
        Query(description='whether post has been published', examples=['True'])
    ],
):
    db_session=app.sql_session()
    post = schema.Post(title=title, content=content, published=published)
    post.create_unique_id()
    db_session.add(post)
    db_session.commit()
    db_session.close()
    return {title: title, content: content, published: published}