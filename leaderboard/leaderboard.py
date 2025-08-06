import json
import os
from typing import List, Dict

def load_leaderboard() -> List[Dict]:
    try:
        with open("leaderboard/leaderboard.json", "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
def save_leaderboard(leaderboard: List[Dict]) -> None:
    with open("leaderboard/leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def add_new_entry(new_entry: Dict) -> None:
    leaderboard = load_leaderboard()
    leaderboard.append(new_entry)
    leaderboard.sort(key=lambda x: x["total_score"], reverse=True)
    if len(leaderboard) > 10:
        for i in range (len(leaderboard) - 10):
            leaderboard.pop(10)
    save_leaderboard(leaderboard)

print(load_leaderboard())