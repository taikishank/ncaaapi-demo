Before doing anything, make sure you have the following installed with pip:
pip install fastapi uvicorn httpx python-dotenv

How to get FastAPI working
- Create your sportdataio account at https://sportsdata.io/
- Copy these two files into your directory
- Insert your API key from sportsdataio
- While inside of the project directory use the following: uvicorn main:app --reload
- Go to http://127.0.0.1:8000/docs
- Test your API calls!

Documentation can be found at https://sportsdata.io/developers/api-documentation/ncaa-basketball
Scrambled data https://sportsdata.io/developers/data-dictionary/ncaa-basketball
