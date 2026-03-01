from fastapi import APIRouter, HTTPException, Query
import json
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "rehab_centers.json")


@router.get("")
@router.get("/")
async def get_rehab_centers(city: str = Query(None)):
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            centers = json.load(f)

        if city:
            centers = [
                c for c in centers
                if c["city"].lower() == city.lower()
            ]

        return centers

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Rehab centers data file not found")