# 🗺️ Project WNP: Development Roadmap

이 로드맵은 'The Wizard and the Princess' 리메이크 프로젝트의 전체 진행 과정을 단계별로 정의합니다.

## ✅ Phase 1: 기초 공사 (Foundation) - [완료]
개발 환경 구축 및 핵심 엔진 프로토타이핑 단계입니다.
- [x] **프로젝트 구조화**: `src/` 모듈 분리 (Engine, Parser, Models)
- [x] **문서화**: `README.md`, `ARCHITECTURE.md`, `HEARTBEAT.md` 작성
- [x] **프로토타입 구현**:
  - 기본 파서 (Verb-Noun 구조)
  - 인메모리 상태 관리 (GameState)
  - 시나리오 01 구현 (마법사 동굴 이벤트)

---

## ✅ Phase 2: 데이터 중심 설계 (Data-Driven) - [완료]
하드코딩된 데이터를 DB로 이관하여 확장성을 확보하는 단계입니다.
- [x] **SQLite 도입**:
  - `src/database.py` 구현 및 `wnp.db` 생성
  - `rooms`, `saves` 테이블 스키마 설계
- [x] **엔진 연동**:
  - `engine.py`가 DB에서 실시간으로 방 정보를 조회하도록 수정
- [x] **상태 저장 시스템**:
  - `SAVE` / `LOAD` 명령어 구현
  - `GameState` 객체의 JSON 직렬화/역직렬화 구현

---

## 🚧 Phase 3: 콘텐츠 확장 (Content Expansion) - [진행 중]
원작의 방대한 세계관을 구현합니다.

### 3-1. Zone 1: The Desert (사막) - [부분 완료]
- [x] **기본 맵 구현**: 사막 입구, 끝없는 사막, 오아시스 추가
- [x] **환경 시스템**: 갈증(Thirst) 및 물 마시기(`DRINK`) 구현
- [ ] **사막 미로 알고리즘**:
  - 특정 패턴(예: N, W, S)으로 이동하지 않으면 제자리로 돌아오는 로직
  - 랜덤 인카운터(전갈 등) 발생 확률 추가

### 3-2. Zone 2: Serpent's Crossing (마을)
- [ ] **다리 건너기 이벤트**:
  - 거대한 뱀(Serpent)이 길을 막고 있음
  - 아이템(`FLUTE` 등)을 사용하여 뱀을 잠재우는 로직
- [ ] **마을 진입**:
  - 상점(Shop) 시스템 구현 (골드로 아이템 구매)
  - NPC 대화 (`TALK TO <NPC>`)

### 3-3. Zone 3: The Castle (성)
- [ ] **성문 퍼즐**: 다리(Drawbridge)를 내리는 메커니즘
- [ ] **내부 구조**: 감옥, 왕의 침실, 보물 창고 등 20개 이상의 방 데이터 추가

---

## ⚔️ Phase 4: 시스템 고도화 (Advanced Systems)
단순 텍스트 게임을 넘어선 깊이 있는 플레이를 제공합니다.

### 4-1. 전투 시스템 (Combat)
- [ ] **Monster 클래스 설계**: HP, 공격력, 드랍 아이템 속성 추가
- [ ] **전투 루프**: `ATTACK <ENEMY>` 입력 시 턴제 전투 진행
- [ ] **무기 시스템**: 맨손 vs 단검 vs 검 데미지 차등 적용

### 4-2. 고급 파서 (Advanced Parser)
- [ ] **복합 명령어 처리**:
  - 전치사 지원: `HIT SNAKE WITH STICK`
  - 다중 명령: `GET KEY AND UNLOCK DOOR`
- [ ] **동의어 사전(Thesaurus) 확장**: DB에 동의어 테이블 추가하여 유연한 입력 처리

---

## 📦 Phase 5: 배포 및 완성 (Release)
- [ ] **패키징**: `PyInstaller`를 이용한 실행 파일(.exe/.app) 생성
- [ ] **최종 테스트**: 전체 시나리오 QA (End-to-End Test)
- [ ] **배포**: GitHub Release 등록

---
*Last Updated: 2026-02-03*
