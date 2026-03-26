# 3️⃣ 3D_POSE_ESTIMATION - 3D 포즈 추정 (고급)# 3D 포즈 추정: 마커의 높이와 공간 위치 측정



마커의 3D 위치와 회전을 추정하는 방법입니다.체스판 위에 놓인 마커의 **높이(Z축), 회전(3D 각도), 정확한 3D 좌표**를 측정하는 방법입니다.



---## 📐 개념



## 📌 개념### 문제 상황

```

### 2D vs 3D카메라에서 본 마커의 위치:



**2D (현재 구현)**:체스판 (기준면, Z=0)

- 카메라가 촬영한 2D 영상에서 마커 위치│

- 평면 좌표: (X cm, Y cm)│  <- 마커가 여기 있음 (Z>0, 높이 있음)

- 회전 각도: Z축 회전만│

━━━━━━━━━━━━━━━━━━━━━━

**3D (이 문서)**:

- 실제 3D 공간에서 마커 위치마커가 체스판 위에 몇 cm 떠있을 때:

- 3D 좌표: (X cm, Y cm, Z cm) - Z는 깊이!- 픽셀 위치만으로는 높이를 알 수 없음 ❌

- 회전: 3축 회전 (Roll, Pitch, Yaw)- 카메라-마커-체스판의 3D 관계를 알아야 함 ✅

```

---

### 해결 방법

## 🎯 원리```

1. 체스판의 카메라 포즈 측정

### 필요한 것   (카메라에서 체스판까지의 거리, 각도)

1. **카메라 매트릭스** (캘리브레이션으로 얻음)

2. **마커 크기** (정확하게 측정)2. 마커의 카메라 포즈 측정

3. **마커 코너** (ArUco로 감지)   (카메라에서 마커까지의 거리, 각도)



### 계산 과정3. 두 포즈의 차이를 계산

```   → 마커가 체스판 위에 몇 cm 떠있는지 알 수 있음!

마커 코너 (픽셀) ```

    ↓

solvePnP 함수---

    ↓

카메라 매트릭스 + 왜곡 제거## 🎯 1단계: 체스판 좌표계 설정

    ↓

3D 위치 & 회전 (rvec, tvec)체스판을 **기준 좌표계(Reference Frame)**로 정의:

    ↓

마커의 (X, Y, Z, Roll, Pitch, Yaw)```

```          마커

           ▲

---           │ Z (높이)

           │

## 🔧 구현 예시    ───────┼──────── Y (세로)

          /

### Step 1: 카메라 캘리브레이션 먼저         /

```bash        X (가로)

# docs/CAMERA_CALIBRATION_GUIDE.md 참고   

# calibration.npz 파일 생성   체스판 (Z=0)

```   ┌─────────────┐

   │ ◻ ◼ ◻ ◼ ◻ ◼ │

### Step 2: 3D 포즈 추정 코드   │ ◼ ◻ ◼ ◻ ◼ ◻ │

```python   │ ◻ ◼ ◻ ◼ ◻ ◼ │

import cv2   └─────────────┘

import numpy as np```

from cv2 import aruco

**설정**:

# 1. 캘리브레이션 데이터 로드- 체스판의 왼쪽 위 코너 = 원점 (0, 0, 0)

data = np.load('calibration.npz')- X축 = 오른쪽 방향

camera_matrix = data['camera_matrix']- Y축 = 아래쪽 방향

dist_coeffs = data['dist_coeffs']- Z축 = 위쪽 방향 (마커의 높이)



# 2. ArUco 설정---

marker_size_cm = 5.0  # 정확하게 측정!

marker_size_m = marker_size_cm / 100.0## 🔍 2단계: 카메라 내부 파라미터 (Camera Matrix)



# 마커의 3D 좌표 정의 (마커 중심 기준)**필수 조건**: 먼저 카메라 캘리브레이션 완료해야 함

# Z축은 마커 정면 방향

objp = np.array([```bash

    [-marker_size_m/2, -marker_size_m/2, 0],# 이전 단계에서 만든 camera_calibration.pkl이 필요

    [marker_size_m/2, -marker_size_m/2, 0],python3 << 'EOF'

    [marker_size_m/2, marker_size_m/2, 0],import pickle

    [-marker_size_m/2, marker_size_m/2, 0]

], dtype=np.float32)with open('camera_calibration.pkl', 'rb') as f:

    data = pickle.load(f)

# 3. 비디오 처리

cap = cv2.VideoCapture('video.mov')print("카메라 행렬:")

detector = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)print(data['camera_matrix'])

print("\n렌즈 왜곡 계수:")

while True:print(data['dist_coeffs'])

    ret, frame = cap.read()EOF

    if not ret:```

        break

    **카메라 행렬 예시**:

    # 왜곡 제거```

    frame = cv2.undistort(frame, camera_matrix, dist_coeffs)[[1234.5    0   640  ]

     [   0  1234.5  360  ]

    # 마커 감지 [   0      0     1  ]]

    corners, ids, rejected = detector.detectMarkers(frame)

    설명:

    if ids is not None:- 1234.5: 초점 거리 (fx, fy)

        for idx, marker_id in enumerate(ids):- (640, 360): 카메라 중심 (cx, cy)

            corner = corners[idx][0]```

            

            # 3. solvePnP로 3D 포즈 계산---

            success, rvec, tvec = cv2.solvePnP(

                objp, corner, ## 📍 3단계: 마커의 3D 포즈 추정

                camera_matrix, 

                dist_coeffs### 3-1. solvePnP로 마커 포즈 계산

            )

            ```bash

            if success:python3 << 'EOF'

                # 회전 벡터 → 오일러 각도로 변환import cv2

                rotation_matrix, _ = cv2.Rodrigues(rvec)import numpy as np

                euler_angles = rotation_matrix_to_euler(rotation_matrix)import pickle

                

                # 결과# 1. 카메라 캘리브레이션 데이터 로드

                x = tvec[0][0] * 100  # m → cmwith open('camera_calibration.pkl', 'rb') as f:

                y = tvec[1][0] * 100    calib_data = pickle.load(f)

                z = tvec[2][0] * 100

                camera_matrix = calib_data['camera_matrix']

                roll, pitch, yaw = euler_anglesdist_coeffs = calib_data['dist_coeffs']

                

                print(f"마커 {marker_id}:")# 2. 체스판 좌표계 설정 (현실 세계 3D 좌표)

                print(f"  위치: X={x:.2f}cm, Y={y:.2f}cm, Z={z:.2f}cm")CHESSBOARD_SIZE = (9, 6)

                print(f"  회전: Roll={roll:.1f}°, Pitch={pitch:.1f}°, Yaw={yaw:.1f}°")SQUARE_SIZE = 0.025  # 2.5cm per square in meters



def rotation_matrix_to_euler(R):# 체스판의 3D 점들 (Z=0, 모두 바닥)

    """회전 행렬 → 오일러 각도"""chessboard_3d = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)

    sy = np.sqrt(R[0, 0]**2 + R[1, 0]**2)chessboard_3d[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)

    chessboard_3d *= SQUARE_SIZE

    singular = sy < 1e-6

    print("체스판 3D 좌표 예시:")

    if not singular:print(f"  왼쪽 위 (0,0): {chessboard_3d[0]}")

        x = np.arctan2(R[2, 1], R[2, 2])print(f"  오른쪽 아래 (9,6): {chessboard_3d[-1]}")

        y = np.arctan2(-R[2, 0], sy)

        z = np.arctan2(R[1, 0], R[0, 0])# 3. 마커의 3D 좌표 (알려진 크기 기준)

    else:# 마커가 5cm × 5cm라고 가정 (Z축은 체스판으로부터 높이)

        x = np.arctan2(-R[1, 2], R[1, 1])# 마커는 체스판 위에 놓인 상태

        y = np.arctan2(-R[2, 0], sy)

        z = 0MARKER_SIZE_M = 0.05  # 5cm in meters

    MARKER_HEIGHT_M = 0.00  # 바닥에 접한 상태 (처음엔 0으로 설정)

    return np.degrees([x, y, z])

```# 마커의 4개 코너 (3D)

marker_3d = np.array([

---    [-MARKER_SIZE_M/2, -MARKER_SIZE_M/2, MARKER_HEIGHT_M],  # 왼쪽 위

    [ MARKER_SIZE_M/2, -MARKER_SIZE_M/2, MARKER_HEIGHT_M],  # 오른쪽 위

## 📊 결과 해석    [ MARKER_SIZE_M/2,  MARKER_SIZE_M/2, MARKER_HEIGHT_M],  # 오른쪽 아래

    [-MARKER_SIZE_M/2,  MARKER_SIZE_M/2, MARKER_HEIGHT_M],  # 왼쪽 아래

### 3D 좌표], dtype=np.float32)

```

카메라 기준 좌표계:# 4. 영상 읽기 및 마커 감지

         카메라video_path = 'your_iphone_video.mov'

            ↑ Z축 (깊이, 앞-뒤)cap = cv2.VideoCapture(video_path)

            │

       ←───┼───→ X축 (좌-우)ret, frame = cap.read()

       Y축 (상-하)if not ret:

       │    print("❌ 영상 열기 실패")

       ↓    exit()



마커 위치:# 마커 감지

X = 10.5 cm  → 카메라로부터 오른쪽으로 10.5cmaruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

Y = 8.3 cm   → 카메라 위쪽으로 8.3cmdetector = cv2.aruco.ArucoDetector(aruco_dict, cv2.aruco.DetectorParameters_create())

Z = 50.0 cm  → 카메라 정면 50cm 떨어짐corners, ids, rejected = detector.detectMarkers(frame)

```

if ids is None:

### 회전 각도 (오일러 각)    print("❌ 마커 감지 실패")

```    exit()

Roll (Φ):   X축 회전 (좌우 굴림)

Pitch (Θ):  Y축 회전 (상하 기울임)# 5. 마커 포즈 추정

Yaw (Ψ):    Z축 회전 (시계/반시계)success, rvec, tvec = cv2.solvePnP(

    marker_3d,           # 3D 점 (현실 세계)

예시:    corners[0].reshape(4, 2),  # 2D 점 (이미지)

Roll = 5°   → 마커가 약간 왼쪽으로 기울어짐    camera_matrix,

Pitch = 0°  → 상하 기울임 없음    dist_coeffs

Yaw = 45°   → 마커가 45도 회전)

```

if success:

---    # rvec: 회전 벡터 (Rodrigues 형식)

    # tvec: 변환 벡터 (위치)

## ⚠️ 주의사항    

    # 회전 행렬로 변환

### 1. 카메라 캘리브레이션 필수    rotation_matrix, _ = cv2.Rodrigues(rvec)

- 캘리브레이션 없으면 정확도 매우 낮음    

- `docs/CAMERA_CALIBRATION_GUIDE.md` 참고    print("=" * 60)

    print("📍 마커의 3D 포즈 (카메라 기준)")

### 2. 마커 크기 정확성    print("=" * 60)

- ±1mm 오차도 결과에 영향    print(f"위치 (tvec):")

- 줄자로 정확하게 측정!    print(f"  X: {tvec[0][0]:.4f}m ({tvec[0][0]*100:.2f}cm)")

    print(f"  Y: {tvec[1][0]:.4f}m ({tvec[1][0]*100:.2f}cm)")

### 3. 마커 정면성    print(f"  Z: {tvec[2][0]:.4f}m ({tvec[2][0]*100:.2f}cm)  ← 카메라로부터 거리")

- 마커가 카메라를 정면으로 봐야 정확    

- 심하게 기울어지면 감지 안 될 수 있음    print(f"\n회전 (Euler 각도로 변환):")

    # 회전 행렬 → 오일러 각도

### 4. 광학 품질    euler = cv2.RQDecomp3x3(rotation_matrix)[0]

- 흐린 영상 → 정확도 저하    print(f"  Pitch (X축 회전): {np.degrees(euler[0]):.2f}°")

- 밝고 선명한 조건 필요    print(f"  Yaw (Y축 회전): {np.degrees(euler[1]):.2f}°")

    print(f"  Roll (Z축 회전): {np.degrees(euler[2]):.2f}°")

---    

    print("=" * 60)

## 💡 활용 사례else:

    print("❌ 포즈 추정 실패")

### 사례 1: 마커 높이 측정

```pythoncap.release()

# 책상 위의 마커 높이 측정EOF

z_distance = tvec[2][0] * 100  # 카메라로부터의 거리```



if tvec[2][0] > 0:**출력 예시**:

    print(f"마커가 카메라 앞에 있음: {z_distance:.1f}cm")```

else:============================================================

    print(f"마커가 카메라 뒤에 있음")📍 마커의 3D 포즈 (카메라 기준)

```============================================================

위치 (tvec):

### 사례 2: 마커 기울임 감지  X: 0.1234m (12.34cm)

```python  Y: -0.0567m (-5.67cm)

# 마커의 pitch 각도로 기울임 감지  Z: 0.3456m (34.56cm)  ← 카메라로부터 거리

if abs(pitch) > 30:

    print("⚠️ 마커가 너무 기울어짐 (정확도 감소)")회전 (Euler 각도로 변환):

else:  Pitch (X축 회전): 5.23°

    print("✅ 마커 각도 정상")  Yaw (Y축 회전): -2.15°

```  Roll (Z축 회전): 1.87°

============================================================

### 사례 3: 깊이 기반 필터링```

```python

# 마커가 특정 거리 범위 내에 있는지 확인---

min_distance_cm = 20.0

max_distance_cm = 100.0## 🔬 4단계: 체스판과 마커의 관계 계산



z_cm = tvec[2][0] * 100체스판도 포즈를 추정하고, 마커가 체스판 위에 **몇 cm 떠있는지** 계산:



if min_distance_cm <= z_cm <= max_distance_cm:```bash

    print(f"✅ 유효한 거리: {z_cm:.1f}cm")python3 << 'EOF'

else:import cv2

    print(f"❌ 범위 벗어남: {z_cm:.1f}cm")import numpy as np

```import pickle



---# 설정 (위와 동일)

with open('camera_calibration.pkl', 'rb') as f:

## 🔗 관련 문서    calib_data = pickle.load(f)



- `docs/SIMPLE_XY_CALIBRATION.md` - 2D 좌표 변환 (기초)camera_matrix = calib_data['camera_matrix']

- `docs/CAMERA_CALIBRATION_GUIDE.md` - 카메라 캘리브레이션 (필수)dist_coeffs = calib_data['dist_coeffs']

- OpenCV 공식 문서: https://docs.opencv.org/4.0.0/

CHESSBOARD_SIZE = (9, 6)

---SQUARE_SIZE = 0.025  # 2.5cm

MARKER_SIZE_M = 0.05

**심화 학습용 문서입니다.** 대부분의 경우 2D 좌표로 충분합니다! 🚀

# 체스판 3D 좌표
chessboard_3d = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
chessboard_3d[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)
chessboard_3d *= SQUARE_SIZE

# 마커 3D 좌표 (초기: Z=0, 즉 체스판과 같은 높이)
marker_3d = np.array([
    [-MARKER_SIZE_M/2, -MARKER_SIZE_M/2, 0],
    [ MARKER_SIZE_M/2, -MARKER_SIZE_M/2, 0],
    [ MARKER_SIZE_M/2,  MARKER_SIZE_M/2, 0],
    [-MARKER_SIZE_M/2,  MARKER_SIZE_M/2, 0],
], dtype=np.float32)

# 영상 읽기
video_path = 'your_iphone_video.mov'
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

# 마커 및 체스판 감지
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
detector = cv2.aruco.ArucoDetector(aruco_dict)
corners, ids, rejected = detector.detectMarkers(frame)

# 체스판 감지
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
ret_chess, corners_chess = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

if ids is not None and ret_chess:
    print("=" * 70)
    print("📊 마커-체스판 상대 위치 관계")
    print("=" * 70)
    
    # 체스판 포즈
    success_chess, rvec_chess, tvec_chess = cv2.solvePnP(
        chessboard_3d,
        corners_chess,
        camera_matrix,
        dist_coeffs
    )
    
    # 마커 포즈
    success_marker, rvec_marker, tvec_marker = cv2.solvePnP(
        marker_3d,
        corners[0].reshape(4, 2),
        camera_matrix,
        dist_coeffs
    )
    
    if success_chess and success_marker:
        # 체스판을 기준 좌표계로 변환
        # 역행렬 계산
        rot_chess, _ = cv2.Rodrigues(rvec_chess)
        rot_chess_inv = rot_chess.T
        tvec_chess_inv = -rot_chess_inv @ tvec_chess
        
        # 마커의 상대 포즈 (체스판 기준)
        rot_marker, _ = cv2.Rodrigues(rvec_marker)
        
        # 상대 변환
        tvec_relative = rot_chess_inv @ (tvec_marker - tvec_chess)
        rot_relative = rot_chess_inv @ rot_marker
        
        print(f"\n체스판 (기준 좌표계):")
        print(f"  위치: ({tvec_chess[0][0]*100:.2f}cm, "
              f"{tvec_chess[1][0]*100:.2f}cm, {tvec_chess[2][0]*100:.2f}cm)")
        
        print(f"\n마커 (카메라 좌표계):")
        print(f"  위치: ({tvec_marker[0][0]*100:.2f}cm, "
              f"{tvec_marker[1][0]*100:.2f}cm, {tvec_marker[2][0]*100:.2f}cm)")
        
        print(f"\n📍 마커 (체스판 기준):")
        print(f"  X: {tvec_relative[0][0]*100:.2f}cm (왼쪽/오른쪽)")
        print(f"  Y: {tvec_relative[1][0]*100:.2f}cm (위/아래)")
        print(f"  Z: {tvec_relative[2][0]*100:.2f}cm  ← 체스판 위 높이! ✅")
        
        # 회전 각도
        euler = cv2.RQDecomp3x3(rot_relative)[0]
        print(f"\n회전:")
        print(f"  Pitch: {np.degrees(euler[0]):.2f}°")
        print(f"  Yaw: {np.degrees(euler[1]):.2f}°")
        print(f"  Roll: {np.degrees(euler[2]):.2f}°")
        
        print("=" * 70)
    else:
        print("❌ 포즈 추정 실패")
else:
    print("❌ 마커 또는 체스판 감지 실패")

cap.release()
EOF
```

**출력 예시**:
```
======================================================================
📊 마커-체스판 상대 위치 관계
======================================================================

체스판 (기준 좌표계):
  위치: (-5.32cm, -8.45cm, 45.23cm)

마커 (카메라 좌표계):
  위치: (-2.15cm, -1.23cm, 48.76cm)

📍 마커 (체스판 기준):
  X: 3.17cm (왼쪽/오른쪽)
  Y: 7.22cm (위/아래)
  Z: 3.53cm  ← 체스판 위 높이! ✅

회전:
  Pitch: 2.34°
  Yaw: -1.45°
  Roll: 0.89°
======================================================================
```

---

## 🎬 5단계: 실시간 3D 추적 스크립트

프로젝트에 추가할 수 있는 완전한 3D 추적 스크립트:

```bash
cat > /Users/kim-kwon-woong/Visual_Studio/Python_26_1/scripts/pose_3d_tracker.py << 'EOF'
"""
3D 포즈 추정을 이용한 마커 추적

사용법:
    python scripts/pose_3d_tracker.py video.mov output.csv camera_calibration.pkl
"""

import cv2
import numpy as np
import csv
import pickle
import argparse
from pathlib import Path

def quaternion_from_rotation_matrix(R):
    """회전 행렬 → 사원수"""
    trace = np.trace(R)
    
    if trace > 0:
        S = 2.0 * np.sqrt(trace + 1.0)
        w = 0.25 * S
        x = (R[2, 1] - R[1, 2]) / S
        y = (R[0, 2] - R[2, 0]) / S
        z = (R[1, 0] - R[0, 1]) / S
    elif (R[0, 0] > R[1, 1]) and (R[0, 0] > R[2, 2]):
        S = 2.0 * np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
        w = (R[2, 1] - R[1, 2]) / S
        x = 0.25 * S
        y = (R[0, 1] + R[1, 0]) / S
        z = (R[0, 2] + R[2, 0]) / S
    elif R[1, 1] > R[2, 2]:
        S = 2.0 * np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
        w = (R[0, 2] - R[2, 0]) / S
        x = (R[0, 1] + R[1, 0]) / S
        y = 0.25 * S
        z = (R[1, 2] + R[2, 1]) / S
    else:
        S = 2.0 * np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
        w = (R[1, 0] - R[0, 1]) / S
        x = (R[0, 2] + R[2, 0]) / S
        y = (R[1, 2] + R[2, 1]) / S
        z = 0.25 * S
    
    return w, x, y, z

def track_markers_3d(video_path, output_csv, calib_pkl, 
                     marker_size_m=0.05, chessboard_size=(9, 6)):
    """3D 포즈로 마커 추적"""
    
    # 카메라 캘리브레이션 로드
    with open(calib_pkl, 'rb') as f:
        calib_data = pickle.load(f)
    
    camera_matrix = calib_data['camera_matrix']
    dist_coeffs = calib_data['dist_coeffs']
    
    # 체스판 3D 좌표
    square_size = 0.025  # 2.5cm
    chessboard_3d = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    chessboard_3d[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    chessboard_3d *= square_size
    
    # 마커 3D 좌표
    marker_3d = np.array([
        [-marker_size_m/2, -marker_size_m/2, 0],
        [ marker_size_m/2, -marker_size_m/2, 0],
        [ marker_size_m/2,  marker_size_m/2, 0],
        [-marker_size_m/2,  marker_size_m/2, 0],
    ], dtype=np.float32)
    
    # ArUco 설정
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    detector = cv2.aruco.ArucoDetector(aruco_dict)
    
    # 비디오 열기
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 체스판 포즈 (프레임별로 변할 수 있으므로 캐시)
    chess_pose_cache = {}
    
    # CSV 쓰기
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'frame', 'timestamp_s', 'marker_id',
            'pos_x_cm', 'pos_y_cm', 'pos_z_cm',
            'rot_pitch_deg', 'rot_yaw_deg', 'rot_roll_deg',
            'quat_w', 'quat_x', 'quat_y', 'quat_z'
        ])
        
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            timestamp = frame_idx / fps
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 체스판 감지 및 포즈 계산
            ret_chess, corners_chess = cv2.findChessboardCorners(gray, chessboard_size, None)
            
            chess_pose = None
            if ret_chess:
                success, rvec_chess, tvec_chess = cv2.solvePnP(
                    chessboard_3d, corners_chess, camera_matrix, dist_coeffs
                )
                if success:
                    rot_chess, _ = cv2.Rodrigues(rvec_chess)
                    chess_pose = (rot_chess, tvec_chess)
            
            # 마커 감지
            corners, ids, rejected = detector.detectMarkers(frame)
            
            if ids is not None and chess_pose is not None:
                rot_chess, tvec_chess = chess_pose
                rot_chess_inv = rot_chess.T
                
                for marker_idx, marker_id in enumerate(ids):
                    success, rvec_marker, tvec_marker = cv2.solvePnP(
                        marker_3d, corners[marker_idx].reshape(4, 2),
                        camera_matrix, dist_coeffs
                    )
                    
                    if success:
                        rot_marker, _ = cv2.Rodrigues(rvec_marker)
                        
                        # 상대 포즈 계산
                        tvec_rel = rot_chess_inv @ (tvec_marker - tvec_chess)
                        rot_rel = rot_chess_inv @ rot_marker
                        
                        # 오일러 각도
                        euler = cv2.RQDecomp3x3(rot_rel)[0]
                        
                        # 사원수
                        quat = quaternion_from_rotation_matrix(rot_rel)
                        
                        writer.writerow([
                            frame_idx,
                            f"{timestamp:.3f}",
                            int(marker_id[0]),
                            f"{tvec_rel[0][0]*100:.2f}",
                            f"{tvec_rel[1][0]*100:.2f}",
                            f"{tvec_rel[2][0]*100:.2f}",
                            f"{np.degrees(euler[0]):.2f}",
                            f"{np.degrees(euler[1]):.2f}",
                            f"{np.degrees(euler[2]):.2f}",
                            f"{quat[0]:.4f}",
                            f"{quat[1]:.4f}",
                            f"{quat[2]:.4f}",
                            f"{quat[3]:.4f}",
                        ])
            
            frame_idx += 1
            if frame_idx % 30 == 0:
                print(f"처리 중: {frame_idx}/{total_frames} ({100*frame_idx/total_frames:.1f}%)")
    
    cap.release()
    print(f"✅ 3D 포즈 데이터 저장: {output_csv}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video', help='입력 비디오 파일')
    parser.add_argument('output', help='출력 CSV 파일')
    parser.add_argument('calibration', help='카메라 캘리브레이션 파일 (pkl)')
    parser.add_argument('--marker-size', type=float, default=0.05,
                       help='마커 크기 (미터), 기본값: 0.05m (5cm)')
    
    args = parser.parse_args()
    
    track_markers_3d(args.video, args.output, args.calibration, args.marker_size)
EOF
```

**사용법**:
```bash
# 1. 먼저 카메라 캘리브레이션 완료 필요 (camera_calibration.pkl 생성)
# 2. 실행
python scripts/pose_3d_tracker.py video.mov output_3d.csv camera_calibration.pkl

# 3. 결과 확인
head -5 output_3d.csv
```

**출력 예시**:
```csv
frame,timestamp_s,marker_id,pos_x_cm,pos_y_cm,pos_z_cm,rot_pitch_deg,rot_yaw_deg,rot_roll_deg,quat_w,quat_x,quat_y,quat_z
0,0.000,0,5.23,-2.15,3.53,2.34,-1.45,0.89,0.9975,0.0204,-0.0126,0.0077
1,0.033,0,5.31,-2.08,3.54,2.32,-1.47,0.91,0.9974,0.0206,-0.0127,0.0079
2,0.067,0,5.38,-2.01,3.55,2.30,-1.49,0.93,0.9973,0.0208,-0.0128,0.0081
```

---

## 📊 6단계: Excel에서 3D 데이터 분석

### 6-1. 높이 변화 그래프
```excel
X축: timestamp_s
Y축: pos_z_cm
→ 마커가 어떻게 들떠있는지 시간에 따른 변화
```

### 6-2. 3D 궤적 시각화
```python
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv('output_3d.csv')

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# X, Y, Z 위치 플롯
ax.plot(df['pos_x_cm'], df['pos_y_cm'], df['pos_z_cm'], 'b-', linewidth=2)
ax.scatter(df['pos_x_cm'].iloc[0], df['pos_y_cm'].iloc[0], df['pos_z_cm'].iloc[0], 
          c='g', s=100, marker='o', label='시작')
ax.scatter(df['pos_x_cm'].iloc[-1], df['pos_y_cm'].iloc[-1], df['pos_z_cm'].iloc[-1], 
          c='r', s=100, marker='x', label='종료')

ax.set_xlabel('X (cm)')
ax.set_ylabel('Y (cm)')
ax.set_zlabel('Z (cm) - 높이')
ax.legend()
ax.set_title('마커의 3D 궤적 (체스판 기준)')

plt.savefig('marker_trajectory_3d.png', dpi=150)
print("✅ 3D 궤적 저장: marker_trajectory_3d.png")
```

---

## 🎯 정리: 체스판 위의 마커 높이 측정

### 워크플로우
```
1. 카메라 캘리브레이션 (camera_calibration.pkl 생성)
   ↓
2. 체스판 + 마커 영상 촬영
   ↓
3. pose_3d_tracker.py 실행
   ↓
4. output_3d.csv 생성 (pos_z_cm = 높이!)
   ↓
5. Excel 또는 Python으로 분석
```

### 얻을 수 있는 정보
```
✅ pos_x_cm: 체스판 내에서 좌우 위치
✅ pos_y_cm: 체스판 내에서 상하 위치
✅ pos_z_cm: 체스판 위 높이 (이게 답!)
✅ rot_pitch/yaw/roll: 3D 회전 각도
✅ quat_w/x/y/z: 사원수 형식 (고급 분석용)
```

---

## ⚠️ 주의사항

### 정확도 영향 요인
```
1. 카메라 캘리브레이션 품질 (정확도 결정)
   - 체스판 이미지 20개 이상 권장
   - 다양한 각도에서 촬영
   
2. 체스판 평탄성 (기준면 정확도)
   - 굽어진 체스판 사용 불가
   - 딱딱한 종이나 판에 인쇄
   
3. 조명 (마커 감지 안정성)
   - 그림자 없는 균일한 조명
   - 어두운 환경 피하기
   
4. 카메라 흔들림 (위치 정확도)
   - 안정적인 카메라 설치
   - 비디오 안정화 기능 활용
```

### 오류가 높을 때
```
❌ "Z 값이 음수가 나온다"
   → 마커가 체스판 아래에 감지됨
   → 체스판 카메라 각도 확인

❌ "값이 계속 튀어다닌다"
   → 카메라 캘리브레이션 재실행
   → 더 많은 체스판 이미지 사용

❌ "체스판이 감지되지 않음"
   → 조명 개선
   → 체스판이 프레임 전체에 보이게 촬영
```

---

## ✅ 완전한 워크플로우

```bash
# 1. 카메라 캘리브레이션 (문서 참조)
# → camera_calibration.pkl 생성

# 2. 체스판 위에 마커 놓고 촬영
python scripts/pose_3d_tracker.py \
  experiment_video.mov \
  experiment_3d.csv \
  camera_calibration.pkl \
  --marker-size 0.05

# 3. 결과 확인
cat experiment_3d.csv | head -10

# 4. Python 분석
python3 << 'EOF'
import pandas as pd
df = pd.read_csv('experiment_3d.csv')
print(f"평균 높이: {df['pos_z_cm'].mean():.2f}cm")
print(f"최대 높이: {df['pos_z_cm'].max():.2f}cm")
print(f"최소 높이: {df['pos_z_cm'].min():.2f}cm")
EOF
```

---

**이제 마커의 정확한 3D 위치와 높이를 모두 알 수 있습니다!** 🎯✨
