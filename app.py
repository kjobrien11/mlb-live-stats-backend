import statsapi
from datetime import date

def get_line_scores(game_pks):
    line_scores = []
    for game in game_pks:
        line_scores.append(statsapi.linescore(game))
    return line_scores

def print_line_scores(line_scores):
    for game in line_scores:
        print(game)
        print()

if __name__ == "__main__":
    today = date.today()
    todays_schedule = statsapi.schedule(date=today)
    game_pks = [game['game_id'] for game in todays_schedule]
    
    line_scores = get_line_scores(game_pks)
    print_line_scores(line_scores)
