from typing import Union
from fastapi import FastAPI, HTTPException
from main import find_short_in_db
from fastapi.responses import (
    RedirectResponse,
    Response,
)

app = FastAPI()


@app.get("/9d6M4")
async def read_root():
    try:
        # Call find_in_db and await its result
        url_object = await find_short_in_db("9d6M4")
        return RedirectResponse(url_object, status_code=301)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
