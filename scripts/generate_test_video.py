#!/usr/bin/env python3
"""
2DOF 손가락 움직임 시뮬레이션 테스트 비디오 생성
- 마커 1: 고정 (손가락 근부)
- 마커 2: 1번 기준 회전 (손가락 중간 관절)
- 마커 3: 2번 기준 회전 (손가락 끝)
"""

import cv2
import numpy as np
from cv2 import aruco
import math


def generate_marker_image(marker_id, size=100):
    """ArUco 마커 이미지 생성"""
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    marker_image = aruco.generateImageMarker(dictionary, marker_id, size)
    return marker_image


def rotate_image(image, angle):
    """이미지를 각도만큼 회전"""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), 
                             borderMode=cv2.BORDER_CONSTANT, 
                             borderValue=(255, 255, 255))  # 흰색 배경
    return rotated


def place_marker_on_frame(frame, marker_image, x, y, angle=0):
    """프레임 위에 마커를 배치 (회전된 마커를 올바르게 배치)"""
    
    # 마커를 BGR로 변환 (그레이스케일인 경우)
    marker = marker_image.copy()
    if len(marker.shape) == 2:
        marker = cv2.cvtColor(marker, cv2.COLOR_GRAY2BGR)
    
    # 정수로 변환
    x = int(x)
    y = int(y)
    
    # 마커 회전
    h, w = marker.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # 회전 후 이미지 크기 계산
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # 변환 매트릭스 조정
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
    # 회전 적용
    rotated_marker = cv2.warpAffine(marker, M, (new_w, new_h),
                                     borderMode=cv2.BORDER_CONSTANT,
                                     borderValue=(255, 255, 255))
    
    rotated_h, rotated_w = rotated_marker.shape[:2]
    
    # 프레임에 배치할 좌표
    x1 = max(0, x - rotated_w // 2)
    y1 = max(0, y - rotated_h // 2)
    x2 = min(frame.shape[1], x1 + rotated_w)
    y2 = min(frame.shape[0], y1 + rotated_h)
    
    # 마커 부분 계산
    mx1 = max(0, rotated_w // 2 - x)
    my1 = max(0, rotated_h // 2 - y)
    mx2 = mx1 + (x2 - x1)
    my2 = my1 + (y2 - y1)
    
    # 마커 부분 추출
    marker_part = rotated_marker[int(my1):int(my2), int(mx1):int(mx2)]
    
    if marker_part.size > 0 and marker_part.shape[0] > 0 and marker_part.shape[1] > 0:
        # 마커의 검은색/회색 부분(마커 정보) 감지, 흰색 배경은 제외
        marker_gray = cv2.cvtColor(marker_part, cv2.COLOR_BGR2GRAY)
        mask = cv2.inRange(marker_gray, np.array(0), np.array(200))  # 검은색/회색만 포함 (흰색 제외)
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        # 프레임 영역과 마커 합성
        frame_part = frame[y1:y2, x1:x2]
        frame[y1:y2, x1:x2] = cv2.bitwise_and(frame_part, cv2.bitwise_not(mask_3ch)) + \
                             cv2.bitwise_and(marker_part, mask_3ch)


def create_finger_motion_video(output_path, duration_sec=10, fps=30):
    """2DOF 손가락 움직임 비디오 생성"""
    
    print("🎬 테스트 비디오 생성 중...")
    
    # 비디오 설정
    frame_width, frame_height = 1280, 720
    total_frames = int(duration_sec * fps)
    
    # 출력 비디오 설정
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    # 마커 이미지 생성 (작은 크기)
    marker_size = 60
    marker_0 = generate_marker_image(0, marker_size)
    marker_1 = generate_marker_image(1, marker_size)
    marker_2 = generate_marker_image(2, marker_size)
    
    # 손가락 기본 위치 (픽셀)
    base_x = frame_width // 3
    base_y = frame_height // 2
    
    # 관절 길이 (픽셀) - 마커 간 거리
    joint_length_1 = 120  # 근부에서 중부까지
    joint_length_2 = 120  # 중부에서 끝부까지
    
    print(f"   해상도: {frame_width}x{frame_height}")
    print(f"   FPS: {fps}")
    print(f"   총 프레임: {total_frames}")
    print(f"   마커 크기: {marker_size}x{marker_size}")
    print()
    
    for frame_idx in range(total_frames):
        # 흰색 배경 프레임 생성
        frame = np.full((frame_height, frame_width, 3), 
                       (255, 255, 255), dtype=np.uint8)
        
        # 진행 시간 (0 ~ 1)
        t = frame_idx / total_frames
        
        # 1번 관절 회전: -90도 ~ 90도 (왕복)
        angle_1 = 90 * math.sin(2 * math.pi * t)
        
        # 2번 관절 회전: -120도 ~ 120도 (1번보다 약간 지연)
        t_delayed = (t + 0.1) % 1.0
        angle_2 = 120 * math.sin(2 * math.pi * t_delayed)
        
        # ========== 마커 1: 고정 (근부) ==========
        marker_1_x = base_x
        marker_1_y = base_y
        place_marker_on_frame(frame, marker_0, marker_1_x, marker_1_y, 0)
        
        # ========== 마커 2: 1번 기준 회전 (중부) ==========
        # 1번 마커로부터 joint_length_1만큼 떨어진 곳에 위치
        rad_1 = math.radians(angle_1)
        marker_2_x = marker_1_x + joint_length_1 * math.cos(rad_1)
        marker_2_y = marker_1_y + joint_length_1 * math.sin(rad_1)
        place_marker_on_frame(frame, marker_1, marker_2_x, marker_2_y, int(angle_1))
        
        # ========== 마커 3: 2번 기준 회전 (끝부) ==========
        # 전체 각도 = angle_1 + angle_2
        total_angle = angle_1 + angle_2
        rad_total = math.radians(total_angle)
        
        marker_3_x = marker_2_x + joint_length_2 * math.cos(rad_total)
        marker_3_y = marker_2_y + joint_length_2 * math.sin(rad_total)
        place_marker_on_frame(frame, marker_2, marker_3_x, marker_3_y, int(total_angle))
        
        # ========== 시각화 정보 추가 ==========
        # 프레임 번호
        cv2.putText(frame, f"Frame: {frame_idx}/{total_frames}", 
                   (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # 시간
        time_sec = frame_idx / fps
        cv2.putText(frame, f"Time: {time_sec:.2f}s", 
                   (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # 각도 정보 (기호 제거)
        cv2.putText(frame, f"Joint1: {angle_1:.1f} deg | Joint2: {angle_2:.1f} deg", 
                   (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # 마커 연결선 (선택사항 - 시각적 보조)
        cv2.line(frame, 
                (int(marker_1_x), int(marker_1_y)),
                (int(marker_2_x), int(marker_2_y)),
                (50, 50, 50), 2)
        cv2.line(frame,
                (int(marker_2_x), int(marker_2_y)),
                (int(marker_3_x), int(marker_3_y)),
                (50, 50, 50), 2)
        
        # 관절점 표시
        cv2.circle(frame, (int(marker_1_x), int(marker_1_y)), 5, (0, 0, 0), -1)
        cv2.circle(frame, (int(marker_2_x), int(marker_2_y)), 5, (0, 0, 0), -1)
        cv2.circle(frame, (int(marker_3_x), int(marker_3_y)), 5, (0, 0, 0), -1)
        
        # 비디오에 쓰기
        out.write(frame)
        
        # 진행 상황 표시
        if frame_idx % max(1, total_frames // 10) == 0:
            progress = (frame_idx / total_frames) * 100
            print(f"   진행: {progress:.0f}% ({frame_idx}/{total_frames})")
    
    out.release()
    print()
    print(f"✅ 비디오 생성 완료!")
    print(f"   파일: {output_path}")
    print(f"   길이: {duration_sec}초")
    print(f"   총 프레임: {total_frames}")


if __name__ == "__main__":
    output_path = "tests/videos/test_video_2dof_finger_motion.mp4"
    create_finger_motion_video(output_path, duration_sec=10, fps=30)
