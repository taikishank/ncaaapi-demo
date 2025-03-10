import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "constants", ".env")
load_dotenv(dotenv_path)

# API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.sportsdata.io/v3/cbb/scores/json"

async def fetch_roster(team_id: str):
    API_KEY="your-api-key-here" # bad practice
    
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/PlayersByTeam/{team_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

async def fetch_team_logs(season: str, team_id: int, numberofgames: str):
    API_KEY="your-api-key-here" # bad practice
    
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/TeamGameStatsBySeason/{season}/{team_id}/{numberofgames}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()
    