# 🔧 CAMERA_CALIBRATION_GUIDE - 카메라 캘리브레이션 (심화)# 카메라 캘리브레이션 가이드



정밀한 측정을 위해 카메라를 캘리브레이션하는 방법입니다.마커의 **픽셀 좌표를 실제 거리(cm, mm)로 변환**하는 방법입니다.



---## 📊 개념 이해



## 📌 왜 필요한가?현재 시스템이 제공하는 데이터:

```

실제 카메라는 렌즈 왜곡이 있습니다:marker center: (512, 384) pixels      ← 픽셀 단위

- 배럴 왜곡: 이미지가 부풀어 보임marker size: 45 pixels                ← 픽셀 단위

- 핀쿠션 왜곡: 이미지가 오목해 보임```

- 광학 왜곡: 가장자리 변형

원하는 결과:

### 영향```

```marker center: (15.3, 11.5) cm        ← 실제 거리

캘리브레이션 전: 오차율 ±5~10%marker size: 1.35 cm                  ← 실제 크기

캘리브레이션 후: 오차율 ±0.5~1% ✅```

```

## 🔧 캘리브레이션 3가지 방법

---

### 방법 1: 간단한 스케일 팩터 (가장 빠름, 정확도 70%)

## 🎯 3가지 캘리브레이션 방법

**원리**: 알려진 크기의 마커로 픽셀-거리 비율 계산

### 방법 1️⃣: 체스판 캘리브레이션 (가장 정확!)

#### 1-1. 준비물

#### 준비물```

1. 체스판 이미지 인쇄- A4 용지에 인쇄된 ArUco 마커 (예: 5cm × 5cm)

2. 평면 배경에 고정- 줄자 또는 자

3. 카메라- iPhone 카메라

```

#### Step 1: 체스판 이미지 인쇄

```bash#### 1-2. 실행 순서

# OpenCV로 생성

python -c "**단계 1: 기준 마커 촬영**

import cv2```

import numpy as np1. 프로젝트의 marker/marker_0.png를 A4에 인쇄

   - 크기: 정확히 5cm × 5cm로 인쇄

# 8×6 체스판 생성   

board = np.zeros((480, 640, 3), dtype=np.uint8)2. iPhone으로 촬영

square_size = 60   - 카메라를 정면으로 놓기 (기울이지 않기)

   - 거리: 약 30cm (영상에 마커가 충분히 크게 나타나야 함)

for i in range(8):   - 조명: 밝고 균일한 환경

    for j in range(6):   

        if (i + j) % 2 == 0:3. 영상 저장: calibration_5cm.mov

            x1, y1 = i * square_size, j * square_size```

            x2, y2 = (i + 1) * square_size, (j + 1) * square_size

            cv2.rectangle(board, (x1, y1), (x2, y2), (255, 255, 255), -1)**단계 2: 픽셀 크기 측정**

```bash

cv2.imwrite('chessboard.png', board)# 프로젝트 디렉토리에서 실행

print('✅ 체스판 생성: chessboard.png')cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1

"source venv/bin/activate

```

python3 << 'EOF'

또는:import cv2

- OpenCV 샘플 다운로드import numpy as np

- 온라인: https://docs.opencv.org/4.0.0/pattern.png

# 1단계에서 촬영한 영상

#### Step 2: 체스판 영상 촬영video_path = 'calibration_5cm.mov'

```bashcap = cv2.VideoCapture(video_path)

# 다양한 각도에서 최소 20장 촬영

# 각 영상에서 체스판의 코너가 명확하게 보여야 함# 첫 번째 프레임 읽기

ret, frame = cap.read()

폴더 구조:if not ret:

calibration_images/    print("영상 열기 실패")

├── board_0.jpg    exit()

├── board_1.jpg

├── board_2.jpg# ArUco 마커 감지

...aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

├── board_19.jpgdetector = cv2.aruco.ArucoDetector(aruco_dict)

```corners, ids, rejected = detector.detectMarkers(frame)



촬영 팁:if ids is not None:

- ✅ 다양한 각도 (정면, 측면, 대각선)    # 첫 번째 마커의 크기 계산

- ✅ 다양한 거리 (가까움, 중간, 멀음)    corner = corners[0]

- ✅ 밝고 선명한 이미지    

- ❌ 흐릿하거나 왜곡된 이미지    # 두 점 사이 거리 계산 함수

    def distance(p1, p2):

#### Step 3: 캘리브레이션 스크립트 실행        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

```python    

import cv2    # 마커의 변의 길이 계산

import numpy as np    top_side = distance(corner[0][0], corner[0][1])

import glob    bottom_side = distance(corner[0][2], corner[0][3])

    left_side = distance(corner[0][0], corner[0][3])

# 체스판 내부 코너 개수 (8×6 보드라면 7×5)    right_side = distance(corner[0][1], corner[0][2])

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)    

objp = np.zeros((7*5, 3), np.float32)    avg_pixel_size = (top_side + bottom_side + left_side + right_side) / 4

objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)    

    print("=" * 60)

objpoints = []  # 3D 좌표    print("📏 캘리브레이션 결과")

imgpoints = []  # 2D 좌표    print("=" * 60)

    print(f"실제 마커 크기: 5.00 cm")

images = glob.glob('calibration_images/*.jpg')    print(f"픽셀 크기: {avg_pixel_size:.2f} px")

    print(f"\n스케일 팩터: {avg_pixel_size / 5.0:.4f} px/cm")

for fname in images:    print(f"역수 (cm/px): {5.0 / avg_pixel_size:.4f} cm/px")

    img = cv2.imread(fname)    print("=" * 60)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    

        # 설정 파일 생성

    ret, corners = cv2.findChessboardCorners(gray, (7, 5), None)    scale_factor = avg_pixel_size / 5.0

        

    if ret:    with open('calibration_config.txt', 'w') as f:

        objpoints.append(objp)        f.write(f"PIXELS_PER_CM={scale_factor:.4f}\n")

                f.write(f"CM_PER_PIXEL={5.0/avg_pixel_size:.4f}\n")

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)        f.write(f"CALIBRATION_DATE=2026-03-26\n")

        imgpoints.append(corners2)        f.write(f"CALIBRATION_MARKER_SIZE_CM=5.0\n")

    

# 캘리브레이션    print("\n✅ 설정 저장됨: calibration_config.txt")

ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(    

    objpoints, imgpoints, gray.shape[::-1], None, Noneelse:

)    print("❌ 마커 감지 실패 - 촬영 다시 시도")



print(f"✅ 캘리브레이션 완료!")cap.release()

print(f"카메라 매트릭스:\n{camera_matrix}")EOF

print(f"왜곡 계수:\n{dist_coeffs}")```



# 저장**출력 예시**:

np.savez('calibration.npz', ```

         camera_matrix=camera_matrix, ============================================================

         dist_coeffs=dist_coeffs)📏 캘리브레이션 결과

```============================================================

실제 마커 크기: 5.00 cm

#### Step 4: 왜곡 제거픽셀 크기: 187.45 px

```python스케일 팩터: 37.49 px/cm

import cv2역수 (cm/px): 0.0267 cm/px

import numpy as np============================================================

✅ 설정 저장됨: calibration_config.txt

# 저장된 캘리브레이션 로드```

data = np.load('calibration.npz')

camera_matrix = data['camera_matrix']#### 1-3. 스케일 팩터 사용

dist_coeffs = data['dist_coeffs']

이제 픽셀 좌표를 cm로 변환할 수 있습니다:

# 비디오 처리

cap = cv2.VideoCapture('video.mov')```python

# calibration_config.txt 읽기

while True:with open('calibration_config.txt', 'r') as f:

    ret, frame = cap.read()    for line in f:

    if not ret:        if line.startswith('CM_PER_PIXEL='):

        break            cm_per_pixel = float(line.split('=')[1])

    

    # 왜곡 제거# CSV 데이터 변환

    undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs)import csv

    

    # 이제 정확한 추적 가능with open('result_data.csv', 'r') as f_in:

    # ... ArUco 추적 코드 ...    reader = csv.DictReader(f_in)

```    

    with open('result_data_calibrated.csv', 'w', newline='') as f_out:

---        fieldnames = list(reader.fieldnames) + ['center_x_cm', 'center_y_cm']

        writer = csv.DictWriter(f_out, fieldnames=fieldnames)

### 방법 2️⃣: ArUco 마커 캘리브레이션        writer.writeheader()

        

체스판이 없을 때 사용:        for row in reader:

            # 픽셀을 cm로 변환

```python            x_px = float(row['center_x_px'])

import cv2            y_px = float(row['center_y_px'])

from cv2 import aruco            

            row['center_x_cm'] = f"{x_px * cm_per_pixel:.2f}"

# 정확히 알려진 크기의 ArUco 마커 사용            row['center_y_cm'] = f"{y_px * cm_per_pixel:.2f}"

# 예: 실제 5cm인 마커            

            writer.writerow(row)

detector = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

print("✅ 캘리브레이션된 데이터 저장: result_data_calibrated.csv")

# 마커 영상 촬영 (다양한 각도)```

# 후 추적하면서 거리 오차 계산

---

# 여러 마커의 알려진 거리로 검증

# 오차 계산 후 왜곡 계수 추정### 방법 2: 정밀 카메라 캘리브레이션 (정확도 95%)

```

**원리**: 체스보드 패턴으로 카메라의 내부 파라미터(렌즈 왜곡) 측정

---

#### 2-1. 준비물

### 방법 3️⃣: 간단한 검증 방법 (추천! ✅)```

- 체스보드 패턴 (9×6 또는 7×5 격자)

체스판이 없을 때:- A4 용지에 인쇄

- 줄자

```python- iPhone 카메라

# 1. 알려진 거리의 마커 2개 배치 (정확히 10cm 떨어짐)```

# 2. 추적 실행

# 3. 측정된 거리 vs 실제 거리 비교#### 2-2. 체스보드 생성 및 인쇄



import pandas as pd**단계 1: 체스보드 이미지 생성**

```bash

df = pd.read_csv('result.csv')python3 << 'EOF'

import cv2

# 마커 0과 1의 거리import numpy as np

marker_0_x = df[df['marker_id'] == 0]['center_x_cm'].mean()

marker_1_x = df[df['marker_id'] == 1]['center_x_cm'].mean()# 체스보드 생성 (9×6, 정사각형 크기 50px)

square_size = 50

measured_distance = abs(marker_1_x - marker_0_x)width = 9 * square_size

actual_distance = 10.0  # cmheight = 6 * square_size



error_percent = abs(measured_distance - actual_distance) / actual_distance * 100chessboard = np.zeros((height, width), dtype=np.uint8)

print(f"오차율: {error_percent:.1f}%")

for i in range(6):

# 오차율이 5% 이상이면 → 체스판 캘리브레이션 추천    for j in range(9):

```        if (i + j) % 2 == 1:

            chessboard[i*square_size:(i+1)*square_size, 

---                       j*square_size:(j+1)*square_size] = 255



## 📊 정밀도 비교cv2.imwrite('chessboard_9x6.png', chessboard)

print("✅ 체스보드 생성: chessboard_9x6.png")

| 방법 | 정밀도 | 난이도 | 시간 |print("   인쇄 크기: 9×6 격자, 각 정사각형 2.5cm × 2.5cm")

|------|--------|--------|------|EOF

| 간단 스케일만 사용 | ±5-10% | 쉬움 | 5분 |```

| **체스판 캘리브레이션** | **±0.5-1%** | **중간** | **30분** |

| 고급 카메라 모델 | ±0.1-0.3% | 어려움 | 2시간+ |**단계 2: A4에 인쇄**

```

---1. chessboard_9x6.png 열기

2. 인쇄 설정:

## 💡 언제 필요한가?   - 용지: A4

   - 배율: 100% (정사각형이 2.5cm × 2.5cm가 되도록)

### ✅ 캘리브레이션 필요   - 여백: 최소화

- 정밀도 ±1% 필요3. 인쇄

- 극도로 정확한 측정 필요```

- 다양한 거리에서 사용

**단계 3: 촬영**

### ⚠️ 캘리브레이션 선택사항```

- 정밀도 ±2-3% 충분1. 체스보드를 평평한 곳에 놓기

- 일반적인 용도2. iPhone으로 30~50장 촬영

- 같은 거리/각도에서만 사용   - 다양한 각도에서 촬영 (정면, 좌/우 45도, 상/하 45도)

   - 카메라를 기울이기, 옆각도로 보기 등

### ❌ 캘리브레이션 불필요   - 체스보드가 프레임에 완전히 들어오도록

- 정밀도 ±5% 충분3. 폴더에 저장: calibration_images/

- 상대 거리만 필요```

- 빠른 처리 필요

**단계 4: 캘리브레이션 실행**

---```bash

python3 << 'EOF'

## 🎯 결론import cv2

import numpy as np

**대부분의 경우**: 간단한 스케일 변환으로 충분 ✅from pathlib import Path

import pickle

**정밀한 측정 필요**: 체스판 캘리브레이션 추천 🔧

# 체스보드 설정

---CHESSBOARD_SIZE = (9, 6)  # (width, height)

SQUARE_SIZE = 0.025  # 2.5cm in meters

다음: `docs/3D_POSE_ESTIMATION.md` 참고

# 캘리브레이션 데이터 저장소
object_points = []  # 3D 점 (현실 세계)
image_points = []   # 2D 점 (이미지)

# 3D 기준점 생성 (z=0)
objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE

# 체스보드 감지
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

image_paths = list(Path('calibration_images').glob('*.jpg')) + \
              list(Path('calibration_images').glob('*.png')) + \
              list(Path('calibration_images').glob('*.mov'))

print(f"발견된 이미지: {len(image_paths)}개")

for img_path in sorted(image_paths)[:50]:  # 최대 50개
    img = cv2.imread(str(img_path))
    if img is None:
        continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)
    
    if ret:
        object_points.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        image_points.append(corners2)
        print(f"✅ {img_path.name}: 체스보드 감지")
    else:
        print(f"❌ {img_path.name}: 체스보드 미감지")

if len(object_points) > 3:
    # 카메라 캘리브레이션
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        object_points, image_points, gray.shape[::-1], None, None
    )
    
    print("\n" + "=" * 60)
    print("📷 카메라 캘리브레이션 완료")
    print("=" * 60)
    print(f"보정 오류: {ret:.4f}")
    print(f"\n카메라 행렬:\n{camera_matrix}")
    print(f"\n렌즈 왜곡 계수:\n{dist_coeffs}")
    print("=" * 60)
    
    # 저장
    calib_data = {
        'camera_matrix': camera_matrix,
        'dist_coeffs': dist_coeffs,
        'calibration_error': ret
    }
    
    with open('camera_calibration.pkl', 'wb') as f:
        pickle.dump(calib_data, f)
    
    print("\n✅ 캘리브레이션 데이터 저장: camera_calibration.pkl")
else:
    print(f"❌ 충분한 체스보드가 감지되지 않음 ({len(object_points)}/5 필요)")
EOF
```

#### 2-3. 캘리브레이션된 데이터 생성

```bash
python3 << 'EOF'
import cv2
import numpy as np
import pickle

# 1. 캘리브레이션 데이터 로드
with open('camera_calibration.pkl', 'rb') as f:
    calib_data = pickle.load(f)

camera_matrix = calib_data['camera_matrix']
dist_coeffs = calib_data['dist_coeffs']

# 2. 마커 감지 시 왜곡 보정
video_path = 'your_iphone_video.mov'
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 프레임 왜곡 보정
    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, dist_coeffs, (w, h), 1, (w, h)
    )
    
    frame_undistorted = cv2.undistort(
        frame, camera_matrix, dist_coeffs, None, new_camera_matrix
    )
    
    # 이제 frame_undistorted에서 마커 감지
    # (이렇게 하면 더 정확한 위치 추출 가능)

cap.release()
EOF
```

---

### 방법 3: 물리적 거리 측정 (가장 정확, 수동)

**원리**: 실제 현장에서 마커 간 거리를 직접 측정하고 비교

#### 3-1. 현장 설정
```
1. 마커 2개를 정확히 10cm 떨어져 배치
2. iPhone으로 촬영
3. 두 마커의 픽셀 거리를 측정
4. 픽셀 거리 / 실제 거리 = 스케일 팩터
```

#### 3-2. 코드 실행

```bash
python3 << 'EOF'
import cv2
import numpy as np
import math

video_path = 'calibration_distance_10cm.mov'
cap = cv2.VideoCapture(video_path)

# 첫 프레임에서 두 마커 감지
ret, frame = cap.read()
if not ret:
    print("영상 열기 실패")
    exit()

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
detector = cv2.aruco.ArucoDetector(aruco_dict)
corners, ids, rejected = detector.detectMarkers(frame)

if ids is not None and len(ids) >= 2:
    # 마커 0과 마커 1의 중심 계산
    def get_center(corner):
        return np.mean(corner[0], axis=0)
    
    center_0 = get_center(corners[0])
    center_1 = get_center(corners[1])
    
    # 픽셀 거리 계산
    pixel_distance = math.sqrt(
        (center_1[0] - center_0[0])**2 + 
        (center_1[1] - center_0[1])**2
    )
    
    print("=" * 60)
    print("📏 거리 캘리브레이션")
    print("=" * 60)
    print(f"마커 0 중심: ({center_0[0]:.1f}, {center_0[1]:.1f})")
    print(f"마커 1 중심: ({center_1[0]:.1f}, {center_1[1]:.1f})")
    print(f"픽셀 거리: {pixel_distance:.2f} px")
    print(f"실제 거리: 10.00 cm")
    print(f"\n스케일: {pixel_distance/10:.4f} px/cm")
    print(f"역수: {10/pixel_distance:.4f} cm/px")
    print("=" * 60)

cap.release()
EOF
```

---

## 🎯 어느 방법을 선택할까?

| 방법 | 소요시간 | 정확도 | 난이도 | 권장 상황 |
|------|--------|------|------|---------|
| **방법 1** | 5분 | 70% | ⭐ 쉬움 | 빠른 시작, 대략적 측정 |
| **방법 2** | 30분 | 95% | ⭐⭐⭐ 어려움 | 정밀 분석 필요 |
| **방법 3** | 10분 | 85% | ⭐⭐ 중간 | 현장 실측 가능 |

**추천**: 먼저 **방법 1로 시작** → 필요하면 **방법 2로 업그레이드**

---

## 📐 결과 해석

### 예시 1: 스케일 팩터 = 37.49 px/cm

```
마커가 이동한 거리: 50 픽셀
실제 거리: 50 px ÷ 37.49 px/cm = 1.33 cm
```

### 예시 2: 마커 속도 계산

```csv
timestamp_s  center_x_px  center_y_px  center_x_cm  center_y_cm
0.000        512.0        384.0        13.27        9.96
0.033        514.5        385.2        13.34        9.99
```

```
이동 거리: √[(13.34-13.27)² + (9.99-9.96)²] = 0.07 cm
시간 간격: 0.033 초
속도: 0.07 cm / 0.033 s = 2.12 cm/s
```

---

## 🔄 자동 캘리브레이션 스크립트

프로젝트에 자동 캘리브레이션 스크립트를 추가하려면:

```bash
# 스크립트 생성
cat > /Users/kim-kwon-woong/Visual_Studio/Python_26_1/scripts/calibrate_camera.py << 'EOF'
"""
카메라 캘리브레이션 자동화 스크립트

사용법:
    python scripts/calibrate_camera.py calibration_5cm.mov --marker-size 5.0
"""

import cv2
import numpy as np
import argparse
from pathlib import Path

def calibrate_with_marker(video_path: str, marker_size_cm: float = 5.0):
    """마커로 캘리브레이션"""
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    
    if not ret:
        print("❌ 영상 열기 실패")
        return None
    
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    detector = cv2.aruco.ArucoDetector(aruco_dict)
    corners, ids, rejected = detector.detectMarkers(frame)
    
    if ids is None or len(ids) == 0:
        print("❌ 마커 감지 실패")
        return None
    
    # 첫 번째 마커의 크기 계산
    corner = corners[0]
    
    def distance(p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    
    sides = [
        distance(corner[0][0], corner[0][1]),
        distance(corner[0][1], corner[0][2]),
        distance(corner[0][2], corner[0][3]),
        distance(corner[0][3], corner[0][0]),
    ]
    
    avg_pixel_size = np.mean(sides)
    scale_factor = avg_pixel_size / marker_size_cm
    
    print("=" * 60)
    print("✅ 캘리브레이션 완료")
    print("=" * 60)
    print(f"마커 크기: {marker_size_cm} cm")
    print(f"픽셀 크기: {avg_pixel_size:.2f} px")
    print(f"스케일: {scale_factor:.4f} px/cm")
    print(f"역수: {marker_size_cm/avg_pixel_size:.4f} cm/px")
    print("=" * 60)
    
    cap.release()
    return marker_size_cm / avg_pixel_size  # cm/px 반환

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video', help='캘리브레이션 영상 파일')
    parser.add_argument('--marker-size', type=float, default=5.0,
                       help='마커 크기 (cm), 기본값: 5.0')
    
    args = parser.parse_args()
    
    cm_per_px = calibrate_with_marker(args.video, args.marker_size)
    
    if cm_per_px:
        with open('calibration_config.txt', 'w') as f:
            f.write(f"CM_PER_PIXEL={cm_per_px:.6f}\n")
        print("✅ 설정 저장: calibration_config.txt")
EOF
```

---

## ✅ 체크리스트

- [ ] 카메라 캘리브레이션 방법 선택 (방법 1 추천)
- [ ] 마커 또는 체스보드 준비
- [ ] 캘리브레이션 영상 촬영
- [ ] 스크립트 실행하여 스케일 팩터 계산
- [ ] `calibration_config.txt` 생성 확인
- [ ] CSV 데이터 변환 (선택)
- [ ] Excel에서 cm 단위 거리 분석

---

## 🆘 문제 해결

**Q: 마커/체스보드 감지가 안 됨**
```
해결:
1. 조명 확인 (너무 어둡지 않은지)
2. 마커가 완전히 프레임에 들어오는지 확인
3. 카메라 초점이 맞는지 확인 (자동 초점이 작동하는지)
```

**Q: 스케일이 프레임마다 다르게 나옴**
```
원인: 마커가 카메라에서 가까워졌다/멀어졌다 (3D 원근감)
해결: 동일한 거리에서 촬영하거나, 3D 포즈 추정 필요
```

**Q: 카메라 캘리브레이션 오류가 높음**
```
원인: 체스보드 이미지 품질 부족
해결:
1. 더 많은 이미지 촬영 (최소 20개)
2. 다양한 각도에서 촬영
3. 체스보드 크기 정확성 확인
```

---

**다음 단계**: 위 방법 중 하나로 캘리브레이션을 완료하면, 픽셀 데이터를 자동으로 cm 단위로 변환할 수 있습니다! 🎯
