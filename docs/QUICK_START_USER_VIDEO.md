# 📱 QUICK_START_USER_VIDEO - iPhone 영상 처리# 자신의 iPhone 영상 분석 가이드



iPhone에서 촬영한 영상으로 ArUco 추적을 하는 방법입니다.iPhone에서 촬영한 영상을 이 프로젝트로 분석하고 결과를 받는 완전한 방법입니다.



---## 📱 1단계: iPhone에서 영상 촬영



## 📹 iPhone 영상 준비### 권장 설정

```

### 1단계: iPhone에서 촬영카메라 설정:

1. 1cm (또는 원하는 크기) ArUco 마커를 인쇄✓ 동영상 포맷: 1080p 60fps (또는 슬로우모션 240fps)

2. 마커를 카메라 앞에 배치✓ 코덱: H.264 권장

3. 밝고 균일한 조명에서 촬영✓ 안정화: 활성화 (흔들림 방지)

4. **최소 5초 이상** 촬영✓ 해상도: 최대 해상도 권장

5. 카메라를 고정시킨 후 마커만 움직이면 좋음✓ 조명: 충분한 밝기 필수 (마커 인식을 위해)

```

### 촬영 팁

✅ **잘 촬영하기**:### 마커 배치 방법

- 밝은 실내 또는 야외```

- 마커가 완전히 보이도록마커가 항상 화면 내에 완전하게 들어오도록 배치:

- 손떨림 없이✓ 마커를 크기 있게 촬영 (너무 작지 않게)

- 마커와 배경의 명확한 대비✓ 마커가 프레임 경계로 잘리지 않게 주의

✓ 마커가 명확하고 밝게 보이도록

❌ **피해야 할 것**:✓ 배경은 마커와 색상이 대비되게 (검은 마커 + 밝은 배경)

- 너무 어두운 환경```

- 마커가 일부 가려짐

- 과도한 움직임## 💻 2단계: 영상 파일을 컴퓨터로 옮기기

- 복잡한 배경

### 방법 1: AirDrop (가장 간단)

---```

1. Mac에서 Finder 열기

## 💻 Mac으로 전송2. iPhone에서 영상 선택 → 공유 → AirDrop

3. Mac 선택

### 방법 1: AirDrop (가장 간단!)4. 다운로드 완료!

1. iPhone에서 파일 앱 열기```

2. 방금 촬영한 영상 선택

3. 공유 → AirDrop### 방법 2: USB 연결

4. Mac 선택```

5. Mac에 자동 저장됨1. iPhone을 USB로 Mac에 연결

2. Finder → 위치 → [iPhone 이름] 선택

### 방법 2: iTunes 동기화3. 파일 앱에서 DCIM 폴더 열기

1. iPhone을 Mac에 연결4. 영상 파일 복사 → Mac에 저장

2. Finder에서 iPhone 선택```

3. 사진 탭 → 동기화

4. Mac 포토 라이브러리에 저장### 방법 3: iCloud 클라우드

```

### 방법 3: iCloud1. iPhone: 설정 → iCloud → 사진 동기화

1. iPhone에서 설정 → iCloud2. Mac: 사진 앱에서 다운로드

2. 사진 → iCloud 포토 라이브러리 켜기3. Finder로 원본 파일 위치 찾기

3. Mac에서 같은 Apple 계정 로그인```

4. 사진 앱에서 다운로드

## 📂 3단계: 영상 파일을 프로젝트에 복사

---

### 파일 위치

## 🎬 영상 파일 확인```

프로젝트 루트에 직접 복사하거나 tests/videos/에 저장:

### 지원되는 형식

✅ **지원**:/Users/kim-kwon-woong/Visual_Studio/Python_26_1/

- MOV (iPhone 기본 형식)├── your_iphone_video.mov  ← 또는 여기

- MP4└── tests/

- AVI    └── videos/

- MKV        └── your_iphone_video.mov  ← 또는 여기

- FLV```

- WMV

### 터미널에서 복사

### 파일 정보 확인```bash

```bash# 예: 데스크톱에 있는 영상을 프로젝트에 복사

# 영상 길이, 해상도 확인cp ~/Desktop/my_video.mov /Users/kim-kwon-woong/Visual_Studio/Python_26_1/

python -c "

import cv2# 또는 tests/videos에 복사

v = cv2.VideoCapture('iphone_video.mov')cp ~/Desktop/my_video.mov /Users/kim-kwon-woong/Visual_Studio/Python_26_1/tests/videos/

fps = v.get(5)```

total_frames = int(v.get(7))

duration_sec = total_frames / fps## 🚀 4단계: 분석 실행

width = int(v.get(3))

height = int(v.get(4))### 4-1. 터미널 열기

print(f'길이: {duration_sec:.1f}초')```bash

print(f'해상도: {width}x{height}')# 1. 프로젝트 폴더로 이동

print(f'FPS: {fps}')cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1

"

```# 2. 가상환경 활성화

source venv/bin/activate

---

# 이제 준비 완료!

## 📏 마커 크기 측정```



### 정확하게 측정하기 (매우 중요!)### 4-2. 분석 명령 실행



1. **줄자 준비**#### 옵션 A: 기본 분석 (빠름)

   - 정확한 줄자 또는 캘리퍼```bash

   - 스마트폰 앱 (측정)는 부정확할 수 있음# 출력 파일명이 자동으로 생성됨

python scripts/aruco_tracker_with_video.py your_iphone_video.mov

2. **마커 측정**```

   - 마커의 가장자리를 정확히 측정

   - 가로 길이 측정 (예: 5.0cm)**결과**:

   - 세로 길이 측정 (예: 5.0cm)- `tracking_output.mp4` (시각화 영상)

   - 가로/세로가 같아야 함 (정사각형)- `tracking_log.csv` (로그 데이터)



3. **예시**#### 옵션 B: 출력 파일명 지정 (권장)

   ``````bash

   가로: ├─────┤ = 5.0cm# 원하는 이름으로 저장

   세로: ├─ 5.0cmpython scripts/aruco_tracker_with_video.py \

   ```  your_iphone_video.mov \

  my_analysis.mp4 \

### 측정 기록  my_analysis.csv

```bash```

# 사용할 마커 크기를 메모

# 예: 아래에 기록해두고 사용**결과**:

- `my_analysis.mp4`

# 마커 1: 1.0cm- `my_analysis.csv`

# 마커 2: 3.5cm  

# 마커 3: 5.2cm#### 옵션 C: 진행 상황 실시간 확인 (선택)

``````bash

# 콘솔에서 진행상황 보기

---python scripts/aruco_tracker_with_video.py \

  your_iphone_video.mov \

## 🚀 스크립트 실행  my_analysis.mp4 \

  my_analysis.csv 2>&1 | tee analysis_log.txt

### 준비 사항```

1. ✅ iPhone 영상을 Mac으로 전송 완료

2. ✅ 마커 크기 측정 완료### 4-3. 실행 중 콘솔 출력 예시

```

### 실행 방법[INFO] ArUco Tracker with Video Output initialized

  - Input: your_iphone_video.mov

#### 1단계: 가상환경 활성화  - Output video: my_analysis.mp4

```bash  - Output CSV: my_analysis.csv

cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1

source venv/bin/activate[VIDEO INFO]

```  - Resolution: 1920x1080

  - FPS: 60.0

#### 2단계: 스크립트 실행 (3가지 옵션)  - Total frames: 3600

  - Duration: 60.00 seconds

**옵션 A: 1cm 마커 (마커가 정확히 1cm일 때)**

```bash[PROCESSING VIDEO]

python scripts/aruco_tracker_1cm.py iphone_video.mov result.csv  - Processed 100/3600 frames

```  - Processed 200/3600 frames

  ...

**옵션 B: 정확한 크기 지정 (권장! ⭐)**  - Processed 3600/3600 frames

```bash

# 예: 5cm 마커[RESULTS]

python scripts/aruco_tracker_flexible.py iphone_video.mov result.csv --marker-size 5.0  - Frames processed: 3600

  - Total detections: 2847

# 예: 3.5cm 마커  - Output video: my_analysis.mp4

python scripts/aruco_tracker_flexible.py iphone_video.mov result.csv --marker-size 3.5  - Output CSV: my_analysis.csv



# 예: 10cm 마커[SUCCESS] Tracking complete!

python scripts/aruco_tracker_flexible.py iphone_video.mov result.csv --marker-size 10.0```

```

## 📊 5단계: 결과 확인

**옵션 C: 시각화 포함 (결과를 영상으로도 보고 싶을 때)**

```bash### 5-1. 분석 영상 보기

python scripts/aruco_tracker_with_video.py iphone_video.mov iphone_annotated.mp4 result.csv --marker-size 5.0```bash

```# 생성된 mp4 파일 재생

open my_analysis.mp4

#### 3단계: 완료 대기

```# 또는 QuickTime에서 열기

진행 상황이 표시됩니다:open -a QuickTime\ Player my_analysis.mp4

████████░░ 83% 완료...```

```

**화면에 표시되는 정보**:

---- 마커 ID (화면 왼쪽 상단)

- 마커 위치 (중심 좌표)

## 📊 결과 확인- 회전각 (도 단위)

- 프레임 번호 및 시간

### CSV 파일 열기- 감지된 마커 개수

```bash

# Excel/Numbers에서 열기### 5-2. CSV 데이터 분석

open result.csv

#### 5-2-1. Excel에서 열기

# 또는 미리보기```

head -5 result.csv1. Excel 실행

```2. 파일 → 열기 → my_analysis.csv

3. 데이터 보기 및 분석

### 결과 예시```

```csv

timestamp_s,frame_number,marker_id,center_x_cm,center_y_cm,rotation_angle_deg#### 5-2-2. CSV 구조 이해

0.000,0,0,10.25,8.50,-2.15```csv

0.033,1,0,10.31,8.58,-1.95timestamp_s    frame_number    marker_id    center_x_px    center_y_px    rotation_angle_deg    corner_0_x    ...

0.067,2,0,10.37,8.66,-1.750.000000       0              0            512.50         384.25         -2.35                490.12        ...

```0.016667       1              0            513.12         385.10         -2.10                490.74        ...

0.033333       2              0            513.74         385.95         -1.85                491.36        ...

### Python에서 분석```

```python

import pandas as pd**컬럼 설명**:

- `timestamp_s`: 프레임의 시간 (초)

df = pd.read_csv('result.csv')- `frame_number`: 프레임 번호 (0부터 시작)

- `marker_id`: ArUco marker ID (0~249)

# 기본 정보- `center_x_px`: 마커 중심 x 좌표 (픽셀)

print(f"감지된 프레임: {len(df)}")- `center_y_px`: 마커 중심 y 좌표 (픽셀)

print(f"마커 ID: {df['marker_id'].unique()}")- `rotation_angle_deg`: 마커 회전각 (도)

- `corner_0_x` ~ `corner_3_y`: 4개 코너 좌표

# 좌표 범위

print(f"X: {df['center_x_cm'].min():.2f} ~ {df['center_x_cm'].max():.2f} cm")#### 5-2-3. Excel에서 간단한 분석

print(f"Y: {df['center_y_cm'].min():.2f} ~ {df['center_y_cm'].max():.2f} cm")```

1. 데이터 필터링

# 이동 거리   - marker_id로 필터 (특정 마커만 보기)

dx = df['center_x_cm'].diff()   - timestamp_s 범위 지정 (특정 시간만)

dy = df['center_y_cm'].diff()

distance = (dx**2 + dy**2)**0.52. 그래프 만들기

print(f"총 이동 거리: {distance.sum():.2f} cm")   - X: timestamp_s

```   - Y: center_x_px 또는 center_y_px

   → 마커의 움직임 시각화

---

3. 속도 계산 (선택)

## 📊 Excel에서 그래프 만들기   - 새 컬럼: velocity_px_per_s

   - 공식: =SQRT((C2-C1)^2 + (D2-D1)^2) / (A2-A1)

### 1. CSV를 Excel에서 열기   → 프레임 간 이동 속도 계산

```bash```

open result.csv

```## 🔍 6단계: 결과 저장 및 정리



### 2. 그래프 만들기### 결과 파일 저장 위치

1. `timestamp_s`, `center_x_cm`, `center_y_cm` 선택```bash

2. 메뉴 → 삽입 → 그래프# 프로젝트 폴더에 바로 저장된 경우

3. 차트 유형: 산점도 또는 선 그래프ls -la *.mp4 *.csv

4. 완성!

# 또는 tests/results에 저장

### 3. 결과 해석cp my_analysis.* /Users/kim-kwon-woong/Visual_Studio/Python_26_1/tests/results/

- X축: 시간 (초)```

- Y축: 좌표 (cm)

- 궤적 확인 가능### 권장: 분석 폴더 만들기

```bash

---# 날짜별 폴더 만들기

mkdir -p analysis_results/2026-03-26

## ⚠️ 문제 해결

# 결과 이동

### 마커를 감지하지 못함mv my_analysis.* analysis_results/2026-03-26/



**원인 확인**:# 정리

1. 조명이 너무 어두움 → 더 밝은 곳에서 재촬영ls -la analysis_results/2026-03-26/

2. 마커 크기가 부정확함 → 줄자로 다시 측정```

3. 마커가 부분 가려짐 → 완전히 보이도록 재촬영

## 📈 7단계: 고급 분석 (선택)

**테스트**:

```bash### Python에서 CSV 분석

# 먼저 테스트 영상으로 시도```python

python scripts/aruco_tracker_1cm.py tests/videos/test_video_10s_3markers_small.mp4 test.csvimport csv



# 성공하면 → 자신의 iPhone 영상 시도# CSV 읽기

# 실패하면 → 환경 설정 재확인with open('my_analysis.csv', 'r') as f:

```    reader = csv.DictReader(f)

    detections = list(reader)

### 크기가 부정확함

```bash# 마커별 통계

# 마커를 다시 측정하고 --marker-size 값 조정marker_0_data = [d for d in detections if int(d['marker_id']) == 0]

python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 4.95print(f"Marker 0: {len(marker_0_data)} 감지")

```

# 위치 변화

### 영상이 너무 크거나 처리가 느림if marker_0_data:

```bash    x_values = [float(d['center_x_px']) for d in marker_0_data]

# FFmpeg로 해상도 줄이기 (선택사항)    print(f"X 범위: {min(x_values):.0f} ~ {max(x_values):.0f} px")

ffmpeg -i iphone_video.mov -vf scale=720:480 smaller_video.mov```



# 줄어든 영상 처리### Pandas 설치 (고급 분석용)

python scripts/aruco_tracker_flexible.py smaller_video.mov result.csv --marker-size 5.0```bash

```pip install pandas matplotlib



---# 그래프 그리기

python3 << 'EOF'

## 💡 팁import pandas as pd

import matplotlib.pyplot as plt

### 여러 iPhone 영상 처리

```bashdf = pd.read_csv('my_analysis.csv')

# 폴더의 모든 MOV 파일 처리

for video in *.mov; do# 마커 0만 필터

    output="${video%.mov}.csv"marker_0 = df[df['marker_id'] == 0]

    python scripts/aruco_tracker_flexible.py "$video" "$output" --marker-size 5.0

done# 그래프

```plt.figure(figsize=(12, 6))

plt.plot(marker_0['timestamp_s'], marker_0['center_x_px'], label='X')

### 배치 처리 결과 확인plt.plot(marker_0['timestamp_s'], marker_0['center_y_px'], label='Y')

```bashplt.xlabel('Time (s)')

# 모든 CSV 파일 목록plt.ylabel('Position (px)')

ls *.csvplt.legend()

plt.savefig('marker_0_trajectory.png')

# 결과 통합 (Python)print("그래프 저장: marker_0_trajectory.png")

import pandas as pdEOF

import os```



dfs = []## 🐛 문제 해결

for csv_file in os.listdir('.'):

    if csv_file.endswith('.csv'):### Q1: "모듈을 찾을 수 없음" 에러

        df = pd.read_csv(csv_file)```

        df['source'] = csv_file에러: ModuleNotFoundError: No module named 'cv2'

        dfs.append(df)

해결:

combined = pd.concat(dfs, ignore_index=True)1. 가상환경 활성화 확인: source venv/bin/activate

combined.to_csv('combined_results.csv', index=False)2. 패키지 설치: pip install -r requirements.txt

print(f"✅ {len(dfs)}개 파일 통합 완료")3. 다시 실행

``````



---### Q2: 마커 감지가 안 됨

```

**이제 iPhone 영상으로 추적을 시작하세요!** 🎬📱해결 순서:

1. 영상 밝기 확인 (너무 어두우면 감지 불가)
2. 마커가 완전히 프레임 내에 있는지 확인
3. 마커 크기 확인 (너무 작으면 감지 어려움)
4. 배경과 마커의 색상 대비 확인
```

### Q3: 처리가 느림
```
원인: 해상도가 높거나 영상이 길다

해결 방법:
1. 영상 크기 축소 (ffmpeg 사용)
   ffmpeg -i input.mov -vf scale=1280:720 output.mov

2. 또는 원본 영상이 이미 최적화된 크기인지 확인
```

### Q4: MP4 재생이 안 됨
```
VLC 플레이어 설치 (모든 코덱 지원):
brew install vlc

또는:
open -a VLC my_analysis.mp4
```

## ✅ 완전한 워크플로우 예시

```bash
# 1. 터미널 열기 및 프로젝트 진입
cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1
source venv/bin/activate

# 2. 영상 확인
ls -lh *.mov

# 3. 분석 실행 (1분 영상 기준: 약 5~10초 소요)
python scripts/aruco_tracker_with_video.py my_video.mov result_video.mp4 result_data.csv

# 4. 결과 확인
open result_video.mp4           # 영상 재생
open result_data.csv            # Excel에서 분석

# 5. 결과 정리
mv result_video.mp4 result_data.csv tests/results/
```

## 📌 요점 정리

| 단계 | 작업 | 소요 시간 |
|------|------|--------|
| 1 | iPhone 촬영 | 1~5분 |
| 2 | 파일 전송 (AirDrop) | 1분 |
| 3 | 프로젝트에 복사 | 30초 |
| 4 | 분석 실행 | 영상 길이의 10% |
| 5 | 결과 확인 | 2~5분 |
| **총합** | - | **15~30분** |

---

**이제 완전한 분석 파이프라인을 시작할 수 있습니다!** 🎉

궁금한 점이나 추가 도움이 필요하면 알려주세요.
