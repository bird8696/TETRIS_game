
```markdown
# 🎮 테트리스 클래식 (Tetris Classic)

`Pygame`으로 제작된 심플하고 컬러풀한 테트리스 게임입니다.  
고스트 블록, 홀드 기능, 다음 블록 미리보기, 속도 조절 등의 기능이 포함되어 있어  
재미있고 쉽게 커스터마이징할 수 있습니다!

---

## 🧩 주요 기능

- ✅ 고전 테트리스 게임 플레이
- 👻 고스트 블록 표시
- 🌀 블록 회전 (시계방향 / 반시계방향)
- 🟪 홀드 기능 (`C` 키)
- ⏭️ 다음 블록 미리보기
- ⚙️ 게임 속도 조절 가능
- 🎛️ 메뉴 및 설정 화면 포함
- 🧱 격자에 은은한 테두리 표시

---

## ⌨️ 조작 방법

| 키보드 키      | 동작                          |
|---------------|-------------------------------|
| ← / →         | 좌/우 이동                     |
| ↓             | 아래로 이동 (소프트 드롭)       |
| SPACE         | 즉시 바닥으로 드롭 (하드 드롭)  |
| X             | 시계방향 회전                  | 
| Z             | 반시계방향 회전                |
| C             | 블록 홀드                     |

---

## 🛠️ 설치 및 실행 방법 (Anaconda 가상환경 사용)

### 1. 아나콘다 가상환경 생성 및 활성화

```bash
conda create -n tetris-env python=3.11
conda activate tetris-env
```

### 2. Pygame 설치

```bash
pip install pygame
```

> 💡 `conda-forge`를 통해 설치할 수도 있습니다:
> ```bash
> conda install -c conda-forge pygame
> ```

### 3. 게임 실행

GitHub에서 프로젝트를 클론한 뒤 실행합니다:

```bash
git clone https://github.com/yourusername/tetris-classic.git
cd tetris-classic
python tetris.py
```

---

## ⚙️ 설정 화면

- 게임 속도를 1~10 사이에서 조절할 수 있습니다.
- "Back to Menu" 버튼을 눌러 메인 메뉴로 돌아갈 수 있습니다.

---

## 📁 프로젝트 구조

```
tetris-classic/
├── tetris.py         # 메인 게임 코드
├── README.md         # 이 파일
└── (필요 시 assets/)  # 이미지, 사운드 등 리소스 폴더
```

---

## 🚀 향후 추가 예정 기능

- 🎵 배경음악 및 효과음 추가
- 🏆 최고 점수 저장 기능
- 🌀 7-개 블록 고정 랜덤 알고리즘 (7-bag)
- 🎮 게임패드 조작 지원
- 🖥️ 전체화면 모드 전환

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스로 제공됩니다.  
자유롭게 사용, 수정, 배포하실 수 있습니다.

---

## 🙌 제작 정보

- 제작: [Pygame](https://www.pygame.org/) 기반
- 영감: 클래식 테트리스 게임에서 착안

