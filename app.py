import statsapi
from datetime import date

today = date.today()
todays_schedule = statsapi.schedule(date=today)
game_pks = [game['game_id'] for game in todays_schedule]
print(game_pks)

for game in game_pks:
    print(statsapi.linescore(game))
    print()