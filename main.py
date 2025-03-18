from fastapi import FastAPI
import httpx
from ncaa_api import *

app = FastAPI()

API_KEY = "828a039bc45c4450b89be0f13aefbb4e"
BASE_URL = "https://api.sportsdata.io/v3/cbb/scores/json"
    
# return all active players
@app.get("/active_players")
async def get_active_players():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/PlayersByActive?key={API_KEY}")
        return response.json()

# return the UCLA roster
@app.get("/roster/ucla")
async def get_ucla():
    return await fetch_roster("ucla")
    
# sample response for team_id=1 (ie SMU)
@app.get("/logs/smu")
async def get_team1_logs():
    return await fetch_team_logs("2025", 1, "all")

# dynamic endpoints
@app.get("/logs/{team_id}")
async def get_team_logs(team_id: int, season: str="2025", numberofgames: str="all"):
    return await fetch_team_logs(season, team_id, numberofgames)

# testing function
# @app.get("/player/stats/test")
# async def get_player_logs_season(season: str="2025"):
#     return await fetch_player_logs_season(season, player_id=60023623)
######################


#   solution for fetching all player ids from a single team
#   fetch the roster of a specific team and return all of the player ids
@app.get("/roster/ucla/player/ids")
async def fetch_ucla_player_ids():
    roster_data = await fetch_roster("ucla")
    return get_player_ids(roster_data)

# returns JSON response containing all UCLA player logs for the season
# calls on above function to retrieve all player ids, then fetches each players' season data
@app.get("/sample/team")
async def fetch_ucla_player_logs():
    roster_data = await fetch_ucla_player_ids()
    return await fetch_team_player_logs("2025", roster_data)