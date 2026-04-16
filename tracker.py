#!/usr/bin/env python3
"""
ArUco 마커 트래커 (2-pass whitelist 방식)

동작 순서
--------
[Pass 1] 영상 전체를 스캔하여 마커 ID별 감지 횟수를 집계
         → 가장 많이 감지된 마커 대비 --whitelist-threshold(기본 20%)
            이상 감지된 ID만 "유효 마커"로 선정
[Pass 2] 유효 마커 ID만 필터링해서 CSV · 시각화 MP4 · Position PNG 생성

FPS / 슬로우모션 대응
--------------------
--target-fps (기본 60). 영상 FPS 가 target-fps 보다 크게 높으면 균일 샘플링
예) 240fps 슬로우모션 영상 + --target-fps 60  → 4프레임마다 1프레임 처리

사용법
-----
    python tracker.py 영상파일.mov --marker-size 1.0
    python tracker.py 영상파일.mov --marker-size 1.0 --target-fps 120
"""

import cv2
import numpy as np
import csv
import argparse
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # 디스플레이 없이 파일로만 저장
import matplotlib.pyplot as plt


# =====================================================================
# CLI
# =====================================================================
def main():
    parser = argparse.ArgumentParser(
        description="ArUco 마커 추적 + 시각화 영상 + Position Plot 생성 (2-pass whitelist)"
    )
    parser.add_argument("video_path", help="입력 비디오 파일 경로")
    parser.add_argument(
        "--marker-size",
        type=float,
        default=1.0,
        help="마커 크기 (cm, 기본값: 1.0)",
    )
    parser.add_argument(
        "--target-fps",
        type=float,
        default=60.0,
        help="분석 대상 FPS (기본 60). 영상 FPS가 더 높으면 균일 샘플링. "
             "예: 240fps 슬로우모션 영상은 stride=4 로 60fps 처리.",
    )
    parser.add_argument(
        "--whitelist-threshold",
        type=float,
        default=0.2,
        help="유효 마커 선정 기준 (최다 감지 마커 대비 비율, 기본 0.2 = 20%%)",
    )

    args = parser.parse_args()

    video_path = Path(args.video_path)
    if not video_path.exists():
        print(f"파일을 찾을 수 없음: {video_path}")
        return

    # output/ 폴더에 자동 저장
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    stem         = video_path.stem
    output_video = output_dir / f"{stem}_tracked.mp4"
    output_csv   = output_dir / f"{stem}_tracked.csv"
    output_plot  = output_dir / f"{stem}_position.png"

    print(f"입력 영상 : {video_path}")
    print(f"마커 크기 : {args.marker_size} cm")
    print(f"Target FPS: {args.target_fps}")
    print(f"결과 저장 : {output_dir}/")
    print()

    track(
        video_path=str(video_path),
        output_video_path=str(output_video),
        output_csv_path=str(output_csv),
        marker_size_cm=args.marker_size,
        target_fps=args.target_fps,
        whitelist_threshold=args.whitelist_threshold,
    )
    generate_position_plots(str(output_csv), str(output_plot), title=stem)
    print(f"  PNG:  {output_plot}")


# =====================================================================
# ArUco Detector (튜닝된 파라미터)
# =====================================================================
def _create_detector():
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    params = cv2.aruco.DetectorParameters()

    # --- Adaptive Threshold 튜닝 ---
    params.adaptiveThreshWinSizeMin  = 3
    params.adaptiveThreshWinSizeMax  = 53    # 기본 23 → 53
    params.adaptiveThreshWinSizeStep = 4     # 기본 10 → 4

    # --- 마커 크기 허용 범위 ---
    params.minMarkerPerimeterRate = 0.01     # 기본 0.03 → 0.01
    params.maxMarkerPerimeterRate = 4.0

    # --- 모션 블러 대응 ---
    params.polygonalApproxAccuracyRate = 0.05  # 기본 0.03 → 0.05

    # --- Corner Refinement: 서브픽셀 정확도 ---
    params.cornerRefinementMethod         = cv2.aruco.CORNER_REFINE_SUBPIX
    params.cornerRefinementWinSize        = 5
    params.cornerRefinementMaxIterations  = 30
    params.cornerRefinementMinAccuracy    = 0.1

    # --- Error Correction ---
    params.errorCorrectionRate = 1.0         # 기본 0.6 → 1.0

    return cv2.aruco.ArucoDetector(dictionary, params)


# =====================================================================
# Tracking: 2-pass (whitelist 학습 → 실제 추적)
# =====================================================================
def track(video_path, output_video_path, output_csv_path,
          marker_size_cm=1.0, target_fps=60.0, whitelist_threshold=0.2):
    detector_obj = _create_detector()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"비디오를 열 수 없음: {video_path}")
        return

    video_fps    = cap.get(cv2.CAP_PROP_FPS)
    width        = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Sampling stride: target_fps 기준 균일 샘플링
    stride         = max(1, round(video_fps / target_fps))
    effective_fps  = video_fps / stride
    sampled_frames = (total_frames + stride - 1) // stride

    print(f"해상도: {width}x{height}  영상 FPS: {video_fps:.2f}  총 프레임: {total_frames}")
    if stride > 1:
        print(f"샘플링: stride={stride} → 분석 FPS {effective_fps:.2f}, 처리 프레임 {sampled_frames}")
    else:
        print("샘플링 없음 (영상 FPS ≈ target FPS)")
    print()

    # ---------- Pass 1: Whitelist 학습 ----------
    print("[Pass 1/2] 전체 스캔으로 유효 마커 학습 중...")
    id_counts = defaultdict(int)
    frame_idx = 0
    processed = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % stride == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, ids, _ = detector_obj.detectMarkers(gray)
            if ids is not None:
                for mid in ids:
                    id_counts[int(mid[0])] += 1
            processed += 1
            if processed % max(1, sampled_frames // 5) == 0:
                pct = processed / sampled_frames * 100
                print(f"  {pct:.0f}% ({processed}/{sampled_frames})")
        frame_idx += 1

    if not id_counts:
        print("마커가 한 번도 감지되지 않았습니다.")
        cap.release()
        return

    max_count   = max(id_counts.values())
    threshold   = max(5, int(max_count * whitelist_threshold))
    allowed_ids = {mid for mid, cnt in id_counts.items() if cnt >= threshold}
    excluded    = {mid: cnt for mid, cnt in id_counts.items() if mid not in allowed_ids}

    allowed_info = {mid: id_counts[mid] for mid in sorted(allowed_ids)}
    print(f"  → 학습된 유효 마커 ({len(allowed_ids)}개): {allowed_info}")
    if excluded:
        print(f"  → 노이즈로 제외 ({len(excluded)}개): {dict(sorted(excluded.items()))}")
    print()

    # Pass 2를 위해 비디오 되감기
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # ---------- Pass 2: 실제 추적 + 저장 ----------
    print("[Pass 2/2] 유효 마커 추적 + CSV/MP4 저장 중...")
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    out    = cv2.VideoWriter(output_video_path, fourcc, effective_fps, (width, height))

    csv_file = open(output_csv_path, 'w', newline='')
    fieldnames = [
        'timestamp_s', 'frame_number', 'marker_id',
        'center_x_cm', 'center_y_cm', 'rotation_angle_deg',
        'corner_0_x_cm', 'corner_0_y_cm',
        'corner_1_x_cm', 'corner_1_y_cm',
        'corner_2_x_cm', 'corner_2_y_cm',
        'corner_3_x_cm', 'corner_3_y_cm',
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    scale_cm_per_px = None
    frame_idx = 0
    processed = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % stride != 0:
            frame_idx += 1
            continue

        frame_idx_actual = frame_idx
        timestamp        = frame_idx_actual / video_fps

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detector_obj.detectMarkers(gray_frame)

        # Whitelist 필터
        if ids is not None:
            keep = [i for i, mid in enumerate(ids) if int(mid[0]) in allowed_ids]
            if keep:
                corners = tuple(corners[i] for i in keep)
                ids = ids[keep]
            else:
                corners, ids = (), None

        # 첫 유효 감지 시점에 스케일 계산
        if scale_cm_per_px is None and ids is not None:
            c0 = corners[0]
            sides = [
                np.linalg.norm(c0[0][1] - c0[0][0]),
                np.linalg.norm(c0[0][2] - c0[0][1]),
                np.linalg.norm(c0[0][3] - c0[0][2]),
                np.linalg.norm(c0[0][0] - c0[0][3]),
            ]
            scale_cm_per_px = marker_size_cm / np.mean(sides)

        display_frame = frame.copy()
        markers_detected = False

        if ids is not None and scale_cm_per_px is not None:
            markers_detected = True

            for marker_idx, marker_id in enumerate(ids):
                corner = corners[marker_idx][0]

                center_px = np.mean(corner, axis=0)
                center_cm = center_px * scale_cm_per_px

                v1 = corner[1] - corner[0]
                angle = np.degrees(np.arctan2(v1[1], v1[0]))

                corners_cm = corner * scale_cm_per_px

                writer.writerow({
                    'timestamp_s':        f'{timestamp:.3f}',
                    'frame_number':       frame_idx_actual,
                    'marker_id':          int(marker_id[0]),
                    'center_x_cm':        f'{center_cm[0]:.2f}',
                    'center_y_cm':        f'{center_cm[1]:.2f}',
                    'rotation_angle_deg': f'{angle:.2f}',
                    'corner_0_x_cm':      f'{corners_cm[0][0]:.2f}',
                    'corner_0_y_cm':      f'{corners_cm[0][1]:.2f}',
                    'corner_1_x_cm':      f'{corners_cm[1][0]:.2f}',
                    'corner_1_y_cm':      f'{corners_cm[1][1]:.2f}',
                    'corner_2_x_cm':      f'{corners_cm[2][0]:.2f}',
                    'corner_2_y_cm':      f'{corners_cm[2][1]:.2f}',
                    'corner_3_x_cm':      f'{corners_cm[3][0]:.2f}',
                    'corner_3_y_cm':      f'{corners_cm[3][1]:.2f}',
                })

                # 시각화
                corner_int = corner.astype(np.int32)
                cv2.polylines(display_frame, [corner_int], True, (0, 255, 0), 2)
                cv2.circle(display_frame, (int(center_px[0]), int(center_px[1])), 5, (255, 0, 0), -1)
                cv2.putText(display_frame, f"ID:{int(marker_id[0])}",
                            (int(center_px[0]) + 10, int(center_px[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(display_frame, f"({center_cm[0]:.1f}, {center_cm[1]:.1f})cm",
                            (int(center_px[0]) + 10, int(center_px[1]) + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

        cv2.putText(display_frame,
                    f"Frame: {frame_idx_actual}/{total_frames}  {timestamp:.2f}s",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        status_text  = "Detected" if markers_detected else "No markers"
        status_color = (0, 255, 0) if markers_detected else (0, 0, 255)
        cv2.putText(display_frame, status_text,
                    (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

        out.write(display_frame)

        processed += 1
        if processed % max(1, sampled_frames // 10) == 0:
            pct = processed / sampled_frames * 100
            print(f"  {pct:.0f}% ({processed}/{sampled_frames})")

        frame_idx += 1

    cap.release()
    out.release()
    csv_file.close()

    print()
    print("완료!")
    print(f"  영상: {output_video_path}")
    print(f"  CSV:  {output_csv_path}")


# =====================================================================
# Position Plot (x, y vs frame) 생성
# =====================================================================
def generate_position_plots(csv_path, output_png_path, title=None, min_detection_ratio=0.2):
    """
    CSV 파일에서 마커별 x, y position plot 생성.
    (2-pass 방식에서 CSV는 이미 깨끗하므로 필터는 안전망 역할)
    """
    marker_data = defaultdict(lambda: {'frame': [], 'x': [], 'y': []})

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = int(row['marker_id'])
            marker_data[mid]['frame'].append(int(row['frame_number']))
            marker_data[mid]['x'].append(float(row['center_x_cm']))
            marker_data[mid]['y'].append(float(row['center_y_cm']))

    if not marker_data:
        print("  (plot 생략: CSV에 감지된 마커가 없음)")
        return

    # 안전망: 혹시라도 남은 극소수 false positive 제거
    max_count = max(len(d['frame']) for d in marker_data.values())
    threshold = max(5, int(max_count * min_detection_ratio))
    filtered = {mid: d for mid, d in marker_data.items() if len(d['frame']) >= threshold}
    excluded = [mid for mid in marker_data if mid not in filtered]
    if excluded:
        print(f"  (plot 필터링: {len(excluded)}개 제외 - ID {excluded})")

    display_title = title if title else Path(csv_path).stem
    fig, (ax_x, ax_y) = plt.subplots(2, 1, figsize=(10, 8))

    for mid in sorted(filtered.keys()):
        d = filtered[mid]
        label = f'Marker {mid}'
        ax_x.plot(d['frame'], d['x'], label=label, linewidth=1.5)
        ax_y.plot(d['frame'], d['y'], label=label, linewidth=1.5)

    ax_x.set_title(f'{display_title} — x position', fontsize=12, fontweight='bold')
    ax_x.set_xlabel('Frame')
    ax_x.set_ylabel('x position (cm)')
    ax_x.grid(True, linestyle='--', alpha=0.5)
    ax_x.legend(loc='best')

    ax_y.set_title(f'{display_title} — y position', fontsize=12, fontweight='bold')
    ax_y.set_xlabel('Frame')
    ax_y.set_ylabel('y position (cm)')
    ax_y.grid(True, linestyle='--', alpha=0.5)
    ax_y.legend(loc='best')

    plt.tight_layout()
    plt.savefig(output_png_path, dpi=120, bbox_inches='tight')
    plt.close(fig)


if __name__ == "__main__":
    main()
