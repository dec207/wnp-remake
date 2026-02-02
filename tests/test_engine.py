import unittest
import os
import shutil
from src.engine import GameEngine
from src.parser import parse_input
from src.database import Database

class TestWNP(unittest.TestCase):
    
    def setUp(self):
        """각 테스트 시작 전 실행: 깨끗한 DB 환경 준비"""
        self.test_db_path = "test_wnp.db"
        # 기존 test DB가 있다면 삭제
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
        # 엔진 초기화 (DB 경로를 테스트용으로 바꿔야 하지만, 
        # 현재 구조상 engine.py가 hardcoded 'wnp.db'를 씀.
        # 일단은 integration test 성격으로 wnp.db를 백업하고 테스트 후 복구하거나,
        # Database 클래스를 리팩토링해서 db_path를 주입받게 해야 함.
        # 여기서는 빠른 구현을 위해 Database 클래스를 monkey patch 하거나
        # 단순히 engine을 실행하여 로직만 검증 (DB 의존성 있는 부분은 주의)
        
        self.engine = GameEngine()
        # 테스트 속도를 위해 sleep 제거 (mocking 추천되지만 간단히 진행)

    def test_parser(self):
        """명령어 파서 테스트"""
        self.assertEqual(parse_input("GO NORTH"), ("GO", "NORTH"))
        self.assertEqual(parse_input("go north"), ("GO", "NORTH"))
        self.assertEqual(parse_input("GO TO THE NORTH"), ("GO", "NORTH"))
        self.assertEqual(parse_input(""), (None, None))

    def test_movement_and_food(self):
        """이동 및 갈증 시스템 테스트"""
        # 초기 위치: cavern -> 이동 -> tunnel
        initial_food = self.engine.state.food
        self.engine.process_command("GO", "SOUTH")
        
        self.assertEqual(self.engine.state.current_room_id, "tunnel")
        self.assertEqual(self.engine.state.food, initial_food - 1)

    def test_inventory_system(self):
        """아이템 획득 및 인벤토리 확인"""
        self.assertIn("THERMAL POD", self.engine.state.inventory)
        
        # 없는 아이템 사용 시도
        self.engine.process_command("THROW", "STONE")
        self.assertIn("THERMAL POD", self.engine.state.inventory) # 여전히 있어야 함

    def test_wizard_event(self):
        """마법사 처치 시나리오 테스트"""
        # 1. 동굴에서 POD 던지기
        self.engine.state.current_room_id = "cavern"
        self.engine.process_command("THROW", "POD")
        
        # 2. 결과 검증
        self.assertTrue(self.engine.state.flags.get("wizard_defeated"))
        self.assertEqual(self.engine.state.score, 50)
        self.assertNotIn("THERMAL POD", self.engine.state.inventory)

if __name__ == '__main__':
    unittest.main()
