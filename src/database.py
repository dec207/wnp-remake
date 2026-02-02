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
        self.conn.commit()
        
        # 초기 데이터가 없으면 주입 (Seeding)
        self.cursor.execute("SELECT count(*) FROM rooms")
        if self.cursor.fetchone()[0] == 0:
            self._seed_data()

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
                "사방이 모래뿐인 사막 한가운데입니다. 태양은 뜨겁고 방향 감각이 흐려집니다.\n멀리 동쪽에 야자수가 보이는 것 같습니다.",
                json.dumps({"NORTH": "desert_entry", "EAST": "oasis"})
            ),
            (
                "oasis",
                "신비한 오아시스 (Mysterious Oasis)",
                "맑은 물이 솟아나는 오아시스입니다! 물가에는 '마법의 돌'처럼 보이는 것이 반짝입니다.",
                json.dumps({"WEST": "desert_path"})
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
