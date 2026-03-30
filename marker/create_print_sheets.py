"""
A4 출력용 ArUco 마커 PDF 생성 스크립트
- print_1cm.pdf   : 마커 ID 1~10, 각 1cm × 1cm
- print_1_5cm.pdf : 마커 ID 1~10, 각 1.5cm × 1.5cm

사용법:
    python3 create_print_sheets.py

인쇄 시 반드시 "실제 크기(100%)" 또는 "크기 조정 없음"으로 인쇄하세요.
"""

from PIL import Image, ImageDraw, ImageFont
import os

DPI = 300
MM = DPI / 25.4  # 1mm → px

A4_W = int(210 * MM)   # 2480 px
A4_H = int(297 * MM)   # 3508 px

MARGIN_X = int(20 * MM)   # 좌우 마진 20mm
MARGIN_TOP = int(25 * MM) # 상단 마진 25mm
MARGIN_BOT = int(20 * MM) # 하단 마진 20mm
GAP = int(10 * MM)         # 셀 간격 10mm
LABEL_H = int(5 * MM)      # 레이블 높이 5mm

MARKER_DIR = os.path.dirname(os.path.abspath(__file__))


def get_font(size_px):
    """시스템 폰트를 시도하고, 없으면 기본 폰트 사용."""
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size_px)
            except Exception:
                continue
    return ImageFont.load_default()


def create_sheet(marker_size_cm: float, output_path: str):
    marker_px = int(marker_size_cm * 10 * MM)  # cm → mm → px

    canvas = Image.new("RGB", (A4_W, A4_H), "white")
    draw = ImageDraw.Draw(canvas)

    # 폰트 크기
    title_font = get_font(int(6 * MM))
    sub_font = get_font(int(3.5 * MM))
    id_font = get_font(int(3 * MM))

    # 제목
    title = f"ArUco Markers ID 1~10  ({marker_size_cm}cm x {marker_size_cm}cm)"
    draw.text((MARGIN_X, int(8 * MM)), title, fill="black", font=title_font)

    # 부제 (인쇄 주의사항)
    subtitle = "Print at 100% scale  /  Do not scale to fit"
    draw.text((MARGIN_X, int(16 * MM)), subtitle, fill="#555555", font=sub_font)

    # 구분선
    line_y = int(22 * MM)
    draw.line([(MARGIN_X, line_y), (A4_W - MARGIN_X, line_y)], fill="#aaaaaa", width=2)

    # 그리드 배치: 2열 × 5행
    cols = 2
    cell_w = (A4_W - MARGIN_X * 2 - GAP * (cols - 1)) // cols

    start_y = MARGIN_TOP
    col_positions = [MARGIN_X + i * (cell_w + GAP) for i in range(cols)]

    for i in range(10):  # ID 1~10
        marker_id = i + 1
        row = i // cols
        col = i % cols

        x0 = col_positions[col] + (cell_w - marker_px) // 2
        y0 = start_y + row * (marker_px + LABEL_H + GAP)

        # 마커 이미지 로드 및 리사이즈
        marker_path = os.path.join(MARKER_DIR, f"aruco_marker_{marker_id}.png")
        if not os.path.exists(marker_path):
            print(f"[경고] 마커 파일 없음: {marker_path}")
            continue

        marker_img = Image.open(marker_path).convert("RGB")
        marker_img = marker_img.resize((marker_px, marker_px), Image.LANCZOS)
        canvas.paste(marker_img, (x0, y0))

        # 테두리 (얇은 회색 선)
        draw.rectangle([x0 - 1, y0 - 1, x0 + marker_px, y0 + marker_px],
                       outline="#cccccc", width=1)

        # ID 레이블
        label = f"ID: {marker_id}"
        bbox = id_font.getbbox(label)
        label_w = bbox[2] - bbox[0]
        label_x = x0 + (marker_px - label_w) // 2
        label_y = y0 + marker_px + int(1 * MM)
        draw.text((label_x, label_y), label, fill="#333333", font=id_font)

    canvas.save(output_path, "PDF", resolution=DPI)
    print(f"저장 완료: {output_path}")


if __name__ == "__main__":
    out_1cm = os.path.join(MARKER_DIR, "print_1cm.pdf")
    out_1_5cm = os.path.join(MARKER_DIR, "print_1_5cm.pdf")

    print("PDF 생성 중...")
    create_sheet(1.0, out_1cm)
    create_sheet(1.5, out_1_5cm)
    print("완료!")
