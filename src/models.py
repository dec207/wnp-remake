from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Room:
    id: str
    name: str
    description: str
    exits: Dict[str, str] = field(default_factory=dict)
    items: List[str] = field(default_factory=list)

@dataclass
class Monster:
    id: str
    name: str
    hp: int
    damage: int
    description: str

@dataclass
class GameState:
    current_room_id: str = "cavern"
    score: int = 0
    gold: int = 0
    food: int = 100
    hp: int = 100         # 플레이어 HP 추가
    max_hp: int = 100
    inventory: List[str] = field(default_factory=list)
    flags: Dict[str, bool] = field(default_factory=dict)
    is_running: bool = True

    def add_score(self, points: int):

        self.score += points

    def decrease_food(self, amount: int = 1):
        self.food -= amount
        if self.food < 0:
            self.food = 0
