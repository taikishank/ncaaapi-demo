import os
import httpx
from fastapi import FastAPI, HTTPException
import asyncio
import logging

BASE_URL = "https://api.sportsdata.io/v3/cbb/scores/json"
STATS_URL = "https://api.sportsdata.io/v3/cbb/stats/json"
API_KEY="828a039bc45c4450b89be0f13aefbb4e" # bad practice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# returns the roster of a specified team
# team_id is in string. ex "ucla", "sdsu", "smu"
async def fetch_roster(team_id: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/PlayersBasic/{team_id}"
    
    logging.info(f"Fetching roster for team: {team_id}")
    logging.info(f"Request url: {url}")

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
    logging.info(f"Response status: {response.status_code}")

    if response.status_code != 200:
        logging.error(f"Error response: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

# use team_id to fetch the logs for all games over the course of the season
async def fetch_team_logs(season: str, team_id: int, numberofgames: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/TeamGameStatsBySeason/{season}/{team_id}/{numberofgames}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()
    
    
# returns the logs of a player's season statistics
async def fetch_player_logs_season(season: str, player_id: int):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {"key": API_KEY}
    url = f"{STATS_URL}/PlayerSeasonStatsByPlayer/{season}/{player_id}"
    
    logger.info(f"Fetching data from URL: {url}")   # debugging
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as http_err:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except httpx.RequestError as req_err:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(req_err)}")


# solution for fetching all player ids from a single team
def get_player_ids(roster_data):
    return [player["PlayerID"] for player in roster_data if "PlayerID" in player]


# returns the season logs for every player on a team
async def fetch_team_player_logs(season: str, player_ids: list):
    tasks=[]
    for player_id in player_ids:
        tasks.append(fetch_player_logs_season(season="2025", player_id=player_id))
    player_logs = await asyncio.gather(*tasks, return_exceptions=True)
    return [log for log in player_logs if not isinstance(log, Exception)]

async def fetch_all_teams():
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/TeamsBasic"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        teams_data = response.json()
        filtered_teams = [
            {
                "TeamID": team.get("TeamID"),
                "Key": team.get("Key"),
                "School": team.get("School")
            }
            for team in teams_data
        ]
        
        return filtered_teams
    except httpx.HTTPStatusError as http_err:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except httpx.RequestError as req_err:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(req_err)}")