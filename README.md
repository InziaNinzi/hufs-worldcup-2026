<<<<<<< HEAD
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

- 기능별 브랜치 사용: 기능/수정 단위로 브랜치를 분리해 작업합니다.
  - 예: `feature/kick-effect`, `fix/collision-bug`
- PEP 8 스타일 준수: 네이밍, 들여쓰기, 라인 길이 등 파이썬 스타일 가이드를 지킵니다.
=======
# hufs-worldcup-2026
2026 북중미 월드컵 1대1 축구 게임 (Python/Pygame)
>>>>>>> 9d12236c48a9ab180250dae5b7ddf2aa6f070b98
