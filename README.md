# ArUco Marker Tracker

비디오에서 ArUco 마커를 감지하고 위치/좌표를 CSV + 시각화 영상으로 저장합니다.

## 파일 구조

```
/
├── tracker.py        ← 메인 실행 스크립트
├── create_markers.py ← 마커 인쇄용 PDF 생성
├── markers/          ← 마커 이미지 (ID 0~49)
└── output/           ← 결과물 자동 저장 (csv, mp4)
```

## 사용법

### 1. 영상 분석

```bash
python tracker.py 영상파일.mov --marker-size 5.0
```

- `--marker-size` : 마커 실제 크기(cm). 기본값 1.0
- 결과는 `output/` 폴더에 자동 저장

**출력 파일:**
- `output/영상파일_tracked.mp4` — 마커 위치가 표시된 시각화 영상
- `output/영상파일_tracked.csv` — 프레임별 좌표 데이터

### 2. 마커 인쇄

```bash
python create_markers.py
```

- `print_1cm.pdf`, `print_1_5cm.pdf` 생성
- 인쇄 시 반드시 **100% 스케일** (크기 조정 없음)

## CSV 컬럼

| 컬럼 | 설명 |
|------|------|
| `timestamp_s` | 영상 시간(초) |
| `frame_number` | 프레임 번호 |
| `marker_id` | 마커 ID |
| `center_x_cm`, `center_y_cm` | 중심 좌표(cm) |
| `rotation_angle_deg` | 회전 각도(도) |
| `corner_0~3_x/y_cm` | 4개 꼭짓점 좌표(cm) |

## 요구사항

```bash
pip install opencv-contrib-python pillow
```
