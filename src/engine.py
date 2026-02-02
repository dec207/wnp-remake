import time
import dataclasses
import random
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

        monster = self.db.get_monster(self.state.current_room_id)
        if monster and verb not in ["ATTACK", "KILL", "FIGHT", "RUN", "FLEE", "INV", "I"]:
            print(f"\n🚫 {monster['name']}가 앞을 막고 있어 다른 행동을 할 수 없습니다! (싸우거나 도망치세요!)")
            return

        if verb in ["SAVE"]:
            self._handle_save()
        elif verb in ["LOAD", "RESTORE"]:
            self._handle_load()
        elif verb in ["GO", "WALK", "MOVE", "RUN", "FLEE"]:
            if verb in ["RUN", "FLEE"] and monster:
                self._handle_flee(monster)
            else:
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
        elif verb in ["BUY", "PURCHASE"]:
            self._handle_buy(noun)
        elif verb in ["ATTACK", "KILL", "FIGHT"]:
            self._handle_attack(noun)
        elif verb in ["PLAY", "BLOW"]:
            self._handle_play(noun)
        else:
            print("\n🤔 무슨 말인지 모르겠습니다.")

    def _handle_attack(self, noun: str):
        monster = self.db.get_monster(self.state.current_room_id)
        if not monster:
            print("\n여기에는 싸울 상대가 없습니다.")
            return

        player_dmg = random.randint(5, 15)
        if "SWORD" in self.state.inventory:
            player_dmg += 10
        
        monster["hp"] -= player_dmg
        print(f"\n⚔️ 당신은 {monster['name']}을(를) 공격하여 {player_dmg}의 피해를 입혔습니다!")

        if monster["hp"] <= 0:
            print(f"💥 {monster['name']}이(가) 쓰러졌습니다! 승리!")
            self.db.delete_monster(self.state.current_room_id)
            self.state.add_score(20)
            gold_drop = random.randint(10, 30)
            self.state.gold += gold_drop
            print(f"💰 전리품으로 {gold_drop} 골드를 획득했습니다. (현재 Gold: {self.state.gold})")
            return
        
        # HP 감소 DB 반영
        self.db.update_monster_hp(self.state.current_room_id, monster["hp"])

        print(f"😡 {monster['name']}이(가) 반격합니다!")
        time.sleep(0.5)
        monster_dmg = monster["damage"]
        self.state.hp -= monster_dmg
        print(f"🩸 당신은 {monster_dmg}의 피해를 입었습니다. (남은 HP: {self.state.hp})")

        if self.state.hp <= 0:
            print("\n💀 당신은 치명상을 입고 쓰러졌습니다... GAME OVER")
            self.state.is_running = False

    def _handle_flee(self, monster):
        if random.random() < 0.5:
            print("\n💨 잽싸게 도망쳤습니다!")
            self._handle_move("NORTH")
        else:
            print("\n🚫 도망치지 못했습니다! 몬스터에게 등을 보였습니다.")
            dmg = monster["damage"]
            self.state.hp -= dmg
            print(f"🩸 {dmg}의 피해를 입었습니다! (남은 HP: {self.state.hp})")

    def _handle_play(self, noun: str):
        if noun == "FLUTE" and "FLUTE" in self.state.inventory:
            if self.state.current_room_id == "castle_gate" and not self.state.flags.get("bridge_lowered"):
                print("\n🎵 피리를 불자 맑고 고운 소리가 울려 퍼집니다.")
                time.sleep(1)
                print("졸고 있던 경비병이 깜짝 놀라 깹니다.")
                print("'아이고, 손님이 오셨군!' 끼기긱... 쿵! 도개교가 내려옵니다.")
                
                self.state.flags["bridge_lowered"] = True
                self.state.add_score(20)
                self.db.update_room_description("castle_gate", "도개교가 내려와 있어 성 안으로 들어갈 수 있습니다.")
                return
            else:
                print("\n🎵 피리를 불었습니다. 듣기 좋은 소리네요.")
        else:
            print("\n연주할 악기가 없습니다.")

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

    def _handle_buy(self, noun: str):
        if self.state.current_room_id == "general_store":
            if not noun:
                print("\n무엇을 사고 싶으신가요? (예: BUY APPLE)")
                return
            item = noun
            price = 5 if item == "APPLE" else 50 if item == "FLUTE" else 0
            if price == 0:
                print(f"\n주인장: '{item}'? 그런 건 안 파네.")
                return
            if self.state.gold >= price:
                self.state.gold -= price
                if item == "APPLE":
                    self.state.food = min(100, self.state.food + 10)
                    print(f"\n🍎 사과를 냠냠. (Food +10, Gold -{price})")
                else:
                    self.state.inventory.append(item)
                    print(f"\n💰 {item} 구매 완료! (Gold -{price})")
            else:
                print(f"\n주인장: 돈이 부족해! {price}G야.")
        else:
            print("\n여기선 살 수 없어요.")

    def _handle_get(self, noun: str):
        if self.state.current_room_id == "oasis" and noun in ["STONE", "MAGIC STONE"]:
            if "MAGIC STONE" not in self.state.inventory:
                print("\n✨ 마법의 돌 획득!")
                self.state.inventory.append("MAGIC STONE")
            else:
                print("\n이미 있어요.")
        else:
            print("\n없어요.")

    def _handle_drink(self, noun: str):
        if self.state.current_room_id == "oasis":
            print("\n💧 꿀꺽꿀꺽. (Food +20)")
            self.state.food = min(100, self.state.food + 20)
        else:
            print("\n물 없음.")

    def _handle_item_use(self, verb: str, noun: str):
        current_room = self.state.current_room_id
        if current_room == "cavern" and not self.state.flags.get("wizard_defeated"):
            if noun in ["POD", "THERMAL POD"] and "THERMAL POD" in self.state.inventory:
                print("\n🔥 Thermal Pod 투척! 마법사 처치!")
                self.state.flags["wizard_defeated"] = True
                self.state.add_score(50)
                self.state.gold += 100
                self.state.inventory.remove("THERMAL POD")
                self.db.update_room_description("cavern", "마법사가 사라진 동굴.")
                return
        if current_room == "serpent_crossing" and not self.state.flags.get("snake_cleared"):
            if noun in ["STONE", "MAGIC STONE"] and "MAGIC STONE" in self.state.inventory:
                print("\n💎 돌 던짐! 뱀 추락!")
                self.state.flags["snake_cleared"] = True
                self.state.add_score(30)
                self.state.inventory.remove("MAGIC STONE")
                self.db.update_room_description("serpent_crossing", "뱀이 없는 다리.")
                return
        print("\n불가능.")

    def _handle_move(self, direction: str):
        if not direction: return
        current_room = self.db.get_room(self.state.current_room_id)
        next_room_id = None

        if self.state.current_room_id == "desert_maze_1":
            if direction == "EAST": next_room_id = "oasis"; print("\n✨ 오아시스!")
            elif direction == "NORTH": next_room_id = "desert_path"
            else: next_room_id = "desert_maze_1"; print("\n🌪️ 미로 제자리...")
            
        elif self.state.current_room_id == "serpent_crossing" and direction == "EAST":
            if self.state.flags.get("snake_cleared"): next_room_id = "town_entry"
            else: print("\n🐍 뱀이 막고 있음!"); return
            
        elif self.state.current_room_id == "castle_gate" and direction == "NORTH":
            if self.state.flags.get("bridge_lowered"): next_room_id = "throne_room"
            else: print("\n🌉 다리가 올라가 있어 건널 수 없습니다. 경비병을 깨워야 할 것 같은데..."); return

        elif direction in current_room.exits:
            next_room_id = current_room.exits[direction]
        
        if next_room_id:
            # 엔딩 체크
            if next_room_id == "throne_room":
                self._trigger_ending()
                return

            self.state.current_room_id = next_room_id
            cost = 2 if "desert" in next_room_id or "oasis" in next_room_id else 1
            self.state.decrease_food(cost)
            print(f"\n🏃 {direction} 이동...")
        else:
            print("\n🚫 못 감.")

    def _trigger_ending(self):
        """게임 엔딩 처리"""
        print("\n" + "="*50)
        print("🎉 축하합니다! 성에 도착했습니다!")
        print("="*50)
        time.sleep(1)
        print("왕: '오, 용감한 모험가여! 내 딸을 구하기 위해 여기까지 오다니!'")
        print("공주: '정말 고마워요!'")
        print("\n당신은 사악한 마법사를 물리치고, 뱀을 따돌리고, 사막을 건너 공주를 구했습니다.")
        
        final_score = self.state.score + 100
        print(f"\n🏆 최종 점수: {final_score} / 200")
        print(f"💰 남은 골드: {self.state.gold}")
        print("\n=== THE END ===")
        self.state.is_running = False

    def render(self):
        print(f"\nScore: {self.state.score} | Gold: {self.state.gold} | Food: {self.state.food} | HP: {self.state.hp}")
        print("-" * 60)
        
        room = self.db.get_room(self.state.current_room_id)
        if room:
            print(f"[{room.name}]")
            print(room.description)
            
            monster = self.db.get_monster(self.state.current_room_id)
            if monster:
                print(f"\n⚠️  {monster['description']}")
                print(f"   [{monster['name']}] HP: {monster['hp']} | Damage: {monster['damage']}")
        else:
            print("🚫 오류: 방 데이터 없음.")
        print("-" * 60)
