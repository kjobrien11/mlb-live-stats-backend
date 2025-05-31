import statsapi
from fastapi import FastAPI
from datetime import date

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    today = date.today()
    todays_schedule = statsapi.schedule(date=today)
    app.state.game_pks = [game['game_id'] for game in todays_schedule]
    app.state.line_scores = []

def retrieve_line_scores(game_pks):
    line_scores = []
    for game in game_pks:
        line_scores.append(statsapi.linescore(game))
    return line_scores

@app.get("/line-scores")
def get_line_scores():
    app.state.line_scores = retrieve_line_scores(app.state.game_pks)
    return app.state.line_scores
