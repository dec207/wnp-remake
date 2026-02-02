import time
import dataclasses
from typing import Dict
from .models import GameState, Room
from .database import Database

class GameEngine:
    def __init__(self):
        self.state = GameState()
        self.db = Database()
        # 테스트용 초기 아이템 지급
        if not self.state.inventory:
             self.state.inventory.append("THERMAL POD")

    def process_command(self, verb: str, noun: str):
        if verb in ["QUIT", "EXIT"]:
            self.state.is_running = False
            self.db.close()
            print("\n게임을 종료합니다. 안녕히 가세요!")
            return

        if verb in ["SAVE"]:
            self._handle_save()
        elif verb in ["LOAD", "RESTORE"]:
            self._handle_load()
        elif verb in ["GO", "WALK", "MOVE", "RUN"]:
            self._handle_move(noun)
        elif verb in ["N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"]:
            direction_map = {"N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST"}
            full_dir = direction_map.get(verb, verb)
            self._handle_move(full_dir)
        elif verb in ["INV", "INVENTORY", "I"]:
            print(f"\n🎒 인벤토리: {', '.join(self.state.inventory) if self.state.inventory else '비어있음'}")
        elif verb in ["THROW", "MELT", "USE"]:
            self._handle_item_use(verb, noun)
        elif verb in ["GET", "TAKE", "PICKUP"]:
            self._handle_get(noun)
        elif verb in ["DRINK"]:
            self._handle_drink(noun)
        else:
            print("\n🤔 무슨 말인지 모르겠습니다.")

    def _handle_save(self):
        try:
            state_dict = dataclasses.asdict(self.state)
            self.db.save_game_state(1, state_dict)
            print("\n💾 게임이 저장되었습니다! (Slot 1)")
        except Exception as e:
            print(f"\n🚫 저장 중 오류 발생: {e}")

    def _handle_load(self):
        try:
            saved_data = self.db.load_game_state(1)
            if saved_data:
                self.state = GameState(**saved_data)
                self.state.is_running = True
                print("\n📂 게임을 불러왔습니다! (Slot 1)")
                self.render()
            else:
                print("\n🚫 저장된 게임이 없습니다.")
        except Exception as e:
            print(f"\n🚫 불러오기 중 오류 발생: {e}")

    def _handle_get(self, noun: str):
        """아이템 줍기"""
        if self.state.current_room_id == "oasis" and noun in ["STONE", "MAGIC STONE"]:
            if "MAGIC STONE" not in self.state.inventory:
                print("\n✨ 오아시스 물가에서 신비하게 빛나는 '마법의 돌'을 주웠습니다!")
                self.state.inventory.append("MAGIC STONE")
            else:
                print("\n이미 가지고 있습니다.")
        else:
            print("\n여기에는 그런 것이 없습니다.")

    def _handle_move(self, direction: str):
        if not direction:
            print("\n어디로 갈까요?")
            return
            
        current_room = self.db.get_room(self.state.current_room_id)
        next_room_id = None

        # 1. 특수 미로 로직 (사막)
        if self.state.current_room_id == "desert_maze_1":
            if direction == "EAST":
                next_room_id = "oasis"
                print("\n✨ 모래 폭풍을 뚫고 오아시스를 발견했습니다!")
            elif direction == "NORTH":
                next_room_id = "desert_path"
            else:
                next_room_id = "desert_maze_1"
                print("\n🌪️ 한참을 걸었지만, 제자리로 돌아온 것 같습니다...")

        # 2. 뱀의 길목 (Serpent's Crossing) 특수 이동
        elif self.state.current_room_id == "serpent_crossing" and direction == "EAST":
            if self.state.flags.get("snake_cleared"):
                next_room_id = "town_entry"
            else:
                print("\n🐍 거대한 코브라가 '쉬익!' 거리며 길을 막아섭니다. 지나갈 수 없습니다!")
                return
        
        # 3. 일반 이동 로직
        elif direction in current_room.exits:
            next_room_id = current_room.exits[direction]
        
        # 4. 이동 결과 처리
        if next_room_id:
            self.state.current_room_id = next_room_id
            
            is_desert = "desert" in next_room_id or "oasis" in next_room_id
            cost = 2 if is_desert else 1
            self.state.decrease_food(cost)
            
            print(f"\n🏃 {direction} 방향으로 이동합니다... {'(🥵 덥습니다!)' if is_desert else ''}")
        else:
            print("\n🚫 그쪽으로는 갈 수 없습니다.")

    def _handle_item_use(self, verb: str, noun: str):
        current_room = self.state.current_room_id
        
        # 마법사 처치 이벤트
        if current_room == "cavern" and not self.state.flags.get("wizard_defeated"):
            if noun in ["POD", "THERMAL POD"] and "THERMAL POD" in self.state.inventory:
                print("\n🔥 당신은 Thermal Pod를 사악한 마법사에게 던졌습니다!")
                time.sleep(1)
                print("💥 팟이 폭발하며 강렬한 열기가 동굴을 채웁니다!")
                time.sleep(1)
                print("😱 마법사는 비명을 지르며 수증기가 되어 사라졌습니다.")
                
                self.state.flags["wizard_defeated"] = True
                self.state.add_score(50)
                self.state.inventory.remove("THERMAL POD")
                
                new_desc = "사악한 마법사의 동굴입니다. 이제 마법사는 없고, 바닥에 물웅덩이만 남아있습니다."
                self.db.update_room_description("cavern", new_desc)
                return

        # 뱀 이벤트 (Serpent's Crossing)
        if current_room == "serpent_crossing" and not self.state.flags.get("snake_cleared"):
            if noun in ["STONE", "MAGIC STONE"] and "MAGIC STONE" in self.state.inventory:
                print("\n💎 당신은 마법의 돌을 절벽 아래로 힘껏 던졌습니다!")
                time.sleep(1)
                print("🐍 거대한 코브라가 반짝이는 돌을 보고 눈이 뒤집혀 절벽 아래로 뛰어내립니다!")
                time.sleep(1)
                print("쿵! ... 조용해졌습니다. 다리가 안전해졌습니다.")
                
                self.state.flags["snake_cleared"] = True
                self.state.add_score(30)
                self.state.inventory.remove("MAGIC STONE")
                
                new_desc = "거대한 협곡을 가로지르는 낡은 다리입니다. 뱀은 사라졌고, 건너편 마을로 갈 수 있습니다."
                self.db.update_room_description("serpent_crossing", new_desc)
                return
        
        print("\n그렇게 할 수 없습니다.")

    def _handle_drink(self, noun: str):
        if self.state.current_room_id == "oasis":
            print("\n💧 오아시스의 맑은 물을 벌컥벌컥 마십니다.")
            print("갈증이 해소되고 기운이 납니다! (Food +20)")
            self.state.food = min(100, self.state.food + 20)
        else:
            print("\n여기에는 마실 물이 없습니다. (모래를 씹으시게요?)")

    def render(self):
        print(f"\nScore: {self.state.score} | Gold: {self.state.gold} | Food: {self.state.food}")
        print("-" * 60)
        
        room = self.db.get_room(self.state.current_room_id)
        if room:
            print(f"[{room.name}]")
            print(room.description)
        else:
            print("🚫 오류: 방 정보를 불러올 수 없습니다.")
        print("-" * 60)
