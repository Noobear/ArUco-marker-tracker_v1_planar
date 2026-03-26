# 📐 SIMPLE_XY_CALIBRATION - XY 좌표 변환 원리# 간단한 마커 크기 기반 캘리브레이션



이 문서는 **픽셀 좌표를 cm 좌표로 변환하는 원리**를 설명합니다.마커가 **수평면(XY)에서만 움직인다면** 이 방법이 가장 간단합니다!



---## 🎯 원리



## 🎯 기본 개념```

마커가 평면 위에만 있을 때:

### 문제

카메라가 촬영한 영상은 **픽셀 단위**입니다:실제 마커 크기: 5cm × 5cm (알려진 값)

- 마커의 중심이 프레임의 (640, 360) 픽셀에 있음        ↓

- **하지만 우리는 cm 단위로 알고 싶음!**영상에서 마커 크기: 187px × 187px (측정된 값)

        ↓

### 해결스케일 팩터 = 187px / 5cm = 37.4 px/cm

**마커 크기**를 기준으로 변환합니다:        ↓

모든 픽셀 좌표를 cm로 변환 가능!

``````

마커 크기(픽셀) → 계산 → 스케일(픽셀/cm)

                         ↓---

마커 위치(픽셀) ───────────→ 마커 위치(cm)

```## ⚡ 방법: 마커 크기만 입력



---```bash

python3 << 'EOF'

## 🔧 변환 방법import cv2

import numpy as np

### Step 1: 첫 프레임에서 마커 감지import csv

```python

# OpenCV ArUco로 마커 감지# ============================================================

corners, ids, rejected = detector.detectMarkers(frame)# 1단계: 마커 크기 설정 (YOUR INPUT HERE!)

# ============================================================

# 첫 번째 마커의 4개 코너:

# corners[0] = [[x0,y0], [x1,y1], [x2,y2], [x3,y3]]MARKER_SIZE_CM = 5.0  # ← 당신의 마커 실제 크기 (cm)

#

#   [x0,y0]────[x1,y1]# ============================================================

#      │          │# 2단계: 첫 프레임에서 스케일 팩터 자동 계산

#      │  마커    │# ============================================================

#      │  1cm     │

#      │          │video_path = 'your_iphone_video.mov'

#   [x3,y3]────[x2,y2]cap = cv2.VideoCapture(video_path)

```

ret, frame = cap.read()

### Step 2: 마커 크기 계산 (픽셀)if not ret:

```python    print("❌ 영상 열기 실패")

# 마커의 가로 크기 (픽셀)    exit()

width_px = distance([x0,y0], [x1,y1])

# ArUco 마커 감지

# 마커의 세로 크기 (픽셀)aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

height_px = distance([x1,y1], [x2,y2])detector = cv2.aruco.ArucoDetector(aruco_dict)

corners, ids, rejected = detector.detectMarkers(frame)

# 평균값 사용

marker_size_px = (width_px + height_px) / 2if ids is None or len(ids) == 0:

    print("❌ 첫 프레임에서 마커 감지 실패")

# 예: marker_size_px = 127 픽셀    exit()

```

# 첫 번째 마커의 픽셀 크기 계산

### Step 3: 스케일 계산corner = corners[0]

```python

# 사용자가 지정한 마커 크기: marker_size_cm = 5.0 cmdef distance(p1, p2):

    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# 변환 계산:

scale_cm_per_px = marker_size_cm / marker_size_px# 마커의 4개 변의 길이

               = 5.0 cm / 127 pixelssides = [

               = 0.0394 cm/pixel    distance(corner[0][0], corner[0][1]),  # 위

    distance(corner[0][1], corner[0][2]),  # 오른쪽

# 의미: 1 픽셀 = 0.0394 cm    distance(corner[0][2], corner[0][3]),  # 아래

```    distance(corner[0][3], corner[0][0]),  # 왼쪽

]

### Step 4: 모든 좌표 변환

```pythonavg_pixel_size = np.mean(sides)

# 픽셀 좌표 (카메라로부터)scale_cm_per_px = MARKER_SIZE_CM / avg_pixel_size

x_px = 640

y_px = 360print("=" * 60)

print("✅ 스케일 팩터 자동 계산")

# cm 좌표로 변환print("=" * 60)

x_cm = x_px * scale_cm_per_pxprint(f"입력한 마커 크기: {MARKER_SIZE_CM} cm")

     = 640 * 0.0394print(f"영상에서 측정된 크기: {avg_pixel_size:.2f} px")

     = 25.22 cmprint(f"스케일 팩터: {scale_cm_per_px:.6f} cm/px")

print("=" * 60)

y_cm = y_px * scale_cm_per_px

     = 360 * 0.0394# ============================================================

     = 14.18 cm# 3단계: 모든 프레임의 마커 좌표를 cm로 변환

```# ============================================================



---output_csv = 'result_calibrated_xy.csv'



## 📊 실제 예시with open(output_csv, 'w', newline='') as f:

    writer = csv.writer(f)

### 시나리오    writer.writerow([

- **마커 크기**: 5.0 cm (줄자로 측정)        'timestamp_s', 'frame_number', 'marker_id',

- **카메라**: iPhone 12        'center_x_cm', 'center_y_cm',  # ← cm 단위!

- **영상 해상도**: 1920 × 1080        'rotation_angle_deg',

        'corner_0_x_cm', 'corner_0_y_cm',

### 계산        'corner_1_x_cm', 'corner_1_y_cm',

        'corner_2_x_cm', 'corner_2_y_cm',

#### 1. 첫 프레임 분석        'corner_3_x_cm', 'corner_3_y_cm',

```    ])

마커 감지됨:    

- 좌상단: (x0=500, y0=300)    fps = cap.get(cv2.CAP_PROP_FPS)

- 우상단: (x1=627, y1=305)    frame_idx = 0

- 우하단: (x2=632, y2=432)    

- 좌하단: (x3=505, y3=427)    while True:

```        ret, frame = cap.read()

        if not ret:

#### 2. 마커 크기 계산            break

```        

가로: √((627-500)² + (305-300)²) = √(127² + 5²) = 127.1 픽셀        timestamp = frame_idx / fps

세로: √((632-627)² + (432-305)²) = √(5² + 127²) = 127.1 픽셀        

평균: 127.1 픽셀        # 마커 감지

```        corners, ids, rejected = detector.detectMarkers(frame)

        

#### 3. 스케일 계산        if ids is not None:

```            for marker_idx, marker_id in enumerate(ids):

scale_cm_per_px = 5.0 cm / 127.1 pixels = 0.03935 cm/pixel                corner = corners[marker_idx]

```                

                # 중심 계산

#### 4. 모든 프레임 변환                center_px = np.mean(corner[0], axis=0)

```                center_cm = center_px * scale_cm_per_px

프레임 0: (640, 360) px → (25.22, 14.17) cm                

프레임 1: (645, 365) px → (25.41, 14.37) cm                # 회전각 계산 (기존 방식 동일)

프레임 2: (650, 370) px → (25.61, 14.57) cm                v1 = corner[0][1] - corner[0][0]

...                angle = np.degrees(np.arctan2(v1[1], v1[0]))

```                

                # 코너 좌표 변환 (cm)

---                corners_cm = corner[0] * scale_cm_per_px

                

## 🔍 공식 정리                writer.writerow([

                    f"{timestamp:.3f}",

### 핵심 공식                    frame_idx,

                    int(marker_id[0]),

```                    f"{center_cm[0]:.2f}",

1. 첫 프레임에서 마커 감지                    f"{center_cm[1]:.2f}",

   corners = detector.detectMarkers(first_frame)                    f"{angle:.2f}",

                    f"{corners_cm[0][0]:.2f}",

2. 마커 크기 계산 (픽셀)                    f"{corners_cm[0][1]:.2f}",

   width_px = ||corner[1] - corner[0]||                    f"{corners_cm[1][0]:.2f}",

   height_px = ||corner[2] - corner[1]||                    f"{corners_cm[1][1]:.2f}",

   marker_size_px = (width_px + height_px) / 2                    f"{corners_cm[2][0]:.2f}",

                    f"{corners_cm[2][1]:.2f}",

3. 스케일 계산                    f"{corners_cm[3][0]:.2f}",

   scale_cm_per_px = marker_size_cm / marker_size_px                    f"{corners_cm[3][1]:.2f}",

                ])

4. 좌표 변환 (모든 프레임)        

   x_cm = x_px * scale_cm_per_px        frame_idx += 1

   y_cm = y_px * scale_cm_per_px        if frame_idx % 30 == 0:

```            fps_cap = cap.get(cv2.CAP_PROP_FPS)

            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

### Python 코드            print(f"처리 중: {frame_idx}/{total} ({100*frame_idx/total:.1f}%)")

```python

import cv2cap.release()

import numpy as np

print("\n" + "=" * 60)

def calculate_scale(marker_size_cm, corners):print("✅ 결과 저장 완료!")

    """마커로부터 스케일 계산"""print(f"파일: {output_csv}")

    corner = corners[0]print("=" * 60)

    

    # 마커의 4개 변 길이 계산# 결과 미리보기

    side1 = np.linalg.norm(corner[1] - corner[0])print("\n첫 5줄:")

    side2 = np.linalg.norm(corner[2] - corner[1])with open(output_csv, 'r') as f:

    side3 = np.linalg.norm(corner[3] - corner[2])    for i, line in enumerate(f):

    side4 = np.linalg.norm(corner[0] - corner[3])        if i < 6:

                print(line.strip())

    # 평균 사이즈

    marker_size_px = np.mean([side1, side2, side3, side4])EOF

    ```

    # 스케일 계산

    scale_cm_per_px = marker_size_cm / marker_size_px**출력 예시**:

    ```

    return scale_cm_per_px============================================================

✅ 스케일 팩터 자동 계산

def pixel_to_cm(pixel_coord, scale_cm_per_px):============================================================

    """픽셀 좌표를 cm으로 변환"""입력한 마커 크기: 5.0 cm

    return pixel_coord * scale_cm_per_px영상에서 측정된 크기: 187.45 px

스케일 팩터: 0.026638 cm/px

# 사용 예시============================================================

marker_size_cm = 5.0

corners = detector.detectMarkers(frame)[0]처리 중: 30/300 (10.0%)

scale = calculate_scale(marker_size_cm, corners)처리 중: 60/300 (20.0%)

...

# 마커 중심 (픽셀)

center_px = np.mean(corners[0], axis=0)============================================================

✅ 결과 저장 완료!

# 마커 중심 (cm)파일: result_calibrated_xy.csv

center_cm = pixel_to_cm(center_px, scale)============================================================

print(f"마커 위치: {center_cm} cm")

```첫 5줄:

timestamp_s,frame_number,marker_id,center_x_cm,center_y_cm,rotation_angle_deg,...

---0.000,0,0,13.65,10.24,-2.35,...

0.033,1,0,13.71,10.31,-2.10,...

## ⚠️ 주의사항0.067,2,0,13.77,10.38,-1.85,...

```

### 1. 정확한 마커 크기 측정

- ❌ 대략적인 크기 사용 → 결과 부정확---

- ✅ 줄자로 정확하게 측정 → 오차 최소화

## 📐 결과 해석

**영향도**:

``````csv

마커 크기 오차 1mm → 결과 오차 ~2%timestamp_s  center_x_cm  center_y_cm  rotation_angle_deg

마커 크기 오차 5mm → 결과 오차 ~10%0.000        13.65        10.24        -2.35

```0.033        13.71        10.31        -2.10

0.067        13.77        10.38        -1.85

### 2. 카메라 왜곡```

- 실제 카메라는 렌즈 왜곡이 있음

- 간단한 스케일 변환으로는 완벽하지 않음- **center_x_cm, center_y_cm**: 마커 중심의 실제 좌표 (cm)

- 정밀도가 필요하면 → 카메라 캘리브레이션 사용- **rotation_angle_deg**: 마커 회전각 (도)



### 3. 마커 기울기---

- 마커가 기울어져도 작동함

- ArUco는 회전 불변적(rotation-invariant)## 🚀 완전한 프로젝트용 스크립트

- 각도는 별도로 계산됨

프로젝트에 추가할 스크립트를 만들겠습니다:

### 4. 카메라 원점 기준

- 모든 좌표는 **카메라를 기준**으로 함```bash

- 월드 좌표계(실제 위치)와는 다름cat > /Users/kim-kwon-woong/Visual_Studio/Python_26_1/scripts/simple_marker_calibration.py << 'EOF'

- 관계 설정 필요시 → 3D 포즈 추정 사용"""

간단한 마커 크기 기반 캘리브레이션

---마커가 수평면(XY)에서만 움직일 때 사용



## 📈 정확도 개선사용법:

    python scripts/simple_marker_calibration.py \

### 방법 1: 더 정확한 마커 측정        input.mov output.csv --marker-size 5.0

```bash

# 5개 점에서 측정 후 평균예시:

- 중심: 5.01cm    python scripts/simple_marker_calibration.py \

- 좌측: 5.00cm        my_video.mov result_calibrated.csv --marker-size 5.0

- 우측: 5.02cm"""

- 상단: 5.01cm

- 하단: 5.00cmimport cv2

평균: 5.01cm ✅import numpy as np

```import csv

import argparse

### 방법 2: 여러 프레임 사용from pathlib import Path

```python

# 처음 10프레임에서 스케일 계산, 평균 사용

scales = []def get_marker_pixel_size(frame, marker_size_cm=5.0):

for i in range(10):    """

    frame = video.read()    첫 프레임에서 마커를 감지하고 스케일 팩터 계산

    scale = calculate_scale(marker_size_cm, detect_markers(frame))    

    scales.append(scale)    Returns:

        scale_cm_per_px: cm/픽셀 변환 팩터

average_scale = np.mean(scales)  # 더 안정적    """

```    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    detector = cv2.aruco.ArucoDetector(aruco_dict)

### 방법 3: 카메라 캘리브레이션    corners, ids, rejected = detector.detectMarkers(frame)

- 체스판 캘리브레이션 사용    

- 렌즈 왜곡 제거    if ids is None or len(ids) == 0:

- 정밀도 ~0.1% 향상        raise ValueError("마커를 감지할 수 없습니다. 영상을 확인하세요.")

- 상세: `docs/CAMERA_CALIBRATION_GUIDE.md` 참고    

    # 첫 번째 마커의 크기 계산

---    corner = corners[0]

    

## 🧪 검증    def distance(p1, p2):

        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

### 방법: 알려진 거리 측정    

```python    sides = [

# 1. 마커 2개를 정확하게 10cm 떨어뜨려 배치        distance(corner[0][0], corner[0][1]),

# 2. 추적 실행        distance(corner[0][1], corner[0][2]),

# 3. 결과 확인        distance(corner[0][2], corner[0][3]),

        distance(corner[0][3], corner[0][0]),

df = pd.read_csv('result.csv')    ]

    

# 마커 0과 1의 거리 계산    avg_pixel_size = np.mean(sides)

marker_0 = df[df['marker_id'] == 0]['center_x_cm'].mean()    scale_cm_per_px = marker_size_cm / avg_pixel_size

marker_1 = df[df['marker_id'] == 1]['center_x_cm'].mean()    

    return scale_cm_per_px, avg_pixel_size

distance = abs(marker_1 - marker_0)

print(f"측정된 거리: {distance:.2f} cm")

print(f"실제 거리: 10.00 cm")def calibrate_marker_tracking(video_path, output_csv, marker_size_cm=5.0):

print(f"오차율: {abs(distance - 10.0) / 10.0 * 100:.1f}%")    """

    마커 크기 기반 캘리브레이션으로 XY 좌표를 cm로 변환

# 결과    """

# 측정된 거리: 10.03 cm ✅    

# 오차율: 0.3% (매우 좋음!)    cap = cv2.VideoCapture(video_path)

```    

    if not cap.isOpened():

---        raise FileNotFoundError(f"영상 파일을 열 수 없음: {video_path}")

    

## 🎯 결론    # 첫 프레임에서 스케일 팩터 계산

    ret, first_frame = cap.read()

**간단한 스케일 변환으로**:    if not ret:

- ✅ 픽셀을 cm으로 변환 가능        raise ValueError("첫 프레임을 읽을 수 없음")

- ✅ 정확도 ±2% (마커 크기 정확하면)    

- ✅ 구현이 간단    scale_cm_per_px, pixel_size = get_marker_pixel_size(first_frame, marker_size_cm)

- ⚠️ 극도의 정확도 필요시 → 카메라 캘리브레이션    

    print("=" * 70)

이 방법은 **대부분의 실용적 용도**에 충분합니다! 🚀    print("✅ 마커 크기 기반 캘리브레이션")

    print("=" * 70)
    print(f"입력한 마커 크기: {marker_size_cm:.1f} cm")
    print(f"영상에서 측정된 크기: {pixel_size:.2f} px")
    print(f"스케일 팩터: {scale_cm_per_px:.6f} cm/px")
    print("=" * 70)
    
    # CSV 작성
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    detector = cv2.aruco.ArucoDetector(aruco_dict)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'timestamp_s', 'frame_number', 'marker_id',
            'center_x_cm', 'center_y_cm',
            'rotation_angle_deg',
            'corner_0_x_cm', 'corner_0_y_cm',
            'corner_1_x_cm', 'corner_1_y_cm',
            'corner_2_x_cm', 'corner_2_y_cm',
            'corner_3_x_cm', 'corner_3_y_cm',
        ])
        
        frame_idx = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 처음부터 시작
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            timestamp = frame_idx / fps
            
            corners, ids, rejected = detector.detectMarkers(frame)
            
            if ids is not None:
                for marker_idx, marker_id in enumerate(ids):
                    corner = corners[marker_idx]
                    
                    # 중심 계산 (cm)
                    center_px = np.mean(corner[0], axis=0)
                    center_cm = center_px * scale_cm_per_px
                    
                    # 회전각
                    v1 = corner[0][1] - corner[0][0]
                    angle = np.degrees(np.arctan2(v1[1], v1[0]))
                    
                    # 코너 좌표 (cm)
                    corners_cm = corner[0] * scale_cm_per_px
                    
                    writer.writerow([
                        f"{timestamp:.3f}",
                        frame_idx,
                        int(marker_id[0]),
                        f"{center_cm[0]:.2f}",
                        f"{center_cm[1]:.2f}",
                        f"{angle:.2f}",
                        f"{corners_cm[0][0]:.2f}",
                        f"{corners_cm[0][1]:.2f}",
                        f"{corners_cm[1][0]:.2f}",
                        f"{corners_cm[1][1]:.2f}",
                        f"{corners_cm[2][0]:.2f}",
                        f"{corners_cm[2][1]:.2f}",
                        f"{corners_cm[3][0]:.2f}",
                        f"{corners_cm[3][1]:.2f}",
                    ])
            
            frame_idx += 1
            
            if frame_idx % max(1, total_frames // 10) == 0:
                progress = 100 * frame_idx / total_frames
                print(f"처리 중: {frame_idx}/{total_frames} ({progress:.1f}%)")
    
    cap.release()
    
    print("\n" + "=" * 70)
    print(f"✅ 완료! 결과: {output_csv}")
    print("=" * 70)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='마커 크기 기반 XY 캘리브레이션'
    )
    parser.add_argument('input', help='입력 비디오 파일')
    parser.add_argument('output', help='출력 CSV 파일')
    parser.add_argument('--marker-size', type=float, default=5.0,
                       help='마커 실제 크기 (cm, 기본값: 5.0)')
    
    args = parser.parse_args()
    
    try:
        calibrate_marker_tracking(args.input, args.output, args.marker_size)
    except Exception as e:
        print(f"❌ 에러: {e}")
        exit(1)
EOF
```

---

## 💻 사용 방법

### 방법 1: 간단히 실행

```bash
# 기본 (마커 크기 5cm 가정)
python scripts/simple_marker_calibration.py my_video.mov result.csv

# 또는 마커 크기 지정
python scripts/simple_marker_calibration.py my_video.mov result.csv --marker-size 10.0
```

### 방법 2: 위의 코드 블록을 직접 복사해서 실행

```bash
cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1
source venv/bin/activate

# 위의 Python 코드 붙여넣기 실행
```

---

## 📊 Excel에서 분석

생성된 CSV를 Excel에서 열면:

| timestamp_s | marker_id | center_x_cm | center_y_cm | rotation_angle_deg |
|-------------|-----------|-------------|-------------|-------------------|
| 0.000 | 0 | 13.65 | 10.24 | -2.35 |
| 0.033 | 0 | 13.71 | 10.31 | -2.10 |
| 0.067 | 0 | 13.77 | 10.38 | -1.85 |

**이제 모든 값이 실제 거리(cm)입니다!** ✨

---

## 🎯 속도 계산 예시

```excel
# Excel에 새 컬럼 추가: Velocity

= SQRT((C2-C3)^2 + (D2-D3)^2) / (A2-A3)

= 마커의 프레임 간 이동 거리 / 시간 차이
= cm/s 단위의 속도
```

---

## ✅ 정리

| 전에 | 지금 |
|-----|------|
| ❌ center_x_px = 512 | ✅ center_x_cm = 13.65 |
| ❌ center_y_px = 384 | ✅ center_y_cm = 10.24 |
| ❓ 무슨 단위? | ✅ cm 단위, 실제 거리! |

**필요한 것은 마커 실제 크기 하나뿐입니다!** 🎯
