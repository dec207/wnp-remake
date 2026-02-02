# 🧪 Test Plan: Project WNP

이 문서는 'The Wizard and the Princess' 리메이크 프로젝트의 품질 보증(QA)을 위한 단위 테스트 전략을 정의합니다.

## 1. 테스트 프레임워크
- **Engine**: `unittest` (Python 표준 라이브러리) 또는 `pytest`
- **Coverage**: 핵심 로직(이동, 아이템 사용, 파싱) 100% 커버리지 목표

## 2. 테스트 범위 (Scope)

### A. 단위 테스트 (Unit Tests)
개별 모듈의 기능이 정확히 동작하는지 검증합니다.
- **`src.parser`**:
  - 정상 입력: "GO NORTH" -> `("GO", "NORTH")`
  - 불용어 처리: "GO TO THE NORTH" -> `("GO", "NORTH")`
  - 예외 입력: 빈 문자열, 특수문자 등 처리 확인
- **`src.models`**:
  - `GameState`: 점수 추가, Food 감소 로직 검증

### B. 통합 테스트 (Integration Tests)
여러 모듈이 결합되어 시나리오대로 동작하는지 검증합니다.
- **게임 엔진 로직 (`src.engine`)**:
  - **이동 (Movement)**:
    - 연결된 방으로 이동 시 `current_room_id` 변경 확인
    - 갈증 시스템: 사막 지역 이동 시 `food` 감소량(2) 확인
    - 벽 충돌: 연결되지 않은 방향 이동 시 제자리 유지 확인
  - **아이템 사용 (Interaction)**:
    - **Scenario 01 (Wizard)**: `THROW POD` 시 마법사 처치 플래그(`wizard_defeated`) 활성화 확인
    - **Scenario 02 (Snake)**: `THROW STONE` 시 뱀 처치 플래그(`snake_cleared`) 및 이동 가능 여부 확인
  - **세이브/로드**:
    - 현재 상태 저장 -> 게임 재시작 -> 로드 시 데이터 일치 여부 확인

## 3. 자동화 전략
- **Pre-commit Check**: 커밋 전 모든 단위 테스트가 통과해야 함.
- **Script**: `./run_tests.sh` 명령어로 전체 테스트 스위트 실행.
