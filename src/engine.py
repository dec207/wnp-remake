import time
from typing import Dict
from .models import GameState, Room

# 초기 맵 데이터 (추후 JSON 로딩 방식으로 변경 예정)
WORLD_MAP: Dict[str, Room] = {
    "cavern": Room(
        id="cavern",
        name="사악한 마법사의 동굴 (Cavern of the Evil Wizard)",
        description="당신은 사악한 마법사의 동굴에 서 있습니다.\n사방에 얼음 난쟁이들의 시체가 널브러져 있어 음산한 분위기를 자아냅니다.\n정면에는 사악한 마법사가 당신을 노려보고 있습니다!",
        exits={"SOUTH": "tunnel"}
    ),
    "tunnel": Room(
        id="tunnel",
        name="어두운 터널",
        description="동굴 밖으로 이어지는 어두운 터널입니다. 북쪽에서 찬 바람이 불어옵니다.",
        exits={"NORTH": "cavern"}
    )
}

class GameEngine:
    def __init__(self):
        self.state = GameState()
        # 테스트용 초기 아이템 지급
        self.state.inventory.append("THERMAL POD")

    def process_command(self, verb: str, noun: str):
        if verb in ["QUIT", "EXIT"]:
            self.state.is_running = False
            print("\n게임을 종료합니다. 안녕히 가세요!")
            return

        if verb in ["GO", "WALK", "MOVE", "RUN"]:
            self._handle_move(noun)
        elif verb in ["N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"]:
            # 방향만 입력한 경우 처리 (예: "N")
            direction_map = {"N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST"}
            full_dir = direction_map.get(verb, verb)
            self._handle_move(full_dir)
        elif verb in ["INV", "INVENTORY", "I"]:
            print(f"\n🎒 인벤토리: {', '.join(self.state.inventory) if self.state.inventory else '비어있음'}")
        elif verb in ["THROW", "MELT", "USE"]:
            self._handle_item_use(verb, noun)
        else:
            print("\n🤔 무슨 말인지 모르겠습니다.")

    def _handle_move(self, direction: str):
        if not direction:
            print("\n어디로 갈까요?")
            return
            
        current_room = WORLD_MAP[self.state.current_room_id]
        if direction in current_room.exits:
            next_room_id = current_room.exits[direction]
            self.state.current_room_id = next_room_id
            self.state.decrease_food()
            print(f"\n🏃 {direction} 방향으로 이동합니다...")
        else:
            print("\n🚫 그쪽으로는 갈 수 없습니다.")

    def _handle_item_use(self, verb: str, noun: str):
        # 마법사 처치 이벤트
        if self.state.current_room_id == "cavern" and not self.state.flags.get("wizard_defeated"):
            if noun in ["POD", "THERMAL POD"] and "THERMAL POD" in self.state.inventory:
                print("\n🔥 당신은 Thermal Pod를 사악한 마법사에게 던졌습니다!")
                time.sleep(1)
                print("💥 팟이 폭발하며 강렬한 열기가 동굴을 채웁니다!")
                time.sleep(1)
                print("😱 마법사는 비명을 지르며 수증기가 되어 사라졌습니다.")
                
                self.state.flags["wizard_defeated"] = True
                self.state.add_score(50)
                self.state.inventory.remove("THERMAL POD")
                
                # 방 설명 업데이트
                WORLD_MAP["cavern"].description = "사악한 마법사의 동굴입니다. 이제 마법사는 없고, 바닥에 물웅덩이만 남아있습니다."
                return
        
        print("\n그렇게 할 수 없습니다.")

    def render(self):
        """현재 상태와 방 정보를 화면에 출력"""
        print(f"\nScore: {self.state.score} | Gold: {self.state.gold} | Food: {self.state.food}")
        print("-" * 60)
        
        room = WORLD_MAP[self.state.current_room_id]
        print(f"[{room.name}]")
        print(room.description)
        print("-" * 60)
