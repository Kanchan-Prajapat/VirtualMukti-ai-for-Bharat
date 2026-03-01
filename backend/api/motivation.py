from fastapi import APIRouter, HTTPException
import json
import os
import random

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "stories.json")


@router.get("/quote")
async def get_random_quote():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            stories = json.load(f)

        if not stories:
            raise HTTPException(status_code=404, detail="No stories found")

        random_story = random.choice(stories)

        return {
            "quote": random_story["title"],
            "message": random_story["story"]
        }

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Stories data file not found")