# System Architecture

## 1. Directory Structure (디렉토리 구조)

```text
wnp/
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry Point (게임 루프)
│   ├── engine.py        # Game Engine (상태 관리, 로직 연결)
│   ├── parser.py        # Command Parser (명령어 해석)
│   ├── models.py        # Data Classes (GameState, Room, Item)
│   └── data_loader.py   # JSON 데이터 로더
├── data/
│   ├── rooms.json       # 맵 데이터
│   └── items.json       # 아이템 데이터
├── docs/                # 문서
└── tests/               # 단위 테스트
```

## 2. Core Modules (핵심 모듈)

### A. GameState (Singleton)
게임의 현재 상태를 저장하는 중앙 저장소입니다.
- **속성**: `score`, `gold`, `food`, `inventory`, `current_room_id`, `flags`(이벤트 플래그)
- **역할**: 게임 세션 동안 유지되어야 할 모든 데이터 관리.

### B. Parser
사용자의 자연어 입력을 게임이 이해할 수 있는 `Action`으로 변환합니다.
- **Input**: "Throw the thermal pod at the wizard"
- **Process**: 
  1. 정규화 (소문자 변환, 불필요한 단어 제거)
  2. 토큰화 (Verb: `THROW`, Noun: `THERMAL POD`, Target: `WIZARD`)
  3. 유효성 검사
- **Output**: `('THROW', 'thermal pod', 'wizard')` 튜플 반환.

### C. Game Engine
Parser로부터 받은 명령을 실행하고, GameState와 World Data를 업데이트합니다.
- **이동 처리**: 현재 방의 `exits` 확인 -> `current_room_id` 변경 -> `food` 감소.
- **상호작용**: 아이템 사용 조건 확인 -> `flags` 업데이트 -> 결과 메시지 반환.

## 3. Data Flow (데이터 흐름)

1. **User Input** (`STDIN`)
   ↓
2. **Parser**: 텍스트 분석 및 의도 파악
   ↓
3. **Engine**: 로직 수행 (조건 체크, 상태 변경)
   ↓ 
   - *Update* `GameState` (Inventory, Flags)
   - *Query* `WorldData` (Room Info)
   ↓
4. **Output**: 결과 텍스트 출력 (`STDOUT`)
