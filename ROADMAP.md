# 🗺️ Project WNP: Development Roadmap

이 로드맵은 'The Wizard and the Princess' 리메이크 프로젝트의 전체 진행 과정을 단계별로 정의합니다.

## ✅ Phase 1: 기초 공사 (Foundation) - [완료]
- [x] **프로젝트 구조화**: `src/` 모듈 분리
- [x] **문서화**: `README.md`, `ARCHITECTURE.md` 작성
- [x] **프로토타입 구현**: 파서 및 기본 엔진 구현

---

## ✅ Phase 2: 데이터 중심 설계 (Data-Driven) - [완료]
- [x] **SQLite 도입**: `wnp.db` 구축 및 스키마 설계
- [x] **엔진 연동**: DB 기반 실시간 데이터 조회
- [x] **상태 저장 시스템**: `SAVE` / `LOAD` 구현

---

## ✅ Phase 3: 콘텐츠 확장 (Content Expansion) - [완료]
- [x] **Zone 1: The Desert**: 사막 미로, 갈증 시스템, 오아시스 구현
- [x] **Zone 2: Serpent's Crossing**: 뱀 이벤트, 마을 상점(Shop) 구현
- [x] **Zone 3: The Castle**: 성문 퍼즐(피리), 알현실 엔딩 구현

---

## ✅ Phase 4: 시스템 고도화 (Advanced Systems) - [완료]
- [x] **전투 시스템**: 
  - HP/Gold/Damage 스탯 도입
  - 몬스터 AI (반격) 및 전리품 시스템 구현
  - `ATTACK`, `RUN` 명령어 추가
- [x] **품질 보증(QA)**:
  - 단위 테스트(`test_engine.py`) 및 시나리오 테스트(`test_scenario.py`) 구축
  - CI 스크립트(`run_tests.sh`) 작성

---

## 📦 Phase 5: 배포 및 완성 (Release) - [대기 중]
- [ ] **패키징**: `PyInstaller`를 이용한 실행 파일(.exe/.app) 생성
- [ ] **최종 테스트**: 전체 시나리오 QA (End-to-End Test) ✅ 완료
- [ ] **배포**: GitHub Release 등록

---
*Last Updated: 2026-02-03 (All Core Features Completed)*
