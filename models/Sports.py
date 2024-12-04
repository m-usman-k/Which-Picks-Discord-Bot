from pydantic import BaseModel

class StatModel(BaseModel):
    stat_name: str
    stat_value: str

class PlayerStatListModel(BaseModel):
    sports_name: str
    player_name: str
    all_stats: list[StatModel]

class TeamStatListModel(BaseModel):
    sports_name: str
    team_name: str
    all_stats: list[StatModel]

class WhichPickListModel(BaseModel):
    who_will_win: str
    why: str
    probability: float
    all_stats: list[StatModel]

class WillHappenListModel(BaseModel):
    will_happen_or_not: bool
    why: str
    probability: float
    all_stats: list[StatModel]