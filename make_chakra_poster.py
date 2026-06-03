from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W, H = 1242, 2258
BASE = Path("/Users/ninez/Documents/海报")
PNG = BASE / "七脉轮能量观测与灵性评估.png"
JPG = BASE / "七脉轮能量观测与灵性评估_最终版.jpg"

BG = (248, 252, 255)
PAPER = (255, 255, 255)
CARD = (249, 253, 255)
INK = (38, 55, 74)
MUTED = (101, 128, 153)
LINE = (184, 218, 238)
ACCENT = (72, 154, 198)

FONT_SONG = "/Users/ninez/Library/Fonts/SOURCEHANSERIFSC-REGULAR.OTF"
FONT_SONG_LIGHT = "/Users/ninez/Library/Fonts/SOURCEHANSERIFSC-LIGHT.OTF"
FONT_SONG_MEDIUM = "/Users/ninez/Library/Fonts/SourceHanSerifCN-Medium-6.otf"
FONT_SONG_BOLD = "/Users/ninez/Library/Fonts/SOURCEHANSERIFSC-BOLD.OTF"
FONT_SONG_HEAVY = "/Users/ninez/Library/Fonts/SOURCEHANSERIFSC-HEAVY.OTF"
FONT_AVENIR = "/System/Library/Fonts/Avenir.ttc"
FONT_BODONI = "/System/Library/Fonts/Supplemental/Bodoni 72 OS.ttc"


def font(path, size):
    return ImageFont.truetype(path, size)


F = {
    "eyebrow": font(FONT_AVENIR, 27),
    "title": font(FONT_SONG_HEAVY, 62),
    "brand": font(FONT_BODONI, 38),
    "h_en": font(FONT_AVENIR, 21),
    "h": font(FONT_SONG_BOLD, 44),
    "price": font(FONT_SONG_BOLD, 58),
    "section": font(FONT_SONG_MEDIUM, 31),
    "body": font(FONT_SONG_LIGHT, 29),
    "note": font(FONT_SONG_LIGHT, 25),
    "mini": font(FONT_SONG_LIGHT, 21),
}


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw, text, fnt, max_w):
    lines, current = [], ""
    for ch in text:
        test = current + ch
        if text_size(draw, test, fnt)[0] <= max_w or not current:
            current = test
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def paragraph(draw, x, y, text, fnt, fill, max_w, gap=12):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def center(draw, y, text, fnt, fill=INK):
    tw, th = text_size(draw, text, fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)
    return y + th


def center_in_box(draw, box, text, fnt, fill=INK):
    x1, y1, x2, y2 = box
    tb = draw.textbbox((0, 0), text, font=fnt)
    tw = tb[2] - tb[0]
    text_y = y1 + (y2 - y1) / 2 - (tb[1] + tb[3]) / 2 - 2
    draw.text((x1 + (x2 - x1 - tw) / 2, text_y), text, font=fnt, fill=fill)


def center_in(draw, x1, y, x2, text, fnt, fill=INK):
    tw, _ = text_size(draw, text, fnt)
    draw.text((x1 + (x2 - x1 - tw) / 2, y), text, font=fnt, fill=fill)


def round_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def sparkle(draw, x, y, s=12, fill=ACCENT, outline=None):
    pts = [
        (x, y - s), (x + s * .22, y - s * .22), (x + s, y),
        (x + s * .22, y + s * .22), (x, y + s),
        (x - s * .22, y + s * .22), (x - s, y), (x - s * .22, y - s * .22),
    ]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=1)


def star_field(draw):
    for x, y, s in [(136, 220, 22), (1018, 185, 28), (1075, 420, 18), (178, 615, 16),
                    (1080, 930, 16), (118, 1320, 14), (1060, 1660, 18), (180, 2140, 16)]:
        sparkle(draw, x, y, s, fill=(98, 180, 220, 70), outline=(95, 165, 207, 90))
    for x, y in [(232, 132), (298, 302), (952, 326), (100, 482), (1080, 650),
                 (232, 1010), (1016, 1180), (176, 1510), (1082, 1430), (252, 1832),
                 (1000, 2180), (240, 2450)]:
        sparkle(draw, x, y, 8, fill=(99, 174, 216, 95))


def draw_grid(draw, x, y, items, cols=2):
    col_w = (W - 2 * x - 14) / cols
    row_h = 86
    for i, text in enumerate(items):
        col = i % cols
        row = i // cols
        bx = x + col * (col_w + 14)
        by = y + row * (row_h + 20)
        round_rect(draw, (bx, by, bx + col_w, by + row_h), 0, CARD, outline=(221, 238, 247), width=1)
        sparkle(draw, bx + 31, by + row_h / 2, 10, fill=(75, 155, 200, 180))
        paragraph(draw, bx + 58, by + 22, text, F["note"], INK, col_w - 78, 5)
    return y + math.ceil(len(items) / cols) * (row_h + 20)


def draw_chakra_stickers(draw, x, y, w):
    colors = [
        (218, 76, 86),   # root
        (235, 137, 61),  # sacral
        (230, 190, 64),  # solar plexus
        (93, 176, 127),  # heart
        (80, 164, 210),  # throat
        (89, 103, 194),  # third eye
        (156, 102, 205), # crown
    ]
    labels = ["Root", "Sacral", "Solar", "Heart", "Throat", "Eye", "Crown"]
    step = w / 7
    cy = y + 58
    for i, (color, label) in enumerate(zip(colors, labels)):
        cx = x + step * i + step / 2
        r = 33
        pale = (*color, 30)
        soft = (*color, 80)
        strong = (*color, 150)
        draw.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), fill=(255, 255, 255, 145), outline=(210, 232, 242, 150), width=1)
        for k in range(12):
            a = math.radians(k * 30)
            px = cx + math.cos(a) * 22
            py = cy + math.sin(a) * 22
            prx, pry = 13, 22
            draw.ellipse((px - prx, py - pry, px + prx, py + pry), fill=pale, outline=soft, width=1)
        for k in range(8):
            a = math.radians(k * 45 + 22.5)
            px = cx + math.cos(a) * 13
            py = cy + math.sin(a) * 13
            draw.ellipse((px - 9, py - 14, px + 9, py + 14), fill=(*color, 45), outline=soft, width=1)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=soft, width=2)
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=(255, 255, 255, 120), outline=strong, width=2)
        sparkle(draw, cx, cy, 9, fill=strong)
        tw, _ = text_size(draw, label, F["mini"])
        draw.text((cx - tw / 2, cy + 52), label, font=F["mini"], fill=(96, 132, 154))
    return y + 128


def draw_chip_orbit(draw, x, y, w, labels):
    h = 170
    cx, cy = x + w / 2, y + h / 2
    rx, ry = w / 2 - 95, h / 2 - 34
    for start in range(0, 360, 34):
        draw.arc((cx - rx, cy - ry, cx + rx, cy + ry), start, start + 18, fill=(151, 207, 234, 145), width=2)
    sparkle(draw, cx, cy, 17, fill=(77, 157, 202, 120), outline=(93, 171, 213, 95))
    positions = [
        (cx - rx + 34, cy - 30), (cx - rx + 34, cy + 30),
        (cx, cy - 55), (cx, cy + 55),
        (cx + rx - 34, cy - 30), (cx + rx - 34, cy + 30),
    ]
    for label, (tx, ty) in zip(labels, positions):
        tw, th = text_size(draw, label, F["note"])
        bw, bh = max(112, tw + 58), 46
        bx, by = tx - bw / 2, ty - bh / 2
        round_rect(draw, (bx, by, bx + bw, by + bh), 23, (247, 252, 255), outline=(187, 224, 241), width=1)
        sparkle(draw, bx + 22, by + 22, 5, fill=(75, 155, 200, 155))
        draw.text((bx + (bw - tw) / 2 + 8, by + 8), label, font=F["note"], fill=INK)
        sparkle(draw, bx + bw - 22, by + 22, 5, fill=(75, 155, 200, 155))
    return y + h


img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

for r, alpha in [(980, 70), (700, 55), (460, 40)]:
    draw.ellipse((W / 2 - r / 2, 42, W / 2 + r / 2, 42 + r * .72), fill=(231, 247, 255, alpha))
star_field(draw)

draw.rounded_rectangle((38, 28, W - 38, H - 28), 42, outline=(126, 184, 214), width=2)
draw.rounded_rectangle((52, 42, W - 52, H - 42), 34, outline=(218, 238, 248), width=1)
for x in [W / 2 - 78, W / 2, W / 2 + 78]:
    sparkle(draw, x, 38, 13, fill=(61, 139, 184, 170))

y = 360
center(draw, y, "CHAKRA ENERGY OBSERVATION", F["eyebrow"], fill=(91, 137, 166))
y += 50
center(draw, y, "七脉轮能量观测与灵性评估", F["title"], fill=INK)
y += 90
center(draw, y, "Lian Yue Xian", F["brand"], fill=(58, 102, 130))
y += 62
center(draw, y, "能量觉察 · 内在探索 · 灵性成长阶段评估", F["body"], fill=MUTED)
y += 50
consult_box = (445, y, W - 445, y + 54)
round_rect(draw, consult_box, 0, (255, 255, 255), outline=LINE, width=1)
center_in_box(draw, consult_box, "咨询模式：文字", F["note"], fill=INK)
y += 112

card_x, card_w = 145, W - 290
card_y = y
card_h = 1060
round_rect(draw, (card_x, card_y, card_x + card_w, card_y + card_h), 0, PAPER, outline=LINE, width=2)
draw.rectangle((card_x + 18, card_y + 18, card_x + card_w - 18, card_y + card_h - 18), outline=(222, 239, 248), width=1)

y = card_y + 54
draw.text((card_x + 48, y), "C H A K R A   R E A D I N G", font=F["h_en"], fill=(105, 158, 189))
y += 36
draw.text((card_x + 48, y), "七脉轮能量观测", font=F["h"], fill=INK)
price_x1 = card_x + card_w - 300
price_x2 = card_x + card_w - 46
center_in(draw, price_x1, card_y + 46, price_x2, "188r", F["price"], fill=(32, 73, 100))
center_in(draw, price_x1, card_y + 118, price_x2, "48小时内出报告", F["note"], fill=MUTED)
y += 82
y = paragraph(
    draw, card_x + 48, y,
    "通过七脉轮能量系统观测，帮助你了解当前能量状态、内在真实意愿与外界影响因素之间的关系。",
    F["body"], INK, card_w - 96, 12
)
y += 36
y = draw_chakra_stickers(draw, card_x + 58, y, card_w - 116)
y += 34
draw.text((card_x + 48, y), "观测与评估", font=F["section"], fill=INK)
y += 58
y = draw_grid(draw, card_x + 48, y, [
    "整体的能量状态",
    "七脉轮能量强弱分析",
    "能量阻塞点识别",
    "个人意愿与外界影响",
    "背后的深层影响因素",
    "个性化疗愈与建议",
], cols=2)
y += 48
draw.line((card_x + 48, y + 8, card_x + 48, y + 86), fill=ACCENT, width=5)
y = paragraph(
    draw, card_x + 72, y,
    "通过观测当前能量状态，帮助你更清晰地理解自身处境，发现影响现实体验的深层模式，并找到更适合自己的成长方向。",
    F["note"], INK, card_w - 122, 8
)

y = card_y + card_h + 56
note_h = 250
round_rect(draw, (card_x, y, card_x + card_w, y + note_h), 0, PAPER, outline=LINE, width=2)
draw.text((card_x + 48, y + 44), "温馨提示", font=F["h"], fill=INK)
paragraph(
    draw, card_x + 48, y + 138,
    "本服务旨在协助个人进行能量觉察与内在探索，不构成医疗、心理诊断或未来结果保证。",
    F["body"], INK, card_w - 96, 12
)

PNG.parent.mkdir(parents=True, exist_ok=True)
img.save(PNG, quality=98)
img.save(JPG, quality=98, optimize=True)

print(PNG)
print(JPG)
