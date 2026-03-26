# 🎯 QUICK_START_1CM - 1cm 마커 설정# ArUco 마커 추적 - 간단한 사용법



**1cm 마커**를 사용하는 가장 간단한 방법입니다.## 🎯 한 줄 요약



---```bash

python scripts/aruco_tracker_1cm.py your_video.mov result.csv

## ✅ 1cm 마커 준비```



### 마커 인쇄**끝!** ✅

1. `marker/aruco_marker_0.png` 열기

2. **100% 스케일**로 인쇄 (매우 중요!)---

3. 정확히 **1cm × 1cm** 크기 확인

## 🔧 마커 크기 변경하기

### 마커 크기 확인

```bash### 현재 설정

# 줄자로 측정- 마커 크기: **1cm × 1cm** (고정)

# 1cm 마커는 정확히 1.0cm × 1.0cm이어야 함

# 가로: 1.0cm ✅### 마커 크기를 변경할 때

# 세로: 1.0cm ✅

```**방법 1: 가장 간단한 방법** (권장)



---마커 크기를 변경하면, 스크립트를 다시 생성하는 가장 간단한 방법:



## 🚀 사용 방법```bash

cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1

### 1단계: 영상 촬영

- iPhone 또는 카메라로 영상 촬영# 스크립트 편집 (VS Code 또는 nano)

- 1cm 마커를 화면에 보이도록nano scripts/aruco_tracker_1cm.py

- 최소 5초 이상 촬영

# 3번 줄을 찾아서 변경:

### 2단계: 파일 준비# 현재:

```bashMARKER_SIZE_CM = 1.0  # 고정값

# 영상을 프로젝트 폴더로 복사

cp ~/Desktop/my_video.mov .# 변경 예 (5cm로 변경할 경우):

```MARKER_SIZE_CM = 5.0  # 고정값



### 3단계: 스크립트 실행# 저장: Ctrl+O → Enter → Ctrl+X

```bash```

# 가상환경 활성화

source venv/bin/activate**방법 2: VS Code에서 편집**



# 스크립트 실행```

python scripts/aruco_tracker_1cm.py my_video.mov result.csv1. VS Code 열기

```2. scripts/aruco_tracker_1cm.py 클릭

3. 찾기: Ctrl+F → "MARKER_SIZE_CM" 검색

### 4단계: 결과 확인4. "1.0" → 원하는 크기로 변경 (예: "5.0")

```bash5. 저장: Cmd+S

# CSV 파일 열기```

open result.csv

**방법 3: 터미널에서 변경**

# 또는 Python에서 분석

python -c "import pandas as pd; df=pd.read_csv('result.csv'); print(df.head())"```bash

```# 마커 크기 2cm로 변경

sed -i '' 's/MARKER_SIZE_CM = 1.0/MARKER_SIZE_CM = 2.0/' scripts/aruco_tracker_1cm.py

---

# 확인

## 📊 결과 해석grep "MARKER_SIZE_CM" scripts/aruco_tracker_1cm.py

```

### CSV 컬럼

| 컬럼 | 의미 |### 변경 위치 정확히 알려드림

|------|------|

| `timestamp_s` | 영상 재생 시간 (초) |**scripts/aruco_tracker_1cm.py 파일의 14번 줄**:

| `marker_id` | 마커 ID (0~249) |

| `center_x_cm` | 마커 중심 X 좌표 (cm) |```python

| `center_y_cm` | 마커 중심 Y 좌표 (cm) |def calibrate_and_track(video_path, output_csv):

| `rotation_angle_deg` | 마커 회전 각도 (도) |    """

    1cm × 1cm 마커를 기준으로 XY 좌표를 cm로 변환하면서 추적

### 예시 데이터    """

```csv    

timestamp_s,marker_id,center_x_cm,center_y_cm,rotation_angle_deg    MARKER_SIZE_CM = 1.0  # ← 여기를 변경! 이 숫자를 바꾸면 됨

0.000,0,15.32,12.45,-1.25```

0.033,0,15.38,12.52,-1.00

0.067,0,15.44,12.59,-0.75---

0.100,0,15.50,12.66,-0.50

```## 📝 변경 예시



**해석**:### 예시 1: 2cm × 2cm 마커로 변경

- 마커 0이 감지됨

- X 좌표: 약 15cm```python

- Y 좌표: 약 12.5cmMARKER_SIZE_CM = 2.0  # 2cm × 2cm로 변경

- 조금씩 이동 중```



---```bash

python scripts/aruco_tracker_1cm.py video.mov result.csv

## 🎨 다른 크기 마커로 변경```



**1cm이 아닌 다른 크기를 사용하려면?**결과:

```

### 방법 1: 유연한 스크립트 사용 (권장!)마커 크기: 2.0 cm × 2.0 cm (변경됨)

```bash```

# 2cm 마커

python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 2.0### 예시 2: 5cm × 5cm 마커로 변경



# 5cm 마커```python

python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 5.0MARKER_SIZE_CM = 5.0  # 5cm × 5cm로 변경

```

# 10cm 마커

python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 10.0```bash

```python scripts/aruco_tracker_1cm.py video.mov result.csv

```

### 방법 2: 마커를 1cm로 조정

- 마커를 축소/확대 인쇄결과:

- 다시 정확히 1cm로 만들기```

- 같은 스크립트 사용마커 크기: 5.0 cm × 5.0 cm (변경됨)

```

---

### 예시 3: 10cm × 10cm 마커로 변경

## ⚠️ 주의사항

```python

### 정확한 1cm 확인MARKER_SIZE_CM = 10.0  # 10cm × 10cm로 변경

- 줄자로 **정확히** 측정```

- 1.0cm ± 0.1cm 범위 내

- 작으면 결과가 부정확함```bash

python scripts/aruco_tracker_1cm.py video.mov result.csv

### 조명```

- 밝은 환경에서 촬영

- 마커와 배경의 명확한 대비결과:

- 그림자가 없도록```

마커 크기: 10.0 cm × 10.0 cm (변경됨)

### 마커 가시성```

- 마커가 완전히 프레임에 보여야 함

- 일부 가려지면 감지 안 됨---

- 정면을 향하도록 배치

## ✅ 변경 확인

---

변경한 후 반드시 확인하세요:

## 🆘 문제 해결

```bash

### 마커를 감지하지 못함# 변경이 제대로 되었는지 확인

```bashgrep "MARKER_SIZE_CM" scripts/aruco_tracker_1cm.py

# 1. 조명 확인

# → 더 밝은 환경에서 촬영# 출력 예시:

# MARKER_SIZE_CM = 5.0  # 고정값

# 2. 마커 크기 확인```

# → 정확히 1.0cm인지 줄자로 재측정

---

# 3. 마커 ID 확인

# → marker/ 폴더에서 다른 ID 시도## 🚨 주의사항

python scripts/aruco_tracker_1cm.py video.mov result.csv

```### 중요!



### CSV가 비어있음1. **반드시 정확한 마커 크기 입력**

```bash   - 줄자로 측정한 정확한 크기를 입력

# 마커가 감지되지 않음   - 예: 5.23cm → 5.23 입력 (가능)

# 위의 "마커를 감지하지 못함" 참고

2. **스크립트 실행 전에 변경**

# 또는 영상 확인   - 파일 저장 후 → 스크립트 실행

python -c "import cv2; v=cv2.VideoCapture('video.mov'); print(f'프레임: {int(v.get(7))}')"

```3. **여러 크기의 마커를 사용할 경우**

   - 매번 크기를 변경하고 스크립트 실행

---   - 또는 자동화 스크립트 사용 (아래 참조)



## 💡 팁---



### 마커 ID 변경## 🤖 자동화: 마커 크기 파라미터로 넘기기 (권장!)

```bash

# 다른 마커 ID 사용**파일 수정 없이 매번 크기를 지정**하는 가장 편한 방법:

# marker/aruco_marker_1.png 사용

# marker/aruco_marker_2.png 사용```bash

# ...python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 5.0

# marker/aruco_marker_49.png 사용```



# 스크립트는 자동으로 감지함### 사용 예시

```

```bash

### 여러 마커 동시 추적# 1cm × 1cm 마커 (기본값)

```bashpython scripts/aruco_tracker_flexible.py video.mov result.csv

# 1cm 마커 여러 개를 영상에 배치

# 각 마커는 다른 ID 사용 (예: 0, 1, 2)# 2cm × 2cm 마커

# CSV에 marker_id로 구분됨python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 2.0



python scripts/aruco_tracker_1cm.py multi_marker_video.mov result.csv# 5cm × 5cm 마커

```python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 5.0



결과:# 3.5cm × 3.5cm 마커 (소수점도 가능)

```csvpython scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 3.5

timestamp_s,marker_id,...```

0.000,0,15.32,12.45

0.000,1,25.50,8.30### 출력 확인

0.000,2,10.10,20.15

``````

===============================================================================

---✅ ArUco 마커 추적 (유연한 크기 지정)

===============================================================================

**준비됐으면 시작하세요!** 🎬마커 크기: 5.0 cm × 5.0 cm

영상에서 측정된 픽셀 크기: 187.45 px
스케일 팩터: 0.026638 cm/px
또는: 37.45 px/cm
===============================================================================
```

---

## 📋 3가지 방법 비교

| 방법 | 코드 | 장점 | 단점 |
|------|------|------|------|
| **방법 1: 고정 1cm** | `python scripts/aruco_tracker_1cm.py video.mov result.csv` | 가장 간단 | 1cm만 사용 가능 |
| **방법 2: 파일 편집** | 파일 수정 후 실행 | 간단함 | 매번 수정 필요 |
| **방법 3: 파라미터** | `python scripts/aruco_tracker_flexible.py video.mov result.csv --marker-size 5.0` | **가장 편함** ✨ | 명령어 조금 길음 |

**추천: 방법 3 (파라미터 방식)** - 가장 유연하고 편합니다! ✅

---

## 💻 사용 방법

### 1단계: 터미널 열기

```bash
cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1
source venv/bin/activate
```

### 2단계: 스크립트 실행

```bash
python scripts/aruco_tracker_1cm.py your_video.mov result.csv
```

**출력 예시**:
```
======================================================================
✅ ArUco 마커 추적 (1cm × 1cm 고정)
======================================================================
마커 크기: 1.0 cm × 1.0 cm (고정)
영상에서 측정된 픽셀 크기: 37.45 px
스케일 팩터: 0.026714 cm/px
또는: 37.45 px/cm
======================================================================

진행: 30/300 (10.0%) | 감지: 28
진행: 60/300 (20.0%) | 감지: 56
진행: 90/300 (30.0%) | 감지: 84
...

======================================================================
✅ 추적 완료!
출력 파일: result.csv
총 감지 횟수: 287
평균 감지율: 95.7%
======================================================================
```

### 3단계: 결과 확인

```bash
# 첫 5줄 확인
head -5 result.csv

# Excel에서 열기
open result.csv
```

**CSV 내용**:
```csv
timestamp_s,frame_number,marker_id,center_x_cm,center_y_cm,rotation_angle_deg,...
0.000,0,0,13.65,10.24,-2.35,...
0.033,1,0,13.71,10.31,-2.10,...
0.067,2,0,13.77,10.38,-1.85,...
```

---

## 📊 결과 해석

| 컬럼 | 의미 | 예시 |
|------|------|------|
| `timestamp_s` | 시간 (초) | 0.000, 0.033, 0.067 |
| `frame_number` | 프레임 번호 | 0, 1, 2 |
| `marker_id` | 마커 ID | 0, 1, 2, ... |
| `center_x_cm` | X 좌표 (cm) | 13.65 |
| `center_y_cm` | Y 좌표 (cm) | 10.24 |
| `rotation_angle_deg` | 회전 각도 (도) | -2.35 |
| `corner_*_x_cm` | 코너 X 좌표 (cm) | - |
| `corner_*_y_cm` | 코너 Y 좌표 (cm) | - |

---

## 🎨 Excel에서 분석

### 1. 마커 궤적 그래프

```
1. result.csv 열기
2. center_x_cm, center_y_cm 선택
3. 삽입 → 그래프 → 산점도
4. 마커의 움직임이 시각화됨!
```

### 2. 시간별 위치 변화

```
1. timestamp_s를 X축
2. center_x_cm 또는 center_y_cm를 Y축
3. 선 그래프로 시간에 따른 움직임 표현
```

### 3. 속도 계산 (선택)

```excel
새 컬럼: velocity_cm_per_s

공식: =SQRT((C2-C3)^2 + (D2-D3)^2) / (A2-A3)

설명:
  C2 = center_x_cm (현재 프레임)
  C3 = center_x_cm (이전 프레임)
  D2 = center_y_cm (현재 프레임)
  D3 = center_y_cm (이전 프레임)
  A2 = timestamp_s (현재 프레임)
  A3 = timestamp_s (이전 프레임)
```

---

## 🧪 테스트 실행

프로젝트에 포함된 테스트 비디오로 시험해보세요:

```bash
# 테스트 비디오로 실행
python scripts/aruco_tracker_1cm.py tests/videos/test_video_10s_3markers_small.mp4 tests/results/test_1cm_result.csv

# 결과 확인
head -10 tests/results/test_1cm_result.csv
```

**예상 결과**:
```
✅ 추적 완료!
출력 파일: tests/results/test_1cm_result.csv
총 감지 횟수: 287
평균 감지율: 95.7%
```

---

## 🚀 실제 iPhone 영상 처리

### 1. iPhone에서 영상 촬영
- 마커를 1cm × 1cm로 준비
- iPhone으로 촬영 → AirDrop으로 전송

### 2. 마커 크기 확인
```bash
# 마커가 정말 1cm × 1cm인지 확인
# (줄자로 측정)
```

### 3. 처리 실행
```bash
python scripts/aruco_tracker_1cm.py iphone_video.mov result.csv
```

### 4. 결과 분석
```bash
# 또는 Excel에서 열기
open result.csv
```

---

## 🐛 문제 해결

### Q1: "마커를 감지할 수 없음" 에러

```
해결:
1. 마커가 영상에 제대로 보이는지 확인
2. 조명이 충분한지 확인
3. 마커가 완전히 프레임 내에 들어오는지 확인
```

### Q2: 좌표값이 이상함

```
확인할 것:
1. 마커 크기가 정말 1cm × 1cm인가?
2. 영상이 올바른 파일인가?
3. 첫 프레임에서 마커가 보이는가?
```

### Q3: "파일을 열 수 없음" 에러

```
해결:
cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1
source venv/bin/activate
# 다시 실행
```

---

## 📋 체크리스트

- [ ] 마커 크기를 1cm × 1cm로 준비
- [ ] venv 활성화 (`source venv/bin/activate`)
- [ ] 영상 파일 준비
- [ ] 스크립트 실행
- [ ] result.csv 생성 확인
- [ ] Excel에서 분석

---

## 💡 팁

### 정확한 마커 크기 확인
```
1. A4 용지에 marker_0.png 인쇄
2. 줄자로 측정 (정확히 1cm × 1cm인지)
3. 이 마커로 촬영
```

### 빠른 테스트
```bash
# 포함된 테스트 영상으로 먼저 시험
python scripts/aruco_tracker_1cm.py tests/videos/test_video_10s_3markers_small.mp4 test_result.csv
```

### 배치 처리 (여러 영상)
```bash
for video in *.mov; do
    output="${video%.mov}_result.csv"
    python scripts/aruco_tracker_1cm.py "$video" "$output"
done
```

---

## 🎯 정리

| 항목 | 내용 |
|------|------|
| 마커 크기 | 1cm × 1cm (고정) |
| 필요한 입력 | 영상 파일 하나 |
| 자동으로 계산 | 스케일 팩터 |
| 결과 | CSV 파일 (cm 단위) |
| 소요 시간 | 1분 영상 기준 약 5초 |

---

**이제 정말 간단합니다!** 🎉

궁금한 점이 있으면 알려주세요.
