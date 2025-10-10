from typing import Dict, List, Tuple
from collections import defaultdict


class PointsStore:
    def __init__(self) -> None:
        self._user_to_points: Dict[str, int] = defaultdict(int)

    def add_points(self, user_id: str, points: int) -> None:
        if points < 0:
            return
        self._user_to_points[user_id] += points

    def get_points(self, user_id: str) -> int:
        return int(self._user_to_points.get(user_id, 0))

    def get_leaderboard(self, limit: int = 10) -> Dict[str, List[Tuple[str, int]]]:
        items = sorted(self._user_to_points.items(), key=lambda kv: kv[1], reverse=True)
        return {"leaders": items[:limit]}
