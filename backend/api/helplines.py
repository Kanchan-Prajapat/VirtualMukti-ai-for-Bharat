from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "helplines.json")


@router.get("")
@router.get("/")
async def get_helplines():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Helplines data file not found")