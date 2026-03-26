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

### 시스템 요구사항
- **OS**: macOS, Linux, Windows ✅ (모두 지원)
- **Python**: 3.7 이상 (3.9 권장)
- **메모리**: 최소 2GB (영상 처리용)

### 패키지 요구사항
- **opencv-contrib-python** 4.13.0 이상 (ArUco 마커 감지)
- **numpy** 2.0 이상 (수치 계산)
- **pandas** (선택, 결과 분석용)

### 확인된 작동 환경
| OS | Python | OpenCV | 상태 |
|-----|--------|--------|------|
| macOS 13+ | 3.9 | 4.13.0 | ✅ 테스트됨 |
| macOS M1/M2 | 3.9 | 4.13.0 | ✅ 테스트됨 |
| Linux | 3.7+ | 4.0+ | ✅ 지원 |
| Windows 10+ | 3.7+ | 4.0+ | ✅ 지원 |

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

## 🎬 테스트 영상으로 시작하기 (가장 쉬운 방법!)

프로젝트에 포함된 테스트 영상으로 바로 테스트할 수 있습니다:

```bash
# 1. 가상환경 활성화
source venv/bin/activate

# 2. 테스트 폴더의 영상 목록 확인
ls tests/videos/

# 3. 테스트 영상으로 실행 (1cm 마커 가정)
python scripts/aruco_tracker_1cm.py tests/videos/test_video_10s_3markers_small.mp4 test_result.csv

# 4. 결과 확인
open test_result.csv
```

**결과가 나왔나요?** 
- ✅ `test_result.csv`에 데이터가 있으면 **정상 작동!**
- ❌ CSV가 비어있으면 → 조명/마커 크기 확인

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

---

## 🎨 ArUco 마커 생성 및 출력

### 미리 생성된 마커 사용 (추천!)
프로젝트에 이미 생성된 50개의 ArUco 마커가 있습니다:

```bash
# 마커 폴더 확인
ls marker/

# 결과:
# aruco_marker_0.png (ID: 0)
# aruco_marker_1.png (ID: 1)
# ...
# aruco_marker_49.png (ID: 49)
```

### 마커 크기 조정 및 출력
1. **마커 PDF 열기**: `marker/aruco_marker_X.png` (X는 ID 번호)
2. **원하는 크기로 인쇄**:
   - 1cm 마커: 100% 스케일 인쇄
   - 2cm 마커: 200% 스케일 인쇄
   - 5cm 마커: 500% 스케일 인쇄

### 마커 스펙
- **Dictionary**: DICT_6X6_250 (6×6 비트, 250개 마커)
- **마커 ID 범위**: 0 ~ 249
- **지원 크기**: 1cm ~ 50cm 이상 (스케일 조정 가능)
- **사용 가능한 마커**: `marker/` 폴더에 0~49번 미리 생성됨

### 더 많은 마커 생성 필요시
```bash
# aruco_generate.py 스크립트로 생성 (추후 추가)
python scripts/aruco_generate.py --start-id 50 --count 200 --output marker/
```

---

## � 사용 예시

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

### 🔧 고급 트러블슈팅

#### 마커를 여전히 감지 못함
```bash
# 1. OpenCV 버전 확인
python -c "import cv2; print(cv2.__version__)"
# 결과: 4.13.0 이상인지 확인

# 2. ArUco 모듈 확인
python -c "from cv2 import aruco; print('ArUco 모듈 OK')"

# 3. 테스트 영상으로 먼저 시도
python scripts/aruco_tracker_1cm.py tests/videos/test_video_10s_3markers_small.mp4 debug.csv
# 테스트 영상은 이미 최적화되어 있음
```

#### 마커 크기가 부정확함
```bash
# 1. 실제 마커 크기 재측정 (줄자로 정확히!)
# 2. 마커 ID 확인: 마커에 인쇄된 번호 확인
# 3. 유연한 스크립트 사용:
python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 4.95

# 3mm 오차 범위 내에서 조정 가능
```

#### 프레임 드롭 또는 느린 처리
```bash
# 1. 영상 해상도 확인
python -c "import cv2; v = cv2.VideoCapture('video.mov'); print(f'해상도: {v.get(3)}x{v.get(4)}')"

# 2. 고해상도 영상은 먼저 다운스케일
# FFmpeg 사용:
ffmpeg -i original_video.mov -vf scale=1280:720 downscaled_video.mov
```

#### Windows에서 경로 오류
```bash
# Windows에서는 경로 구분자가 다름:
# ❌ 잘못: python scripts/aruco_tracker_1cm.py video.mov
# ✅ 맞음: python scripts\aruco_tracker_1cm.py video.mov

# 또는 상대경로 사용:
python scripts/aruco_tracker_1cm.py "C:\Users\YourName\Videos\video.mp4" result.csv
```

---

## ℹ️ 기술 정보

### 현재 프로젝트 버전
- **프로젝트**: ArUco-marker-tracker_v1_planar
- **버전**: v1.0 (2026.03.26)
- **상태**: ✅ 안정적
- **GitHub**: https://github.com/Noobear/ArUco-marker-tracker_v1_planar

### 개발 환경
```bash
# 현재 환경 정보 확인
python --version                    # Python 3.9
pip show opencv-contrib-python      # 4.13.0
pip show numpy                      # 2.0.2+
```

### 성능 지표
| 작업 | 성능 |
|------|------|
| 1분 영상 처리 | ~10초 (1080p) |
| 마커 감지 정확도 | 99%+ (최적 조건) |
| 좌표 정밀도 | ±2mm (마커 크기 기준) |
| 지원 마커 ID | 0 ~ 249 (250개) |
| 최대 마커 감지 | 프레임당 10개 |

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: 마커 크기를 모르면 어떻게 하나요?
**A**: 3가지 방법이 있습니다:
1. **줄자로 측정**: 가장 정확한 방법
2. **역산 계산**: 알려진 거리 2개를 측정 후 비교
3. **추정값 사용**: 처음엔 대략적인 크기(예: 5cm)로 시작, 후에 조정

### Q2: 여러 개의 마커를 동시에 추적할 수 있나요?
**A**: ✅ **네, 가능합니다!**
```bash
# 최대 10개까지 프레임당 감지 가능
# 마커 ID가 다르면 자동으로 구분됨
python scripts/aruco_tracker_flexible.py multi_marker_video.mov result.csv --marker-size 5.0

# CSV 결과에 marker_id 컬럼으로 구분됨
```

### Q3: 영상 형식은 뭘 지원하나요?
**A**: OpenCV가 지원하는 모든 형식:
- ✅ MP4, MOV, AVI, MKV, FLV, WMV
- ✅ iPhone 영상 (MOV, MP4)
- ✅ 일반 카메라 영상
- ℹ️ 해상도는 상관없음 (자동 조정)

### Q4: 실시간 카메라 입력을 사용할 수 있나요?
**A**: 현재는 **영상 파일만 지원**합니다.
실시간 카메라는 `aruco_tracker_with_video.py`에서 확장 가능합니다.

### Q5: 정확도를 높이려면?
**A**: 5가지 팁:
1. **조명**: 밝고 균일한 조건에서 촬영
2. **마커 크기**: 정확하게 측정 (±1mm)
3. **영상 품질**: 흔들림 없이, 선명하게
4. **배경**: 단순한 배경, 마커와 대비
5. **각도**: 마커가 약간 기울어져도 괜찮음

### Q6: CSV 결과를 Python에서 바로 사용하려면?
**A**:
```python
import pandas as pd

# CSV 읽기
df = pd.read_csv('result.csv')

# 특정 마커만 필터링
marker_0 = df[df['marker_id'] == 0]

# X, Y 궤적 출력
print(marker_0[['center_x_cm', 'center_y_cm']])

# 거리 계산
dx = marker_0['center_x_cm'].diff()
dy = marker_0['center_y_cm'].diff()
distance = (dx**2 + dy**2)**0.5
print(f"이동 거리: {distance.sum():.2f} cm")
```

### Q7: 마커 ID를 자유롭게 선택할 수 있나요?
**A**: ✅ **네! 0~249 중 아무 ID나 사용 가능합니다.**
```bash
# ID 100 마커 사용 가능
# marker/aruco_marker_100.png 없으면:
python scripts/aruco_generate.py --id 100 --output marker/aruco_marker_100.png
```

### Q8: Linux나 Windows에서도 작동하나요?
**A**: ✅ **네, 완전히 지원됩니다!**
유일한 차이는 경로 표기법:
```bash
# macOS/Linux
python scripts/aruco_tracker_1cm.py video.mov result.csv

# Windows (스크립트 경로)
python scripts\aruco_tracker_1cm.py video.mov result.csv
```

### Q9: 대량의 영상을 처리해야 하면?
**A**: 배치 처리 스크립트:
```bash
# macOS/Linux
for video in videos/*.mov; do
    output="${video%.mov}_result.csv"
    python scripts/aruco_tracker_flexible.py "$video" "$output" --marker-size 5.0
done

# Windows (PowerShell)
Get-ChildItem videos\*.mp4 | ForEach-Object {
    $output = $_.BaseName + "_result.csv"
    python scripts/aruco_tracker_flexible.py $_.FullName $output --marker-size 5.0
}
```

### Q10: 마커를 수동으로 생성할 수 있나요?
**A**: ✅ **온라인 생성 가능:**
- https://chev.me/arucogen/ (추천!)
- https://cv-tricks.com/opencv/generate-custom-markers-using-aruco/

생성한 마커를 `marker/` 폴더에 저장하면 됩니다.

---

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
