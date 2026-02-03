import os
from flask import Flask, render_template, request, jsonify
from .engine import GameEngine
from .parser import parse_input

app = Flask(__name__, template_folder='../templates')

# 싱글 세션 게임 엔진 초기화 (웹 데모용)
game_engine = GameEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    user_input = data.get('command', '')
    
    # 1. 파싱 및 실행
    verb, noun = parse_input(user_input)
    if verb:
        game_engine.process_command(verb, noun)
    
    # 2. 현재 상태 정보 수집
    state = game_engine.state
    room = game_engine.db.get_room(state.current_room_id)
    monster = game_engine.db.get_monster(state.current_room_id)
    
    status_text = f"SCORE: {state.score} | GOLD: {state.gold} | FOOD: {state.food} | HP: {state.hp}"
    
    return jsonify({
        "status": status_text,
        "room_name": room.name if room else "Unknown",
        "description": room.description if room else "오류: 방 정보를 찾을 수 없습니다.",
        "monster": monster['description'] if monster else None
    })

if __name__ == '__main__':
    # 리플릿은 보통 8080 포트를 사용합니다.
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Replit deployment (when run as module)
if __name__.startswith('src.'):
    port = int(os.environ.get('PORT', 8080))
    # We use a separate thread or just run it if it's the main entry
    # Since this is the 'run' command, it should block.
    app.run(host='0.0.0.0', port=port)
