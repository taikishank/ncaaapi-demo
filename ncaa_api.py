import os
import httpx
#from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

BASE_URL = "https://api.sportsdata.io/v3/cbb/scores/json"

async def fetch_roster(team_id: str):
    API_KEY="api-key-placeholder" # bad practice
    
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/PlayersBasic/{team_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

async def fetch_team_logs(season: str, team_id: int, numberofgames: str):
    API_KEY="api-key-placeholder" # bad practice
    
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/TeamGameStatsBySeason/{season}/{team_id}/{numberofgames}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()
    
async def fetch_player_logs_season(season: str, player_id: int):
    API_KEY="api-key-placeholder" # bad practice
    
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/PlayerSeasonStatsByPlayer/{season}/{player_id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()


async def fetch_all_player_logs_season(season: str):
    API_KEY="api-key-placeholder" # bad practice
    
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NO API KEY PROVIDED")

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    url = f"{BASE_URL}/PlayerSeasonStats/{season}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()


# solution for fetching all player ids from a single team
def get_player_ids(roster_data):
    return [player["PlayerID"] for player in roster_data if "PlayerID" in player]