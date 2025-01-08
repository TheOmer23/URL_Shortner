import os
from typing import Union
from fastapi import FastAPI, HTTPException, Request
from main import find_short_in_db, save_to_db, all_long_url, all_short_url
from fastapi.responses import (
    RedirectResponse,
    FileResponse,
)

app = FastAPI()

@app.get("/alllong")
async def get_all_long():
    return all_long_url()
    

@app.get("/allshort")
async def get_all_short():
    return all_short_url()


@app.post("/save")
async def save_url(request: Request):
    body = await request.json()  # Parse the raw JSON body
    url = body["original_url"]
    shorturl = await save_to_db(url)
    return shorturl

@app.get("/{short_url}")
async def read_root(short_url: str):
    try:
        # Call find_in_db and await its result
        url_object = await find_short_in_db(short_url)
        return RedirectResponse(url_object, status_code=301)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
