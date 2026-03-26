# 🚀 START HERE - 30초 빠른 시작# ArUco 마커 추적 - 빠른 시작 가이드



이 문서는 **가장 빠르게 시작**하기 위한 가이드입니다.## 🎯 30초 요약



---```bash

# 1. 프로젝트 폴더로 가기

## ⚡ 3단계 시작 (30초)cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1



### 1️⃣ 가상환경 활성화 (5초)# 2. 가상환경 활성화

```bashsource venv/bin/activate

cd /Users/kim-kwon-woong/Visual_Studio/Python_26_1

source venv/bin/activate# 3. 실행 (마커 크기 1cm)

```python scripts/aruco_tracker_1cm.py your_video.mov result.csv



### 2️⃣ 스크립트 실행 (10초)# 4. 결과 보기

```bashopen result.csv

# 방법 1: 1cm 마커 (가장 간단!)```

python scripts/aruco_tracker_1cm.py your_video.mov result.csv

**끝!** ✅

# 방법 2: 마커 크기 지정 (권장!)

python scripts/aruco_tracker_flexible.py your_video.mov result.csv --marker-size 5.0---

```

## 📊 결과 파일 구조

### 3️⃣ 결과 확인 (5초)

```bash```

open result.csv  # Excel에서 열기result.csv 파일이 생성됨:

```

timestamp_s  marker_id  center_x_cm  center_y_cm  rotation_angle_deg

---0.000        0          13.65        10.24        -2.35

0.033        0          13.71        10.31        -2.10

## 📊 그게 끝!0.067        0          13.77        10.38        -1.85

             ↑          ↑ 시간      ↑ X좌표(cm)  ↑ Y좌표(cm)

`result.csv`에 마커 좌표가 저장되었습니다:```



```csv---

timestamp_s  marker_id  center_x_cm  center_y_cm  rotation_angle_deg

0.000        0          13.65        10.24        -2.35## 🔧 마커 크기 변경

0.033        0          13.71        10.31        -2.10

```### 1cm가 아닌 다른 크기일 때



---```bash

# 2cm 마커

## 🎬 테스트 영상으로 먼저 해보고 싶으면?python scripts/aruco_tracker_flexible.py your_video.mov result.csv --marker-size 2.0



```bash# 5cm 마커

# 바로 테스트 가능!python scripts/aruco_tracker_flexible.py your_video.mov result.csv --marker-size 5.0

python scripts/aruco_tracker_1cm.py tests/videos/test_video_10s_3markers_small.mp4 test_result.csv

open test_result.csv# 3.5cm 마커

```python scripts/aruco_tracker_flexible.py your_video.mov result.csv --marker-size 3.5

```

---

---

## ❓ 더 알고 싶으면?

## 📝 파일별 설명

- **상세 가이드**: `docs/USAGE_GUIDE.md` 읽기

- **iPhone 영상 처리**: `docs/QUICK_START_USER_VIDEO.md`| 파일 | 용도 |

- **마커 크기 변경**: `docs/QUICK_START_1CM.md`|------|------|

- **문제 해결**: `README.md`의 🆘 섹션| `aruco_tracker_1cm.py` | 1cm 마커 전용 (간단) |

| `aruco_tracker_flexible.py` | 크기 변경 가능 (권장!) |

---| `result.csv` | 결과 데이터 (Excel 열기) |



**이제 시작하세요!** 🎯---


## ✅ 체크리스트

- [ ] 마커 크기 측정 (줄자로 정확히)
- [ ] 영상 촬영 (iPhone에서)
- [ ] 컴퓨터에 복사
- [ ] `source venv/bin/activate` 실행
- [ ] 스크립트 실행
- [ ] `result.csv` 열기 (Excel)

---

## 🚨 에러 해결

| 에러 | 해결책 |
|------|--------|
| "마커를 감지할 수 없음" | 영상이 밝은지, 마커가 완전히 보이는지 확인 |
| "파일을 열 수 없음" | 영상 파일명 확인, `cd` 명령어로 폴더 이동 |
| "module not found" | `source venv/bin/activate` 실행했는지 확인 |

---

## 💡 한 줄 팁

```bash
# 첫 5줄만 보기
head -5 result.csv

# 폴더에서 csv 파일 모두 보기
ls -lh *.csv

# 이전 결과 폴더에 저장
mv result.csv tests/results/
```

---

**더 자세한 내용은 `docs/QUICK_START_1CM.md` 참고** 📖
