import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from .engine import GameEngine
from .parser import parse_input

# 리플릿 배포(Health Check)를 위한 간단한 웹 서버
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"WNP Game is running!")
    def log_message(self, format, *args): return # 로그 출력 억제

def run_health_check_server():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

def main():
    # 웹 서버 백그라운드 실행
    threading.Thread(target=run_health_check_server, daemon=True).start()

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
