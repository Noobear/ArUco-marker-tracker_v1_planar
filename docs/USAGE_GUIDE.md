# 📘 USAGE_GUIDE - 상세 사용법# ArUco 마커 추적 - 사용 가이드



모든 스크립트의 상세한 사용 방법을 설명합니다.**빠른 시작은 `START_HERE.md` 참고!** ⚡



------



## 🚀 3가지 방법## 📌 1. 기본 사용법



### 방법 1️⃣: 1cm 고정 마커 (가장 간단!)```bash

cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1

**상황**: 정확히 1cm인 마커를 사용할 때source venv/bin/activate

python scripts/aruco_tracker_1cm.py your_video.mov result.csv

```bash```

python scripts/aruco_tracker_1cm.py input_video.mov output_result.csv

```**결과**: `result.csv` 파일 생성



**장점**:---

- ✅ 가장 간단함

- ✅ 추가 파라미터 없음## 🔧 2. 마커 크기 변경

- ✅ 1cm 마커만 있으면 OK

### 방법 A: 명령어로 지정 (권장!)

**예시**:

```bash```bash

python scripts/aruco_tracker_1cm.py video.mp4 result.csv# 2cm 마커

python scripts/aruco_tracker_1cm.py ~/Desktop/phone_video.mov data/output.csvpython scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 2.0

```

# 5cm 마커

---python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 5.0



### 방법 2️⃣: 마커 크기 지정 (권장! ⭐)# 3.5cm 마커

python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 3.5

**상황**: 마커 크기를 직접 지정하고 싶을 때```



```bash### 방법 B: 파일 편집

python scripts/aruco_tracker_flexible.py input_video.mov output_result.csv --marker-size 5.0

```1. `scripts/aruco_tracker_1cm.py` 열기

2. 14번 줄 찾기: `MARKER_SIZE_CM = 1.0`

**마커 크기 옵션**:3. 숫자 변경: `MARKER_SIZE_CM = 5.0` (5cm로 변경 시)

| 크기 | 명령어 예시 |4. 저장 후 실행

|------|----------|

| 1cm | `--marker-size 1.0` |---

| 2cm | `--marker-size 2.0` |

| 3.5cm | `--marker-size 3.5` |## 📊 3. 결과 파일 (result.csv)

| 5cm | `--marker-size 5.0` |

| 10cm | `--marker-size 10.0` |```

timestamp_s  marker_id  center_x_cm  center_y_cm  rotation_angle_deg

**예시**:0.000        0          13.65        10.24        -2.35

```bash0.033        0          13.71        10.31        -2.10

# 5cm 마커0.067        0          13.77        10.38        -1.85

python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 5.0```



# 3.2cm 마커 (소수점 OK)**각 컬럼 의미**:

python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 3.2- `timestamp_s`: 시간 (초)

- `marker_id`: 마커 번호

# 여러 영상 처리- `center_x_cm`: X 좌표 (cm)

for video in *.mov; do- `center_y_cm`: Y 좌표 (cm)

    python scripts/aruco_tracker_flexible.py "$video" "${video%.mov}.csv" --marker-size 5.0- `rotation_angle_deg`: 회전 각도 (도)

done

```---



**장점**:## 📋 4. Excel에서 분석

- ✅ 모든 크기에 대응

- ✅ 정확도 높음1. `result.csv` 파일 더블클릭 (또는 Excel에서 열기)

- ✅ 가장 추천!2. `center_x_cm`, `center_y_cm` 선택

3. 삽입 → 그래프 → 마커 궤적 시각화!

---

---

### 방법 3️⃣: 시각화 영상 생성 (고급! 📹)

## ✅ 체크리스트

**상황**: 추적 결과를 영상으로 확인하고 싶을 때

- [ ] 마커 크기 측정 (줄자)

```bash- [ ] 영상 촬영 (iPhone)

python scripts/aruco_tracker_with_video.py input_video.mov output_video.mp4 output_result.csv --marker-size 5.0- [ ] 컴퓨터에 복사

```- [ ] `source venv/bin/activate` 실행

- [ ] 스크립트 실행

**출력**:- [ ] `result.csv` 열기

- 📹 `output_video.mp4`: 마커 추적 결과가 그려진 영상

- 📊 `output_result.csv`: 좌표 데이터---



**예시**:## 🐛 문제 해결

```bash

# 영상으로 결과 확인| 문제 | 해결책 |

python scripts/aruco_tracker_with_video.py video.mov annotated.mp4 result.csv --marker-size 5.0|------|--------|

| "마커를 감지할 수 없음" | 영상이 밝은지, 마커가 완전히 보이는지 확인 |

# 결과 재생| "파일을 열 수 없음" | 파일명 확인, `cd` 명령어로 폴더 이동 |

open annotated.mp4| "module not found" | `source venv/bin/activate` 실행 |

```

---

**장점**:

- ✅ 시각적으로 확인 가능## 🚀 테스트해보기

- ✅ 마커 감지 여부 확인

- ✅ 디버깅에 유용```bash

# 포함된 테스트 영상으로 먼저 시험

---python scripts/aruco_tracker_1cm.py tests/videos/test_video_10s_3markers_small.mp4 test_result.csv

```

## 📁 파일 경로 사용법

---

### 상대 경로 (추천)

```bash**더 자세한 내용**: 다른 문서 참고 📖

# 현재 폴더에 있는 파일- `CAMERA_CALIBRATION_GUIDE.md`: 카메라 캘리브레이션

python scripts/aruco_tracker_1cm.py video.mov result.csv- `3D_POSE_ESTIMATION.md`: 3D 포즈 (체스판 위 높이)

- `SIMPLE_XY_CALIBRATION.md`: 기본 개념 설명

# 상위 폴더 파일
python scripts/aruco_tracker_1cm.py ../other_video.mov result.csv

# 하위 폴더 파일
python scripts/aruco_tracker_1cm.py data/videos/test.mov result.csv
```

### 절대 경로
```bash
# 전체 경로 (macOS/Linux)
python scripts/aruco_tracker_1cm.py /Users/username/Videos/video.mov ~/Desktop/result.csv

# 전체 경로 (Windows)
python scripts/aruco_tracker_1cm.py "C:\Users\username\Videos\video.mov" "C:\Desktop\result.csv"
```

---

## 📊 결과 파일 (result.csv) 형식

### 컬럼 설명

| 컬럼 | 설명 | 단위 | 예시 |
|------|------|------|------|
| `timestamp_s` | 비디오 재생 시간 | 초 | 0.000, 0.033, 0.067 |
| `frame_number` | 프레임 번호 (0부터 시작) | - | 0, 1, 2 |
| `marker_id` | ArUco 마커 ID | - | 0~249 |
| `center_x_cm` | 마커 중심 X 좌표 | cm | 13.65 |
| `center_y_cm` | 마커 중심 Y 좌표 | cm | 10.24 |
| `rotation_angle_deg` | 마커 회전 각도 | 도(°) | -2.35 |
| `corner_0_x_cm` | 좌상단 모서리 X | cm | 12.50 |
| `corner_0_y_cm` | 좌상단 모서리 Y | cm | 9.10 |
| `corner_1_x_cm` | 우상단 모서리 X | cm | 14.80 |
| `corner_1_y_cm` | 우상단 모서리 Y | cm | 9.15 |
| `corner_2_x_cm` | 우하단 모서리 X | cm | 14.85 |
| `corner_2_y_cm` | 우하단 모서리 Y | cm | 11.30 |
| `corner_3_x_cm` | 좌하단 모서리 X | cm | 12.55 |
| `corner_3_y_cm` | 좌하단 모서리 Y | cm | 11.25 |

### 실제 예시
```csv
timestamp_s,frame_number,marker_id,center_x_cm,center_y_cm,rotation_angle_deg,corner_0_x_cm,corner_0_y_cm,corner_1_x_cm,corner_1_y_cm,corner_2_x_cm,corner_2_y_cm,corner_3_x_cm,corner_3_y_cm
0.000,0,0,13.65,10.24,-2.35,12.50,9.10,14.80,9.15,14.85,11.30,12.55,11.25
0.033,1,0,13.71,10.31,-2.10,12.56,9.18,14.86,9.22,14.91,11.38,12.61,11.33
0.067,2,0,13.77,10.38,-1.85,12.62,9.26,14.92,9.30,14.97,11.46,12.67,11.41
```

---

## 💻 Python에서 직접 사용

### 방법 1: aruco_tracker_1cm.py 불러오기
```python
import sys
sys.path.append('/Users/kim-kwon-woong/Visual_Studio/Python_26_1')

from scripts.aruco_tracker_1cm import calibrate_and_track

# 실행
calibrate_and_track('video.mov', 'output.csv')

# 완료!
print("✅ 완료!")
```

### 방법 2: aruco_tracker_flexible.py 불러오기
```python
import sys
sys.path.append('/Users/kim-kwon-woong/Visual_Studio/Python_26_1')

from scripts.aruco_tracker_flexible import calibrate_and_track

# 마커 크기 지정
calibrate_and_track('video.mov', 'output.csv', marker_size_cm=5.0)

print("✅ 완료!")
```

### 방법 3: 결과 분석
```python
import pandas as pd

# CSV 읽기
df = pd.read_csv('result.csv')

# 기본 정보
print(f"총 프레임: {len(df)}")
print(f"감지된 마커 ID: {df['marker_id'].unique()}")

# 특정 마커 필터링
marker_0 = df[df['marker_id'] == 0]
print(f"마커 0 감지 프레임: {len(marker_0)}")

# 좌표 범위
print(f"X 범위: {marker_0['center_x_cm'].min():.2f} ~ {marker_0['center_x_cm'].max():.2f} cm")
print(f"Y 범위: {marker_0['center_y_cm'].min():.2f} ~ {marker_0['center_y_cm'].max():.2f} cm")

# 이동 거리 계산
dx = marker_0['center_x_cm'].diff()
dy = marker_0['center_y_cm'].diff()
distance = (dx**2 + dy**2)**0.5
total_distance = distance.sum()
print(f"총 이동 거리: {total_distance:.2f} cm")
```

---

## 🎯 일반적인 사용 사례

### 사례 1: iPhone 영상 분석
```bash
# 1. iPhone에서 촬영한 영상을 Mac으로 전송
# 2. 마커 크기 측정 (예: 3.7cm)
# 3. 실행
python scripts/aruco_tracker_flexible.py iphone_video.mov result.csv --marker-size 3.7

# 4. Excel에서 분석
open result.csv
```

### 사례 2: 여러 영상 배치 처리
```bash
# 모든 MP4 파일 처리
for video in *.mp4; do
    output="${video%.mp4}_result.csv"
    python scripts/aruco_tracker_flexible.py "$video" "$output" --marker-size 5.0
    echo "✅ $video 완료"
done
```

### 사례 3: 시각화 포함 처리
```bash
# 추적 결과를 영상으로 저장
python scripts/aruco_tracker_with_video.py \
    original.mov \
    annotated.mp4 \
    result.csv \
    --marker-size 5.0

# 결과 확인
open annotated.mp4   # 주석이 있는 영상
open result.csv      # CSV 데이터
```

---

## ⚠️ 주의사항

1. **가상환경 활성화 필수**
   ```bash
   source venv/bin/activate
   ```

2. **마커 크기는 정확하게**
   - 줄자로 cm 단위로 측정
   - 1-2mm 오차는 괜찮음

3. **파일 경로에 공백 주의**
   ```bash
   # ❌ 잘못
   python scripts/aruco_tracker_1cm.py my video.mov result.csv
   
   # ✅ 맞음
   python scripts/aruco_tracker_1cm.py "my video.mov" result.csv
   ```

4. **Windows 경로**
   ```bash
   # ❌ macOS 스타일
   python scripts/aruco_tracker_1cm.py video.mov result.csv
   
   # ✅ Windows 스타일
   python scripts\aruco_tracker_1cm.py video.mov result.csv
   ```

---

이제 사용할 준비가 되었습니다! 🚀
