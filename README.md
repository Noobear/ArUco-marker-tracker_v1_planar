# ArUco 마커 추적 프로젝트 🎯

iPhone 영상에서 **ArUco 마커를 자동 감지**하고 **cm 단위의 2D 좌표로 변환**하는 Python 프로젝트입니다.

마커의 **위치, 크기, 회전 각도**를 실시간으로 추적하고 CSV 파일로 저장합니다.

```
iPhone 영상 → ArUco 마커 감지 → 픽셀 좌표 측정 → cm 단위 변환 → CSV 저장
```

---

## ⚡ 빠른 시작 (30초)

### 1️⃣ 가상환경 활성화
```bash
cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1
source venv/bin/activate
```

### 2️⃣ 스크립트 실행
```bash
# 1cm 마커 사용
python scripts/aruco_tracker_1cm.py your_video.mov result.csv

# 다른 크기 마커 사용 (예: 5cm)
python scripts/aruco_tracker_flexible.py your_video.mov result.csv --marker-size 5.0
```

### 3️⃣ 결과 확인
```bash
open result.csv  # Excel에서 열기
```

**완료!** ✅

---

## 📊 결과 파일 (result.csv)

```csv
timestamp_s  frame_number  marker_id  center_x_cm  center_y_cm  rotation_angle_deg
0.000        0             0          13.65        10.24        -2.35
0.033        1             0          13.71        10.31        -2.10
0.067        2             0          13.77        10.38        -1.85
```

**각 컬럼 설명**:
- `timestamp_s`: 비디오 시간 (초)
- `frame_number`: 프레임 번호 (0부터 시작)
- `marker_id`: ArUco 마커 ID (0~249)
- `center_x_cm`: 마커 중심 X 좌표 (cm)
- `center_y_cm`: 마커 중심 Y 좌표 (cm)
- `rotation_angle_deg`: 마커 회전 각도 (도)
- `corner_*_x/y_cm`: 마커의 4개 코너 좌표 (cm)

---

## 🚀 사용 가능한 스크립트

| 스크립트 | 설명 | 사용법 |
|---------|------|--------|
| **aruco_tracker_1cm.py** | 1cm 마커 전용 (가장 간단) | `python scripts/aruco_tracker_1cm.py video.mov result.csv` |
| **aruco_tracker_flexible.py** | 마커 크기 지정 가능 ⭐ | `python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 5.0` |
| aruco_tracker_with_video.py | 시각화 영상 생성 (고급) | `python scripts/aruco_tracker_with_video.py video.mov output.mp4 output.csv` |

---

## 🔧 마커 크기 변경

### 1cm 고정
```bash
python scripts/aruco_tracker_1cm.py video.mov result.csv
```

### 크기 지정 (2cm, 5cm, 10cm 등)
```bash
python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 2.0
python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 5.0
python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 10.0
```

---

## 📁 프로젝트 구조

```
Python_26_1/
│
├── scripts/                          # 추적 스크립트
│   ├── aruco_tracker_1cm.py          # 1cm 마커 전용
│   ├── aruco_tracker_flexible.py     # 크기 변경 가능 ⭐
│   └── aruco_tracker_with_video.py   # 시각화 영상 생성
│
├── docs/                             # 상세 가이드
│   ├── START_HERE.md                 # 30초 빠른 시작
│   ├── USAGE_GUIDE.md                # 자세한 사용법
│   ├── QUICK_START_1CM.md
│   ├── QUICK_START_USER_VIDEO.md
│   ├── SIMPLE_XY_CALIBRATION.md
│   ├── CAMERA_CALIBRATION_GUIDE.md
│   └── 3D_POSE_ESTIMATION.md
│
├── tests/                            # 테스트
│   ├── videos/                       # 테스트 영상
│   └── results/                      # 결과 예시
│
├── marker/                           # ArUco 마커 이미지 (ID 0~49)
│
├── venv/                             # Python 가상환경
├── requirements.txt                  # 패키지 목록
├── README.md                         # 이 파일
└── .gitignore
```

---

## 📋 필수 요구사항

- Python 3.7+
- OpenCV 4.0+ (`opencv-contrib-python`)
- numpy
- Mac/Linux/Windows

---

## 🔧 설치 및 환경 설정

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 가상환경 활성화 (매번 실행 전 필수)
```bash
source venv/bin/activate
```

### 3. 첫 번째 실행
```bash
python scripts/aruco_tracker_1cm.py test_video.mov test_result.csv
```

---

## 💡 사용 예시

### 예시 1: iPhone에서 촬영한 영상 분석
```bash
# 1. iPhone에서 촬영 후 Mac으로 전송
# 2. 마커 크기 정확히 측정 (예: 3.5cm)
# 3. 실행
python scripts/aruco_tracker_flexible.py iphone_video.mov result.csv --marker-size 3.5

# 4. result.csv를 Excel에서 분석
open result.csv
```

### 예시 2: 배치 처리 (여러 영상)
```bash
for video in *.mov; do
    output="${video%.mov}_result.csv"
    python scripts/aruco_tracker_1cm.py "$video" "$output"
done
```

### 예시 3: Python에서 프로그래밍
```python
from scripts.aruco_tracker_flexible import calibrate_and_track

calibrate_and_track('video.mov', 'output.csv', marker_size_cm=5.0)
```

---

## 📈 결과 분석

### Excel에서 그래프 만들기
1. `result.csv`를 Excel에서 열기
2. `timestamp_s`, `center_x_cm`, `center_y_cm` 선택
3. 삽입 → 그래프 → 마커 궤적 시각화

### Python에서 분석
```python
import pandas as pd

df = pd.read_csv('result.csv')
print(f"마커 감지 프레임: {len(df)}")
print(f"X 좌표 범위: {df['center_x_cm'].min():.2f} ~ {df['center_x_cm'].max():.2f} cm")
print(f"Y 좌표 범위: {df['center_y_cm'].min():.2f} ~ {df['center_y_cm'].max():.2f} cm")
```

---

## ⚠️ 주의사항

1. **마커 크기 정확도** ⭐
   - 줄자로 정확하게 측정하세요
   - 10cm 마커는 실제로 10cm이어야 합니다
   - 1-2mm 오차는 괜찮습니다

2. **조명**
   - 밝고 균일한 환경에서 촬영하세요
   - 그림자가 적을수록 좋습니다

3. **마커 가시성**
   - 마커가 완전히 프레임에 들어와야 합니다
   - 부분적으로 가려지면 감지 안 됩니다

4. **배경**
   - 마커와 배경의 색상이 대비되어야 합니다
   - 패턴이 있는 배경은 피하세요

---

## 🆘 문제 해결

| 증상 | 원인 | 해결책 |
|------|------|--------|
| "마커를 감지할 수 없음" | 영상 품질 문제 | 조명 개선, 마커 크기 확인, 대비 확인 |
| "파일을 찾을 수 없음" | 경로 오류 | 파일명, 폴더 경로 확인 |
| "module not found (cv2)" | venv 미활성화 또는 opencv 미설치 | `source venv/bin/activate` 후 `pip install opencv-contrib-python` |
| "CSV가 비어있음" | 마커 미감지 | 영상 확인, 조명 개선 |
| "ValueError: marker_size_cm 오류" | --marker-size 값이 음수 | `--marker-size 1.0` 처럼 양수 사용 |

---

## 📖 더 자세한 정보

더 깊이 있는 학습과 고급 기능:

| 문서 | 내용 |
|------|------|
| `docs/START_HERE.md` | 🚀 **30초 빠른 시작** (먼저 읽기!) |
| `docs/SIMPLE_XY_CALIBRATION.md` | 📐 기본 개념: XY 좌표 변환 원리 |
| `docs/USAGE_GUIDE.md` | 📘 사용 가이드: 모든 스크립트 설명 |
| `docs/QUICK_START_1CM.md` | 🎯 1cm 마커 설정 가이드 |
| `docs/QUICK_START_USER_VIDEO.md` | 📱 iPhone 영상 처리 |
| `docs/CAMERA_CALIBRATION_GUIDE.md` | 🔧 카메라 캘리브레이션 (심화) |
| `docs/3D_POSE_ESTIMATION.md` | 3️⃣ 3D 포즈 추정 (심화) |

---

## 🛠️ 기술 스택

- **OpenCV 4.13.0+**: ArUco 마커 감지, 경계 추출
- **NumPy**: 수치 계산, 벡터 연산
- **Python CSV**: 결과 데이터 저장
- **ArUco Dictionary**: DICT_6X6_250 (250개 마커, ID 0~249)

---

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 🤝 기여

버그 리포트, 기능 제안, Pull Request 환영합니다!

GitHub: https://github.com/Noobear/ArUco-marker-tracker_v1_planar

---

## 📧 문의

이슈는 GitHub Issues에서 등록해주세요.

---

## 🎯 다음 단계

1. ✅ **지금 바로**: 위의 "빠른 시작" 섹션을 따라하세요!
2. 📖 **상세 학습**: `docs/START_HERE.md` 읽기
3. 🎬 **실제 사용**: iPhone 영상으로 테스트
4. 📊 **분석**: CSV 결과를 Excel에서 그래프화

---

**Happy Tracking!** 🚀
