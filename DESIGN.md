# The Wizard and the Princess - Python Remake

## 1. 프로젝트 개요
1980년대 고전 어드벤처 게임 'The Wizard and the Princess'를 현대적인 Python 텍스트 어드벤처(MUD) 엔진으로 재구현하는 프로젝트입니다.

## 2. 기술 스택
- **Language**: Python 3.x
- **Architecture**: 데이터 주도(Data-Driven) 설계 (맵, 아이템 데이터를 코드와 분리)
- **Interface**: CLI (Command Line Interface)

## 3. 핵심 시스템 설계
### A. GameState (상태 관리)
- 플레이어의 모든 상태를 싱글톤 또는 인스턴스로 관리.
- **속성**:
  - `score` (int): 현재 점수 (0~100)
  - `gold` (int): 소지금
  - `food` (int): 체력/이동력 (이동 시 감소)
  - `inventory` (list): 소지 아이템 목록
  - `current_room` (string): 현재 위치 ID
  - `flags` (dict): 게임 내 이벤트 상태 (예: 'wizard_defeated': True)

### B. Parser (명령어 해석기)
- 자연어 입력을 `[동사] + [명사]` 구조로 정규화.
- 동의어 처리 (Synonyms):
  - GO: WALK, MOVE, RUN
  - GET: TAKE, GRAB, PICKUP
  - LOOK: L, EXAMINE, X

### C. World Data (맵 구조)
- JSON 또는 Dictionary 형태로 방 데이터를 관리하여 확장성 확보.
- 각 방(Room) 구조:
  ```json
  "room_id": {
      "name": "방 이름",
      "description": "방 설명 텍스트",
      "exits": {"north": "other_room_id"},
      "items": ["item_id"],
      "events": "trigger_function_name"
  }
  ```

## 4. 개발 로드맵
1. **프로토타입 (완료)**: 핵심 파서 및 이동 로직 구현.
2. **구조 개선 (진행 중)**: 단일 파일에서 모듈화된 구조로 분리.
3. **데이터 분리**: 맵/아이템 데이터를 외부 파일(JSON)로 분리.
4. **콘텐츠 확장**: 원작의 모든 맵과 퍼즐 구현.
