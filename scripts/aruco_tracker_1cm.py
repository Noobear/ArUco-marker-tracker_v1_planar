#!/usr/bin/env python3#!/usr/bin/env python3

""""""

ArUco 마커 추적 - XY 캘리브레이션 (마커 크기 1cm × 1cm 고정)ArUco 마커 추적 - XY 캘리브레이션 (마커 크기 1cm × 1cm 고정)



가장 간단한 사용법:가장 간단한 사용법:

    python scripts/aruco_tracker_1cm.py input.mov output.csv    python scripts/aruco_tracker_1cm.py input.mov output.csv

"""    

그냥 이것만 하면 됨! ✅

import cv2"""

import numpy as np

import csvimport cv2

import argparseimport numpy as np

from pathlib import Pathimport csv

import argparse

from pathlib import Path

def calibrate_and_track(video_path, output_csv):

    """

    1cm × 1cm 마커를 기준으로 XY 좌표를 cm로 변환하면서 추적def calibrate_and_track(video_path, output_csv):

    """    """

        1cm × 1cm 마커를 기준으로 XY 좌표를 cm로 변환하면서 추적

    MARKER_SIZE_CM = 1.0  # 고정값    """

        

    cap = cv2.VideoCapture(video_path)    MARKER_SIZE_CM = 1.0  # 고정값

        

    if not cap.isOpened():    cap = cv2.VideoCapture(video_path)

        print(f"❌ 영상 파일을 열 수 없음: {video_path}")    

        return False    if not cap.isOpened():

            print(f"❌ 영상 파일을 열 수 없음: {video_path}")

    # ArUco 설정        return False

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)    

    detector = cv2.aruco.ArucoDetector(aruco_dict)    # ArUco 설정

        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    # 첫 프레임에서 스케일 팩터 계산    detector = cv2.aruco.ArucoDetector(aruco_dict)

    ret, first_frame = cap.read()    

    if not ret:    # 첫 프레임에서 스케일 팩터 계산

        print("❌ 첫 프레임을 읽을 수 없음")    ret, first_frame = cap.read()

        return False    if not ret:

            print("❌ 첫 프레임을 읽을 수 없음")

    corners, ids, rejected = detector.detectMarkers(first_frame)        return False

        

    if ids is None or len(ids) == 0:    corners, ids, rejected = detector.detectMarkers(first_frame)

        print("❌ 첫 프레임에서 마커를 감지할 수 없음")    

        return False    if ids is None or len(ids) == 0:

            print("❌ 첫 프레임에서 마커를 감지할 수 없음")

    # 첫 번째 마커의 픽셀 크기 계산        return False

    corner = corners[0]    

        # 첫 번째 마커의 픽셀 크기 계산

    def distance(p1, p2):    corner = corners[0]

        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)    

        def distance(p1, p2):

    sides = [        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

        distance(corner[0][0], corner[0][1]),    

        distance(corner[0][1], corner[0][2]),    sides = [

        distance(corner[0][2], corner[0][3]),        distance(corner[0][0], corner[0][1]),

        distance(corner[0][3], corner[0][0]),        distance(corner[0][1], corner[0][2]),

    ]        distance(corner[0][2], corner[0][3]),

            distance(corner[0][3], corner[0][0]),

    avg_pixel_size = np.mean(sides)    ]

    scale_cm_per_px = MARKER_SIZE_CM / avg_pixel_size    

        avg_pixel_size = np.mean(sides)

    print("=" * 70)    scale_cm_per_px = MARKER_SIZE_CM / avg_pixel_size

    print("✅ ArUco 마커 추적 (1cm × 1cm 고정)")    

    print("=" * 70)    print("=" * 70)

    print(f"마커 크기: {MARKER_SIZE_CM:.1f} cm × {MARKER_SIZE_CM:.1f} cm (고정)")    print("✅ ArUco 마커 추적 (1cm × 1cm 고정)")

    print(f"영상에서 측정된 픽셀 크기: {avg_pixel_size:.2f} px")    print("=" * 70)

    print(f"스케일 팩터: {scale_cm_per_px:.6f} cm/px")    print(f"마커 크기: {MARKER_SIZE_CM:.1f} cm × {MARKER_SIZE_CM:.1f} cm (고정)")

    print(f"또는: {1/scale_cm_per_px:.2f} px/cm")    print(f"영상에서 측정된 픽셀 크기: {avg_pixel_size:.2f} px")

    print("=" * 70)    print(f"스케일 팩터: {scale_cm_per_px:.6f} cm/px")

        print(f"또는: {1/scale_cm_per_px:.2f} px/cm")

    # 비디오 정보    print("=" * 70)

    fps = cap.get(cv2.CAP_PROP_FPS)    

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # 비디오 정보

        fps = cap.get(cv2.CAP_PROP_FPS)

    # CSV 작성    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with open(output_csv, 'w', newline='') as f:    

        writer = csv.writer(f)    # CSV 작성

        writer.writerow([    with open(output_csv, 'w', newline='') as f:

            'timestamp_s',        writer = csv.writer(f)

            'frame_number',        writer.writerow([

            'marker_id',            'timestamp_s',

            'center_x_cm',            'frame_number',

            'center_y_cm',            'marker_id',

            'rotation_angle_deg',            'center_x_cm',

            'corner_0_x_cm',            'center_y_cm',

            'corner_0_y_cm',            'rotation_angle_deg',

            'corner_1_x_cm',            'corner_0_x_cm',

            'corner_1_y_cm',            'corner_0_y_cm',

            'corner_2_x_cm',            'corner_1_x_cm',

            'corner_2_y_cm',            'corner_1_y_cm',

            'corner_3_x_cm',            'corner_2_x_cm',

            'corner_3_y_cm',            'corner_2_y_cm',

        ])            'corner_3_x_cm',

                    'corner_3_y_cm',

        frame_idx = 0        ])

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)        

        detection_count = 0        frame_idx = 0

                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while True:        detection_count = 0

            ret, frame = cap.read()        

            if not ret:        while True:

                break            ret, frame = cap.read()

                        if not ret:

            timestamp = frame_idx / fps                break

                        

            corners, ids, rejected = detector.detectMarkers(frame)            timestamp = frame_idx / fps

                        

            if ids is not None:            corners, ids, rejected = detector.detectMarkers(frame)

                for marker_idx, marker_id in enumerate(ids):            

                    corner = corners[marker_idx]            if ids is not None:

                                    for marker_idx, marker_id in enumerate(ids):

                    # 중심 계산 (cm)                    corner = corners[marker_idx]

                    center_px = np.mean(corner[0], axis=0)                    

                    center_cm = center_px * scale_cm_per_px                    # 중심 계산 (cm)

                                        center_px = np.mean(corner[0], axis=0)

                    # 회전각                    center_cm = center_px * scale_cm_per_px

                    v1 = corner[0][1] - corner[0][0]                    

                    angle = np.degrees(np.arctan2(v1[1], v1[0]))                    # 회전각

                                        v1 = corner[0][1] - corner[0][0]

                    # 코너 좌표 (cm)                    angle = np.degrees(np.arctan2(v1[1], v1[0]))

                    corners_cm = corner[0] * scale_cm_per_px                    

                                        # 코너 좌표 (cm)

                    writer.writerow([                    corners_cm = corner[0] * scale_cm_per_px

                        f"{timestamp:.3f}",                    

                        frame_idx,                    writer.writerow([

                        int(marker_id[0]),                        f"{timestamp:.3f}",

                        f"{center_cm[0]:.2f}",                        frame_idx,

                        f"{center_cm[1]:.2f}",                        int(marker_id[0]),

                        f"{angle:.2f}",                        f"{center_cm[0]:.2f}",

                        f"{corners_cm[0][0]:.2f}",                        f"{center_cm[1]:.2f}",

                        f"{corners_cm[0][1]:.2f}",                        f"{angle:.2f}",

                        f"{corners_cm[1][0]:.2f}",                        f"{corners_cm[0][0]:.2f}",

                        f"{corners_cm[1][1]:.2f}",                        f"{corners_cm[0][1]:.2f}",

                        f"{corners_cm[2][0]:.2f}",                        f"{corners_cm[1][0]:.2f}",

                        f"{corners_cm[2][1]:.2f}",                        f"{corners_cm[1][1]:.2f}",

                        f"{corners_cm[3][0]:.2f}",                        f"{corners_cm[2][0]:.2f}",

                        f"{corners_cm[3][1]:.2f}",                        f"{corners_cm[2][1]:.2f}",

                    ])                        f"{corners_cm[3][0]:.2f}",

                                            f"{corners_cm[3][1]:.2f}",

                    detection_count += 1                    ])

                                

            frame_idx += 1                    detection_count += 1

                        

            # 진행상황 표시            frame_idx += 1

            if frame_idx % max(1, total_frames // 10) == 0:            

                progress = 100 * frame_idx / total_frames            # 진행상황 표시

                print(f"진행: {frame_idx:4d}/{total_frames} ({progress:5.1f}%) | "            if frame_idx % max(1, total_frames // 10) == 0:

                      f"감지: {detection_count:4d}")                progress = 100 * frame_idx / total_frames

                    print(f"진행: {frame_idx:4d}/{total_frames} ({progress:5.1f}%) | "

    cap.release()                      f"감지: {detection_count:4d}")

        

    print("\n" + "=" * 70)    cap.release()

    print(f"✅ 추적 완료!")    

    print(f"출력 파일: {output_csv}")    print("\n" + "=" * 70)

    print(f"총 감지 횟수: {detection_count}")    print(f"✅ 추적 완료!")

    print(f"평균 감지율: {100*detection_count/total_frames:.1f}%")    print(f"출력 파일: {output_csv}")

    print("=" * 70)    print(f"총 감지 횟수: {detection_count}")

        print(f"평균 감지율: {100*detection_count/total_frames:.1f}%")

    return True    print("=" * 70)

    

    return True

if __name__ == '__main__':

    parser = argparse.ArgumentParser(

        description='ArUco 마커 추적 (1cm × 1cm 고정 캘리브레이션)',if __name__ == '__main__':

        formatter_class=argparse.RawDescriptionHelpFormatter,    parser = argparse.ArgumentParser(

        epilog="""        description='ArUco 마커 추적 (1cm × 1cm 고정 캘리브레이션)',

예시:        formatter_class=argparse.RawDescriptionHelpFormatter,

  python scripts/aruco_tracker_1cm.py my_video.mov result.csv        epilog="""

  open result.csv  (Excel에서 열기)예시:

        """  # 기본 사용법

    )  python scripts/aruco_tracker_1cm.py my_video.mov result.csv

      

    parser.add_argument('input', help='입력 비디오 파일 (mov, mp4 등)')  # 결과 확인

    parser.add_argument('output', help='출력 CSV 파일 (결과 데이터)')  head -10 result.csv

      open result.csv  (Excel에서 열기)

    args = parser.parse_args()        """

        )

    if not Path(args.input).exists():    

        print(f"❌ 파일을 찾을 수 없음: {args.input}")    parser.add_argument('input', 

        exit(1)                       help='입력 비디오 파일 (mov, mp4 등)')

        parser.add_argument('output', 

    success = calibrate_and_track(args.input, args.output)                       help='출력 CSV 파일 (결과 데이터)')

        

    if success:    args = parser.parse_args()

        print("\n📊 다음 단계:")    

        print(f"  1. Excel에서 {args.output} 열기")    # 입력 파일 존재 확인

        print("  2. center_x_cm, center_y_cm 컬럼 확인")    if not Path(args.input).exists():

        print("  3. 그래프 만들기")        print(f"❌ 파일을 찾을 수 없음: {args.input}")

        exit(0)        exit(1)

    else:    

        exit(1)    # 실행

    success = calibrate_and_track(args.input, args.output)
    
    if success:
        print("\n📊 다음 단계:")
        print(f"  1. Excel에서 {args.output} 열기")
        print("  2. center_x_cm, center_y_cm 컬럼 확인")
        print("  3. 그래프 만들기 (마커 궤적)")
        exit(0)
    else:
        exit(1)
