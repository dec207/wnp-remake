# Project WNP: 작업 목록 (Backlog)

## 🚀 1. 인프라 및 구조 (Infrastructure)
- [x] 초기 프로토타입 작성 (`wnp_game.py`)
- [ ] **프로젝트 폴더 구조화** (현재 단일 파일 → 패키지 구조)
  - `src/main.py`: 엔트리 포인트
  - `src/engine/`: 게임 엔진 코어 (Parser, State)
  - `src/data/`: 맵, 아이템 데이터
- [ ] **Git 초기화 및 .gitignore 설정**

## 🛠 2. 엔진 고도화 (Engine)
- [ ] **데이터 로더 구현**: Python 딕셔너리로 하드코딩된 데이터를 JSON 파일로 분리.
- [ ] **고급 파서 구현**: 전치사 처리 (예: "HIT GOBLIN WITH SWORD") 기능 추가.
- [ ] **세이브/로드 시스템**: `pickle` 또는 `json`을 이용한 게임 상태 저장.

## 🎨 3. 콘텐츠 구현 (Content)
- [ ] **Serpent's Crossing**: 뱀이 길을 막고 있는 초기 맵 구현.
- [ ] **Desert**: 사막 미로 로직 (물 없이 이동 시 사망) 구현.
- [ ] **Castle**: 최종 성 진입 로직.

## 🐛 버그 수정 (Fixes)
- [ ] 이동 시 방향이 잘못된 경우의 에러 메시지 구체화.
