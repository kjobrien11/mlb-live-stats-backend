import statsapi
from fastapi import FastAPI
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST, etc.
    allow_headers=["*"],              # Authorization, Content-Type, etc.
)

@app.on_event("startup")
async def startup_event():
    today = date.today()
    todays_schedule = statsapi.schedule(date=today)
    app.state.game_pks = [game['game_id'] for game in todays_schedule]
    app.state.line_scores = []
    app.state.base_status = {}

def retrieve_line_scores(game_pks):
    line_scores = []
    for game in game_pks:
        print(game)
        current_line_score = statsapi.linescore(game)
        print(current_line_score)
        line_scores.append(current_line_score)
    return line_scores


def get_base_occupancy(game_pks):
    base_info = []
    

    for game in game_pks:
        url = f"https://statsapi.mlb.com/api/v1.1/game/{game}/feed/live"
        response = requests.get(url)
        data = response.json()

        try:
            # Base occupancy
            offense = data["liveData"]["linescore"]["offense"]
            base_status = {
                "1B": offense.get("first") is not None,
                "2B": offense.get("second") is not None,
                "3B": offense.get("third") is not None
            }

            # Teams
            teams = data["gameData"]["teams"]
            home_team = teams["home"]["name"]
            away_team = teams["away"]["name"]

            # Outs and inning status
            outs = data["liveData"]["plays"]["currentPlay"]["count"]["outs"]
            inning = data["liveData"]["linescore"]["currentInning"]
            is_top = data["liveData"]["linescore"]["isTopInning"]
            inning_half = "Top" if is_top else "Bottom"
            inning_status = f"{inning_half} {inning}"

            # Score
            score_data = data["liveData"]["linescore"]["teams"]
            home_score = score_data["home"]["runs"]
            away_score = score_data["away"]["runs"]

            base_info.append( {
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score,
                "outs": outs,
                "inning_status": inning_status,
                "base_occupancy": base_status
            })

        except KeyError as e:
            return {"error": f"Missing data: {e}"}

    return base_info


@app.get("/line-scores")
def get_line_scores():
    app.state.line_scores = retrieve_line_scores(app.state.game_pks)
    return app.state.line_scores

@app.get("/game-information")
def get_line_scores():
    app.state.base_status = get_base_occupancy(app.state.game_pks)
    return app.state.base_status
