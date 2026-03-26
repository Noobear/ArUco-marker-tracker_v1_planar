#!/usr/bin/env python3#!/usr/bin/env python3

""""""

ArUco 마커 추적 - 마커 크기 유연한 버전ArUco 마커 추적 - 마커 크기 유연한 버전



사용법:사용법:

    python scripts/aruco_tracker_flexible.py input.mov output.csv --marker-size 5.0    # 기본 (1cm 기본값)

"""    python scripts/aruco_tracker_flexible.py input.mov output.csv

    

import cv2    # 마커 크기 지정

import numpy as np    python scripts/aruco_tracker_flexible.py input.mov output.csv --marker-size 5.0

import csv    

import argparse    # 2cm 마커

from pathlib import Path    python scripts/aruco_tracker_flexible.py input.mov output.csv --marker-size 2.0

"""



def calibrate_and_track(video_path, output_csv, marker_size_cm=1.0):import cv2

    """import numpy as np

    마커 크기를 지정할 수 있는 XY 추적import csv

    """import argparse

    from pathlib import Path

    cap = cv2.VideoCapture(video_path)

    

    if not cap.isOpened():def calibrate_and_track(video_path, output_csv, marker_size_cm=1.0):

        print(f"❌ 영상 파일을 열 수 없음: {video_path}")    """

        return False    마커 크기를 지정할 수 있는 XY 추적 (파일 수정 불필요)

        """

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)    

    detector = cv2.aruco.ArucoDetector(aruco_dict)    cap = cv2.VideoCapture(video_path)

        

    ret, first_frame = cap.read()    if not cap.isOpened():

    if not ret:        print(f"❌ 영상 파일을 열 수 없음: {video_path}")

        print("❌ 첫 프레임을 읽을 수 없음")        return False

        return False    

        # ArUco 설정

    corners, ids, rejected = detector.detectMarkers(first_frame)    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

        detector = cv2.aruco.ArucoDetector(aruco_dict)

    if ids is None or len(ids) == 0:    

        print("❌ 첫 프레임에서 마커를 감지할 수 없음")    # 첫 프레임에서 스케일 팩터 계산

        return False    ret, first_frame = cap.read()

        if not ret:

    corner = corners[0]        print("❌ 첫 프레임을 읽을 수 없음")

            return False

    def distance(p1, p2):    

        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)    corners, ids, rejected = detector.detectMarkers(first_frame)

        

    sides = [    if ids is None or len(ids) == 0:

        distance(corner[0][0], corner[0][1]),        print("❌ 첫 프레임에서 마커를 감지할 수 없음")

        distance(corner[0][1], corner[0][2]),        return False

        distance(corner[0][2], corner[0][3]),    

        distance(corner[0][3], corner[0][0]),    # 첫 번째 마커의 픽셀 크기 계산

    ]    corner = corners[0]

        

    avg_pixel_size = np.mean(sides)    def distance(p1, p2):

    scale_cm_per_px = marker_size_cm / avg_pixel_size        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

        

    print("=" * 70)    sides = [

    print("✅ ArUco 마커 추적 (유연한 크기 지정)")        distance(corner[0][0], corner[0][1]),

    print("=" * 70)        distance(corner[0][1], corner[0][2]),

    print(f"마커 크기: {marker_size_cm:.1f} cm × {marker_size_cm:.1f} cm")        distance(corner[0][2], corner[0][3]),

    print(f"영상에서 측정된 픽셀 크기: {avg_pixel_size:.2f} px")        distance(corner[0][3], corner[0][0]),

    print(f"스케일 팩터: {scale_cm_per_px:.6f} cm/px")    ]

    print(f"또는: {1/scale_cm_per_px:.2f} px/cm")    

    print("=" * 70)    avg_pixel_size = np.mean(sides)

        scale_cm_per_px = marker_size_cm / avg_pixel_size

    fps = cap.get(cv2.CAP_PROP_FPS)    

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    print("=" * 70)

        print("✅ ArUco 마커 추적 (유연한 크기 지정)")

    with open(output_csv, 'w', newline='') as f:    print("=" * 70)

        writer = csv.writer(f)    print(f"마커 크기: {marker_size_cm:.1f} cm × {marker_size_cm:.1f} cm")

        writer.writerow([    print(f"영상에서 측정된 픽셀 크기: {avg_pixel_size:.2f} px")

            'timestamp_s',    print(f"스케일 팩터: {scale_cm_per_px:.6f} cm/px")

            'frame_number',    print(f"또는: {1/scale_cm_per_px:.2f} px/cm")

            'marker_id',    print("=" * 70)

            'center_x_cm',    

            'center_y_cm',    # 비디오 정보

            'rotation_angle_deg',    fps = cap.get(cv2.CAP_PROP_FPS)

            'corner_0_x_cm',    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            'corner_0_y_cm',    

            'corner_1_x_cm',    # CSV 작성

            'corner_1_y_cm',    with open(output_csv, 'w', newline='') as f:

            'corner_2_x_cm',        writer = csv.writer(f)

            'corner_2_y_cm',        writer.writerow([

            'corner_3_x_cm',            'timestamp_s',

            'corner_3_y_cm',            'frame_number',

        ])            'marker_id',

                    'center_x_cm',

        frame_idx = 0            'center_y_cm',

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)            'rotation_angle_deg',

        detection_count = 0            'corner_0_x_cm',

                    'corner_0_y_cm',

        while True:            'corner_1_x_cm',

            ret, frame = cap.read()            'corner_1_y_cm',

            if not ret:            'corner_2_x_cm',

                break            'corner_2_y_cm',

                        'corner_3_x_cm',

            timestamp = frame_idx / fps            'corner_3_y_cm',

            corners, ids, rejected = detector.detectMarkers(frame)        ])

                    

            if ids is not None:        frame_idx = 0

                for marker_idx, marker_id in enumerate(ids):        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

                    corner = corners[marker_idx]        detection_count = 0

                            

                    center_px = np.mean(corner[0], axis=0)        while True:

                    center_cm = center_px * scale_cm_per_px            ret, frame = cap.read()

                                if not ret:

                    v1 = corner[0][1] - corner[0][0]                break

                    angle = np.degrees(np.arctan2(v1[1], v1[0]))            

                                timestamp = frame_idx / fps

                    corners_cm = corner[0] * scale_cm_per_px            

                                corners, ids, rejected = detector.detectMarkers(frame)

                    writer.writerow([            

                        f"{timestamp:.3f}",            if ids is not None:

                        frame_idx,                for marker_idx, marker_id in enumerate(ids):

                        int(marker_id[0]),                    corner = corners[marker_idx]

                        f"{center_cm[0]:.2f}",                    

                        f"{center_cm[1]:.2f}",                    # 중심 계산 (cm)

                        f"{angle:.2f}",                    center_px = np.mean(corner[0], axis=0)

                        f"{corners_cm[0][0]:.2f}",                    center_cm = center_px * scale_cm_per_px

                        f"{corners_cm[0][1]:.2f}",                    

                        f"{corners_cm[1][0]:.2f}",                    # 회전각

                        f"{corners_cm[1][1]:.2f}",                    v1 = corner[0][1] - corner[0][0]

                        f"{corners_cm[2][0]:.2f}",                    angle = np.degrees(np.arctan2(v1[1], v1[0]))

                        f"{corners_cm[2][1]:.2f}",                    

                        f"{corners_cm[3][0]:.2f}",                    # 코너 좌표 (cm)

                        f"{corners_cm[3][1]:.2f}",                    corners_cm = corner[0] * scale_cm_per_px

                    ])                    

                                        writer.writerow([

                    detection_count += 1                        f"{timestamp:.3f}",

                                    frame_idx,

            frame_idx += 1                        int(marker_id[0]),

                                    f"{center_cm[0]:.2f}",

            if frame_idx % max(1, total_frames // 10) == 0:                        f"{center_cm[1]:.2f}",

                progress = 100 * frame_idx / total_frames                        f"{angle:.2f}",

                print(f"진행: {frame_idx:4d}/{total_frames} ({progress:5.1f}%) | "                        f"{corners_cm[0][0]:.2f}",

                      f"감지: {detection_count:4d}")                        f"{corners_cm[0][1]:.2f}",

                            f"{corners_cm[1][0]:.2f}",

    cap.release()                        f"{corners_cm[1][1]:.2f}",

                            f"{corners_cm[2][0]:.2f}",

    print("\n" + "=" * 70)                        f"{corners_cm[2][1]:.2f}",

    print(f"✅ 추적 완료!")                        f"{corners_cm[3][0]:.2f}",

    print(f"출력 파일: {output_csv}")                        f"{corners_cm[3][1]:.2f}",

    print(f"총 감지 횟수: {detection_count}")                    ])

    print(f"평균 감지율: {100*detection_count/total_frames:.1f}%")                    

    print("=" * 70)                    detection_count += 1

                

    return True            frame_idx += 1

            

            # 진행상황 표시

if __name__ == '__main__':            if frame_idx % max(1, total_frames // 10) == 0:

    parser = argparse.ArgumentParser(                progress = 100 * frame_idx / total_frames

        description='ArUco 마커 추적 (마커 크기 지정 가능)',                print(f"진행: {frame_idx:4d}/{total_frames} ({progress:5.1f}%) | "

        formatter_class=argparse.RawDescriptionHelpFormatter,                      f"감지: {detection_count:4d}")

        epilog="""    

예시:    cap.release()

  python scripts/aruco_tracker_flexible.py my_video.mov result.csv --marker-size 5.0    

        """    print("\n" + "=" * 70)

    )    print(f"✅ 추적 완료!")

        print(f"출력 파일: {output_csv}")

    parser.add_argument('input', help='입력 비디오 파일')    print(f"총 감지 횟수: {detection_count}")

    parser.add_argument('output', help='출력 CSV 파일')    print(f"평균 감지율: {100*detection_count/total_frames:.1f}%")

    parser.add_argument('--marker-size', type=float, default=1.0,    print("=" * 70)

                       help='마커 크기 (cm, 기본값: 1.0)')    

        return True

    args = parser.parse_args()

    

    if not Path(args.input).exists():if __name__ == '__main__':

        print(f"❌ 파일을 찾을 수 없음: {args.input}")    parser = argparse.ArgumentParser(

        exit(1)        description='ArUco 마커 추적 (마커 크기 지정 가능)',

            formatter_class=argparse.RawDescriptionHelpFormatter,

    if args.marker_size <= 0:        epilog="""

        print(f"❌ 마커 크기는 양수여야 함: {args.marker_size}")예시:

        exit(1)  # 기본 (1cm × 1cm)

      python scripts/aruco_tracker_flexible.py my_video.mov result.csv

    success = calibrate_and_track(args.input, args.output, args.marker_size)  

    exit(0 if success else 1)  # 마커 크기 지정

  python scripts/aruco_tracker_flexible.py my_video.mov result.csv --marker-size 5.0
  python scripts/aruco_tracker_flexible.py my_video.mov result.csv --marker-size 2.5
  
  # 결과 확인
  head result.csv
  open result.csv  (Excel 열기)
        """
    )
    
    parser.add_argument('input', 
                       help='입력 비디오 파일 (mov, mp4 등)')
    parser.add_argument('output', 
                       help='출력 CSV 파일')
    parser.add_argument('--marker-size', type=float, default=1.0,
                       help='마커 크기 (cm, 기본값: 1.0)')
    
    args = parser.parse_args()
    
    # 입력 파일 존재 확인
    if not Path(args.input).exists():
        print(f"❌ 파일을 찾을 수 없음: {args.input}")
        exit(1)
    
    # 마커 크기 검증
    if args.marker_size <= 0:
        print(f"❌ 마커 크기는 양수여야 함: {args.marker_size}")
        exit(1)
    
    # 실행
    success = calibrate_and_track(args.input, args.output, args.marker_size)
    
    if success:
        print("\n📊 다음 단계:")
        print(f"  1. Excel에서 {args.output} 열기")
        print("  2. center_x_cm, center_y_cm 컬럼 확인")
        print("  3. 그래프 만들기 (마커 궤적)")
        exit(0)
    else:
        exit(1)
