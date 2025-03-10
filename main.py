from fastapi import FastAPI
import httpx
from services.ncaa_api import fetch_team_logs, fetch_roster

app = FastAPI()

API_KEY = "your-api-key-here"
BASE_URL = "https://api.sportsdata.io/v3/cbb/scores/json"

# example of no API key
@app.get("/null")
async def does_nothing():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}?key=")
        return response.json()
    

@app.get("/active_players")
async def get_active_players():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/PlayersByActive?key={API_KEY}")
        return response.json()

@app.get("/roster/ucla")
async def get_ucla():
    return await fetch_roster("ucla")
    
@app.get("/logs/smu")
async def get_team1_logs():
    return await fetch_team_logs("2025", 1, "all")

# dynamic endpoints
@app.get("/logs/{team_id}")
async def get_team_logs(team_id: int, season: str="2025", numberofgames: str="all"):
    return await fetch_team_logs(season, team_id, numberofgames)
    

