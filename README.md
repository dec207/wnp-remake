# 🏰 The Wizard and the Princess (Python Remake)

> *"사악한 마법사에게 납치된 공주를 구하고 왕국의 평화를 되찾으세요!"*

1980년대 전설적인 텍스트 어드벤처 게임을 현대적인 **Python** 기술로 재탄생시켰습니다.
자연어 명령어로 캐릭터를 조종하고, 퍼즐을 풀고, 몬스터와 싸워 엔딩을 확인하세요.

---

## 🎮 게임 특징 (Features)

- **📝 자연어 파싱**: `GO NORTH`, `THROW STONE`, `ATTACK THIEF` 등 직관적인 영어 명령어를 이해합니다.
- **⚔️ 턴제 전투 시스템**: 사막의 전갈, 마을의 좀도둑과 싸워 레벨업하고 골드를 얻으세요.
- **💾 실시간 상태 관리**: 언제든지 게임을 **저장(SAVE)**하고 **불러오기(LOAD)** 할 수 있습니다.
- **🌎 확장된 세계관**:
  - **Zone 1**: 사악한 마법사의 동굴
  - **Zone 2**: 끝없는 사막의 미로와 오아시스
  - **Zone 3**: 거대한 뱀이 지키는 마을
  - **Zone 4**: 왕이 기다리는 성(Castle)

---

## 🚀 설치 및 실행 방법 (Installation)

### 요구 사항 (Prerequisites)
- **Python 3.8** 이상

### 1. 게임 다운로드
터미널(Terminal)을 열고 아래 명령어를 입력하세요.

```bash
git clone https://github.com/your-repo/wnp-remake.git
cd wnp-remake
```

### 2. 게임 실행
별도의 라이브러리 설치 없이 바로 실행 가능합니다!

```bash
python3 -m src.main
```

---

## 🕹️ 플레이 가이드 (How to Play)

게임이 시작되면 상황을 설명하는 텍스트가 나옵니다.
`>>` 프롬프트에 **영어 명령어**를 입력하여 행동하세요.

### 🏃 이동 (Movement)
- **GO NORTH** (또는 `N`): 북쪽으로 이동
- **GO SOUTH** (`S`), **GO EAST** (`E`), **GO WEST** (`W`)

### 👋 행동 (Action)
- **LOOK** (`L`): 주변을 다시 살펴봅니다.
- **GET <ITEM>** (예: `GET STONE`): 아이템을 줍습니다.
- **INV** (`I`): 가방(인벤토리)을 확인합니다.
- **USE <ITEM>** (예: `USE POTION`): 아이템을 사용합니다.
- **BUY <ITEM>** (예: `BUY APPLE`): 상점에서 물건을 삽니다.
- **SAVE / LOAD**: 게임 상태를 저장하거나 불러옵니다.

### ⚔️ 전투 (Combat)
몬스터를 만나면 전투가 시작됩니다.
- **ATTACK** (`KILL`): 몬스터를 공격합니다.
- **RUN** (`FLEE`): 도망칩니다. (실패 시 피해를 입습니다!)

---

## 💡 팁 & 공략 (Hints)

<details>
<summary>🕵️ 스포일러 주의! (클릭하여 공략 보기)</summary>

1. **마법사 처치**: 시작하자마자 `THERMAL POD`를 던지세요 (`THROW POD`).
2. **사막 미로**: 발자국을 잘 보세요. `S -> E` 순서로 가면 오아시스가 나옵니다.
3. **뱀의 다리**: 오아시스에서 주운 **돌(`STONE`)**을 던져 뱀을 유인하세요.
4. **성문 열기**: 마을 상점에서 **피리(`FLUTE`)**를 사서 성문 앞에서 부세요 (`PLAY FLUTE`).
</details>

---

## 🛠️ 개발자 정보 (Developer)
- **Developed by**: 정환 & Jarvis (AI Assistant)
- **Engine**: Pure Python 3 + SQLite
- **License**: MIT License
