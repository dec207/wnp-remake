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

## 🚧 Phase 2: 데이터 중심 설계 (Data-Driven) - [다음 목표]
하드코딩된 데이터를 DB로 이관하여 확장성을 확보하는 단계입니다.
- [ ] **SQLite 도입**:
  - 스키마 설계 (`rooms`, `items`, `monsters` 테이블)
  - `src/db.py` 모듈 구현 (데이터 조회/저장 로직)
- [ ] **데이터 마이그레이션**:
  - 기존 딕셔너리 데이터를 SQLite DB로 변환
- [ ] **상태 저장 시스템**:
  - `SAVE GAME` / `LOAD GAME` 기능 구현 (Player State DB 저장)

---

## 🔮 Phase 3: 콘텐츠 확장 (Content Expansion)
원작의 방대한 세계관을 구현합니다. (약 50+ Rooms)
- [ ] **Zone 1: The Desert (사막)**
  - 이동 시 갈증(Thirst) 시스템 구현
  - 미로 알고리즘 적용
- [ ] **Zone 2: Serpent's Crossing (마을)**
  - 상점 및 NPC 대화 시스템
- [ ] **Zone 3: The Castle (성)**
  - 복잡한 퍼즐 및 키 아이템 로직 구현

---

## ⚔️ Phase 4: 시스템 고도화 (Advanced Systems)
단순 텍스트 게임을 넘어선 깊이 있는 플레이를 제공합니다.
- [ ] **전투 시스템**: 턴제 전투 로직 (Attack/Defend)
- [ ] **고급 파서**: 복합 명령 처리 ("GET KEY AND OPEN DOOR")
- [ ] **사운드/TTS**: 중요 이벤트 시 음성 출력 (ElevenLabs 연동 등)

---

## 📦 Phase 5: 배포 및 완성 (Release)
- [ ] **패키징**: `PyInstaller`를 이용한 실행 파일(.exe/.app) 생성
- [ ] **최종 테스트**: 전체 시나리오 QA
- [ ] **배포**: GitHub Release 등록

---
*Last Updated: 2026-02-03*
