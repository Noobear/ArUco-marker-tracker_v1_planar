"""
A4 출력용 ArUco 마커 PDF 생성 스크립트
- print_1cm.pdf   : 마커 ID 1~10, 각 1cm × 1cm
- print_1_5cm.pdf : 마커 ID 1~10, 각 1.5cm × 1.5cm

사용법:
    python create_markers.py

인쇄 시 반드시 "실제 크기(100%)" 또는 "크기 조정 없음"으로 인쇄하세요.
"""

from PIL import Image, ImageDraw, ImageFont
import os

DPI = 300
MM = DPI / 25.4  # 1mm → px

A4_W = int(210 * MM)   # 2480 px
A4_H = int(297 * MM)   # 3508 px

MARGIN_X   = int(20 * MM)
MARGIN_TOP = int(25 * MM)
GAP        = int(10 * MM)
LABEL_H    = int(5 * MM)

# markers/ 폴더 (스크립트 기준)
MARKER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "markers")


def get_font(size_px):
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
    marker_px = int(marker_size_cm * 10 * MM)

    canvas = Image.new("RGB", (A4_W, A4_H), "white")
    draw = ImageDraw.Draw(canvas)

    title_font = get_font(int(6 * MM))
    sub_font   = get_font(int(3.5 * MM))
    id_font    = get_font(int(3 * MM))

    title = f"ArUco Markers ID 1~10  ({marker_size_cm}cm x {marker_size_cm}cm)"
    draw.text((MARGIN_X, int(8 * MM)), title, fill="black", font=title_font)

    subtitle = "Print at 100% scale  /  Do not scale to fit"
    draw.text((MARGIN_X, int(16 * MM)), subtitle, fill="#555555", font=sub_font)

    line_y = int(22 * MM)
    draw.line([(MARGIN_X, line_y), (A4_W - MARGIN_X, line_y)], fill="#aaaaaa", width=2)

    cols = 2
    cell_w = (A4_W - MARGIN_X * 2 - GAP * (cols - 1)) // cols
    col_positions = [MARGIN_X + i * (cell_w + GAP) for i in range(cols)]

    for i in range(10):
        marker_id = i + 1
        row = i // cols
        col = i % cols

        x0 = col_positions[col] + (cell_w - marker_px) // 2
        y0 = MARGIN_TOP + row * (marker_px + LABEL_H + GAP)

        marker_path = os.path.join(MARKER_DIR, f"aruco_marker_{marker_id}.png")
        if not os.path.exists(marker_path):
            print(f"[경고] 마커 파일 없음: {marker_path}")
            continue

        marker_img = Image.open(marker_path).convert("RGB")
        marker_img = marker_img.resize((marker_px, marker_px), Image.LANCZOS)
        canvas.paste(marker_img, (x0, y0))

        draw.rectangle([x0 - 1, y0 - 1, x0 + marker_px, y0 + marker_px],
                       outline="#cccccc", width=1)

        label = f"ID: {marker_id}"
        bbox = id_font.getbbox(label)
        label_w = bbox[2] - bbox[0]
        label_x = x0 + (marker_px - label_w) // 2
        label_y = y0 + marker_px + int(1 * MM)
        draw.text((label_x, label_y), label, fill="#333333", font=id_font)

    canvas.save(output_path, "PDF", resolution=DPI)
    print(f"저장 완료: {output_path}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_1cm   = os.path.join(script_dir, "print_1cm.pdf")
    out_1_5cm = os.path.join(script_dir, "print_1_5cm.pdf")

    print("PDF 생성 중...")
    create_sheet(1.0, out_1cm)
    create_sheet(1.5, out_1_5cm)
    print("완료!")
