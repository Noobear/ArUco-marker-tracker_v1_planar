#!/usr/bin/env python3
"""
ArUco Marker Tracker with Video Output
비디오 파일에서 ArUco 마커를 감지하고 추적하며, 시각화 영상을 생성합니다.
"""

import cv2
import numpy as np
import csv
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="ArUco 마커 추적 + 시각화 영상 생성"
    )
    parser.add_argument("video_path", help="입력 비디오 파일 경로")
    parser.add_argument("output_video", help="출력 영상 파일 경로 (MP4)")
    parser.add_argument("output_csv", help="출력 CSV 파일 경로")
    parser.add_argument(
        "--marker-size",
        type=float,
        default=1.0,
        help="마커 크기 (cm, 기본값: 1.0)"
    )
    
    args = parser.parse_args()
    
    video_path = Path(args.video_path)
    output_video = Path(args.output_video)
    output_csv = Path(args.output_csv)
    marker_size_cm = args.marker_size
    
    # 입력 비디오 확인
    if not video_path.exists():
        print(f"❌ 파일을 찾을 수 없음: {video_path}")
        return
    
    print(f"📹 입력 비디오: {video_path}")
    print(f"📊 출력 CSV: {output_csv}")
    print(f"📹 출력 영상: {output_video}")
    print(f"📏 마커 크기: {marker_size_cm}cm")
    print()
    
    calibrate_and_track_with_video(
        str(video_path),
        str(output_video),
        str(output_csv),
        marker_size_cm
    )


def calibrate_and_track_with_video(
    video_path: str,
    output_video_path: str,
    output_csv_path: str,
    marker_size_cm: float = 1.0
) -> None:
    """
    비디오에서 ArUco 마커를 추적하고 시각화 영상을 생성합니다.
    
    Args:
        video_path: 입력 비디오 경로
        output_video_path: 출력 영상 경로
        output_csv_path: 출력 CSV 경로
        marker_size_cm: 마커 크기 (cm)
    """
    
    # ArUco 초기화
    detector = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    params = cv2.aruco.DetectorParameters()
    detector_obj = cv2.aruco.ArucoDetector(detector, params)
    
    # 비디오 열기
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ 비디오를 열 수 없음: {video_path}")
        return
    
    # 비디오 정보
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"✅ 비디오 로드 완료")
    print(f"   해상도: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   총 프레임: {total_frames}")
    print()
    
    # 출력 비디오 설정
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    # CSV 파일 준비
    csv_file = open(output_csv_path, 'w', newline='')
    fieldnames = [
        'timestamp_s', 'frame_number', 'marker_id',
        'center_x_cm', 'center_y_cm', 'rotation_angle_deg',
        'corner_0_x_cm', 'corner_0_y_cm',
        'corner_1_x_cm', 'corner_1_y_cm',
        'corner_2_x_cm', 'corner_2_y_cm',
        'corner_3_x_cm', 'corner_3_y_cm'
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    # 첫 프레임에서 스케일 계산
    scale_cm_per_px = None
    frame_idx = 0
    
    print("🔍 마커 감지 및 추적 중...")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame_idx_actual = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
        timestamp = frame_idx_actual / fps
        
        # 마커 감지
        corners, ids, rejected = detector_obj.detectMarkers(frame)
        
        # 첫 감지 시 스케일 계산
        if scale_cm_per_px is None and ids is not None:
            corner = corners[0]
            
            side1 = np.linalg.norm(corner[0][1] - corner[0][0])
            side2 = np.linalg.norm(corner[0][2] - corner[0][1])
            side3 = np.linalg.norm(corner[0][3] - corner[0][2])
            side4 = np.linalg.norm(corner[0][0] - corner[0][3])
            
            marker_size_px = np.mean([side1, side2, side3, side4])
            scale_cm_per_px = marker_size_cm / marker_size_px
        
        # 시각화 프레임 준비 (복사본)
        display_frame = frame.copy()
        
        # 마커가 감지되었는지 확인
        markers_detected = False
        
        if ids is not None and scale_cm_per_px is not None:
            markers_detected = True
            
            for marker_idx, marker_id in enumerate(ids):
                corner = corners[marker_idx][0]
                
                # 중심 계산
                center_px = np.mean(corner, axis=0)
                center_cm = center_px * scale_cm_per_px
                
                # 회전 각도 계산
                v1 = corner[1] - corner[0]
                angle = np.degrees(np.arctan2(v1[1], v1[0]))
                
                # cm 단위 코너
                corners_cm = corner * scale_cm_per_px
                
                # CSV 작성
                writer.writerow({
                    'timestamp_s': f'{timestamp:.3f}',
                    'frame_number': frame_idx_actual,
                    'marker_id': int(marker_id[0]),
                    'center_x_cm': f'{center_cm[0]:.2f}',
                    'center_y_cm': f'{center_cm[1]:.2f}',
                    'rotation_angle_deg': f'{angle:.2f}',
                    'corner_0_x_cm': f'{corners_cm[0][0]:.2f}',
                    'corner_0_y_cm': f'{corners_cm[0][1]:.2f}',
                    'corner_1_x_cm': f'{corners_cm[1][0]:.2f}',
                    'corner_1_y_cm': f'{corners_cm[1][1]:.2f}',
                    'corner_2_x_cm': f'{corners_cm[2][0]:.2f}',
                    'corner_2_y_cm': f'{corners_cm[2][1]:.2f}',
                    'corner_3_x_cm': f'{corners_cm[3][0]:.2f}',
                    'corner_3_y_cm': f'{corners_cm[3][1]:.2f}'
                })
                
                # 시각화: 마커 테두리 그리기 (초록색)
                corner_int = corner.astype(np.int32)
                cv2.polylines(display_frame, [corner_int], True, (0, 255, 0), 2)
                
                # 시각화: 마커 중심 그리기 (파란색 원)
                cv2.circle(
                    display_frame,
                    (int(center_px[0]), int(center_px[1])),
                    5, (255, 0, 0), -1
                )
                
                # 시각화: 마커 ID 텍스트
                cv2.putText(
                    display_frame,
                    f"ID:{int(marker_id[0])}",
                    (int(center_px[0]) + 10, int(center_px[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )
                
                # 시각화: 좌표 텍스트 (cm)
                cv2.putText(
                    display_frame,
                    f"({center_cm[0]:.1f}, {center_cm[1]:.1f})cm",
                    (int(center_px[0]) + 10, int(center_px[1]) + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    1
                )
        
        # 프레임 정보 표시
        cv2.putText(
            display_frame,
            f"Frame: {frame_idx_actual}/{total_frames} | Time: {timestamp:.2f}s",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        # 감지 상태 표시
        status_text = "✓ Detected" if markers_detected else "○ No markers"
        status_color = (0, 255, 0) if markers_detected else (0, 0, 255)
        cv2.putText(
            display_frame,
            status_text,
            (10, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            status_color,
            2
        )
        
        # 출력 비디오에 쓰기
        out.write(display_frame)
        
        # 진행 상황 표시
        if frame_idx_actual % max(1, total_frames // 10) == 0:
            progress = (frame_idx_actual / total_frames) * 100
            print(f"   진행: {progress:.0f}% ({frame_idx_actual}/{total_frames})")
        
        frame_idx += 1
    
    # 정리
    cap.release()
    out.release()
    csv_file.close()
    
    print()
    print(f"✅ 완료!")
    print(f"   출력 영상: {output_video_path}")
    print(f"   출력 CSV: {output_csv_path}")
    print(f"   처리된 프레임: {frame_idx_actual + 1}")


if __name__ == "__main__":
    main()
