import sys
from .engine import GameEngine
from .parser import parse_input

def main():
    print("\n" + "="*50)
    print(" 🏰 The Wizard and the Princess (Python Remake)")
    print("="*50)
    
    engine = GameEngine()

    while engine.state.is_running:
        # 1. 화면 출력
        engine.render()

        # 2. 입력 대기
        try:
            user_input = input("\n명령을 입력하세요 >> ")
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            break

        # 3. 파싱
        verb, noun = parse_input(user_input)
        
        if not verb:
            continue

        # 4. 로직 실행
        engine.process_command(verb, noun)

if __name__ == "__main__":
    main()
