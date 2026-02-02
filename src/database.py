import sqlite3
import json
from typing import Optional, Dict
from .models import Room

DB_PATH = "wnp.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        """테이블 생성 및 초기 데이터 주입"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                exits TEXT  -- JSON string으로 저장
            )
        ''')
        
        # 세이브 데이터 테이블 추가
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS saves (
                slot_id INTEGER PRIMARY KEY,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data TEXT NOT NULL  -- GameState JSON string
            )
        ''')
        
        self.conn.commit()
        
        # 초기 데이터가 없으면 주입 (Seeding)
        self.cursor.execute("SELECT count(*) FROM rooms")
        if self.cursor.fetchone()[0] == 0:
            self._seed_data()

    def save_game_state(self, slot_id: int, state_data: dict):
        """게임 상태를 JSON으로 저장"""
        json_data = json.dumps(state_data)
        self.cursor.execute("INSERT OR REPLACE INTO saves (slot_id, data) VALUES (?, ?)", (slot_id, json_data))
        self.conn.commit()

    def load_game_state(self, slot_id: int) -> Optional[dict]:
        """저장된 게임 상태를 불러옴"""
        self.cursor.execute("SELECT data FROM saves WHERE slot_id = ?", (slot_id,))
        row = self.cursor.fetchone()
        return json.loads(row[0]) if row else None


    def _seed_data(self):
        """초기 시나리오 데이터 삽입"""
        initial_rooms = [
            (
                "cavern", 
                "사악한 마법사의 동굴 (Cavern of the Evil Wizard)", 
                "당신은 사악한 마법사의 동굴에 서 있습니다.\n사방에 얼음 난쟁이들의 시체가 널브러져 있어 음산한 분위기를 자아냅니다.\n정면에는 사악한 마법사가 당신을 노려보고 있습니다!",
                json.dumps({"SOUTH": "tunnel"})
            ),
            (
                "tunnel", 
                "어두운 터널", 
                "동굴 밖으로 이어지는 어두운 터널입니다. 북쪽에서 찬 바람이 불어오고, 남쪽 끝에서는 뜨거운 열기가 느껴집니다.",
                json.dumps({"NORTH": "cavern", "SOUTH": "desert_entry"})
            ),
            (
                "desert_entry",
                "사막 입구 (Edge of the Desert)",
                "눈부신 햇살이 쏟아지는 사막의 입구입니다. 끝없는 모래 언덕이 남쪽으로 펼쳐져 있습니다.\n목이 마르기 시작합니다.",
                json.dumps({"NORTH": "tunnel", "SOUTH": "desert_path"})
            ),
            (
                "desert_path",
                "끝없는 사막 (Endless Desert)",
                "사방이 모래뿐인 사막 한가운데입니다. 북쪽으로 돌아가는 발자국이 희미합니다.\n남쪽으로는 모래 폭풍이 불고 있습니다.",
                json.dumps({"NORTH": "desert_entry", "SOUTH": "desert_maze_1"})
            ),
            (
                "desert_maze_1",
                "사막의 미로 (Desert Maze)",
                "모래 언덕이 끝없이 이어져 방향을 알 수 없습니다. 뼈만 남은 여행자의 흔적이 보입니다.",
                json.dumps({"NORTH": "desert_path", "SOUTH": "desert_maze_1", "EAST": "desert_maze_1", "WEST": "desert_maze_1"})
            ),
            (
                "oasis",
                "신비한 오아시스 (Mysterious Oasis)",
                "맑은 물이 솟아나는 오아시스입니다! 물가에는 '마법의 돌'처럼 보이는 것이 반짝입니다.\n동쪽으로는 거대한 절벽으로 이어지는 길이 보입니다.",
                json.dumps({"WEST": "desert_path", "EAST": "serpent_crossing"})
            ),
            (
                "serpent_crossing",
                "뱀의 길목 (Serpent's Crossing)",
                "거대한 협곡을 가로지르는 낡은 다리가 앞에 있습니다.\n하지만 다리 한가운데에 집채만 한 거대한 코브라가 똬리를 틀고 길을 막고 있습니다!\n뱀은 당신을 보며 위협적으로 '쉬익' 소리를 냅니다.",
                json.dumps({"WEST": "oasis"})  # 초기에는 뱀 때문에 건너갈 수 없음 (EAST 없음)
            ),
            (
                "town_entry",
                "마을 입구 (Town Entrance)",
                "다리를 건너 안전하게 마을 입구에 도착했습니다. 평화로운 음악 소리가 들려옵니다.",
                json.dumps({"WEST": "serpent_crossing"})
            )
        ]
        
        # 기존 데이터가 있으면 충돌할 수 있으니, OR IGNORE 혹은 REPLACE 사용
        self.cursor.executemany("INSERT OR REPLACE INTO rooms VALUES (?, ?, ?, ?)", initial_rooms)
        self.conn.commit()
        print("✅ DB: 사막 지역(Zone 1) 데이터 확장 완료.")

    def get_room(self, room_id: str) -> Optional[Room]:
        """DB에서 방 정보를 조회하여 Room 객체로 반환"""
        self.cursor.execute("SELECT id, name, description, exits FROM rooms WHERE id = ?", (room_id,))
        row = self.cursor.fetchone()
        
        if row:
            return Room(
                id=row[0],
                name=row[1],
                description=row[2],
                exits=json.loads(row[3])
            )
        return None

    def update_room_description(self, room_id: str, new_desc: str):
        """방 설명 업데이트 (예: 마법사 처치 후)"""
        self.cursor.execute("UPDATE rooms SET description = ? WHERE id = ?", (new_desc, room_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
