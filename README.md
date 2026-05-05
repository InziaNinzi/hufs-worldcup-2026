# World Cup Head Soccer (Pygame)

간단한 1:1 헤드사커 스타일 축구 게임입니다.  
플레이어 2명이 점프와 이동으로 공을 밀어 넣어 점수를 올립니다.

## 실행 방법

1. 가상환경 생성/활성화

```bash
python -m venv venv
```

- Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

2. 의존성 설치

```bash
pip install -r requirements.txt
```

3. 게임 실행

```bash
python main.py
```

## 폴더 구조

```text
worldcup_game/
├─ assets/              # 게임 리소스(선택). 이미지가 없으면 도형으로 자동 대체
├─ src/
│  ├─ __init__.py
│  ├─ constants.py      # 해상도, 색상, 물리값, 키 바인딩, assets 경로 상수
│  ├─ player.py         # Player 클래스
│  └─ ball.py           # Ball 클래스
├─ main.py              # 게임 실행 엔트리포인트
├─ requirements.txt
└─ .gitignore
```

## 팀 컨벤션

- **브랜치 전략**: 기능/수정 단위로 브랜치를 분리합니다.
  - 예: `feature/kick-effect`, `fix/collision-bug`
- **PEP 8 네이밍 규칙 준수**: 
  - **Class**: `PascalCase` (예: `Player`, `Ball`)
  - **Variable / Function / Method**: `snake_case` (예: `is_jumping`, `move_player()`)
  - **Constant**: `UPPER_SNAKE_CASE` (예: `GROUND_Y`, `BALL_GRAVITY`)
- **인코딩**: 모든 소스 코드 및 주석은 `UTF-8` 형식을 사용합니다.

- **커밋 메시지 규칙 (Conventional Commits)**:
  - `feat`: 새로운 기능 추가
  - `fix`: 버그 수정
  - `docs`: 문서 수정 (README, 주석 등)
  - `refactor`: 코드 리팩토링 (기능 변화 없는 구조 변경)[cite: 1]
  - `chore`: 빌드 업무, 패키지 매니저 설정, 로그 삭제 등
  - **양식**: `태그: 요약 설명` (예: `feat: add player jump logic`)[cite: 1]
