from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
from pathlib import Path

W, H = 1242, 4100
OUT = Path("/Users/ninez/Documents/海报/潋月仙_神秘学咨询服务价目表.png")

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
FONT_HEI = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_ST = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_AVENIR = "/System/Library/Fonts/Avenir.ttc"
FONT_BODONI = "/System/Library/Fonts/Supplemental/Bodoni 72 OS.ttc"


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.truetype(FONT_ST, size)


F = {
    "eyebrow": font(FONT_AVENIR, 28),
    "title": font(FONT_SONG_HEAVY, 72),
    "brand": font(FONT_BODONI, 42),
    "h_en": font(FONT_AVENIR, 22),
    "h": font(FONT_SONG_BOLD, 48),
    "price": font(FONT_SONG_BOLD, 58),
    "small": font(FONT_SONG, 24),
    "body": font(FONT_SONG_LIGHT, 29),
    "body_b": font(FONT_SONG_MEDIUM, 29),
    "note": font(FONT_SONG_LIGHT, 25),
    "note_b": font(FONT_SONG_MEDIUM, 25),
    "table": font(FONT_SONG_LIGHT, 31),
    "table_b": font(FONT_SONG_MEDIUM, 31),
    "mini": font(FONT_SONG_LIGHT, 21),
}


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_center(draw, y, text, fnt, fill=INK, spacing=0):
    tw, th = text_size(draw, text, fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill, spacing=spacing)
    return y + th


def draw_center_in(draw, box, text, fnt, fill=INK):
    x1, y1, x2, _ = box
    tw, th = text_size(draw, text, fnt)
    draw.text((x1 + (x2 - x1 - tw) / 2, y1), text, font=fnt, fill=fill)
    return th


def draw_text_center_y(draw, x, cy, text, fnt, fill=INK):
    box = draw.textbbox((0, 0), text, font=fnt)
    y = cy - (box[1] + box[3]) / 2
    draw.text((x, y), text, font=fnt, fill=fill)


def paragraph_center(draw, y, text, fnt, fill, max_w, line_gap=8):
    for line in wrap(draw, text, fnt, max_w):
        tw, _ = text_size(draw, line, fnt)
        draw.text(((W - tw) / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def wrap(draw, text, fnt, max_w):
    lines = []
    current = ""
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


def paragraph(draw, xy, text, fnt, fill, max_w, line_gap=12):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def paragraph_center_y(draw, x, cy, text, fnt, fill, max_w, line_gap=6):
    lines = wrap(draw, text, fnt, max_w)
    total_h = len(lines) * fnt.size + max(0, len(lines) - 1) * line_gap
    y = cy - total_h / 2 - 3
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap


def paragraph_height(draw, text, fnt, max_w, line_gap=12):
    return len(wrap(draw, text, fnt, max_w)) * (fnt.size + line_gap)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def butterfly(draw, cx, cy, scale=1, color=(161, 125, 188, 78)):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    c = color
    # wings
    for side in [-1, 1]:
        pts1 = [
            (cx, cy),
            (cx + side * 76 * scale, cy - 112 * scale),
            (cx + side * 228 * scale, cy - 96 * scale),
            (cx + side * 194 * scale, cy + 48 * scale),
            (cx + side * 58 * scale, cy + 42 * scale),
        ]
        pts2 = [
            (cx, cy + 20 * scale),
            (cx + side * 64 * scale, cy + 54 * scale),
            (cx + side * 164 * scale, cy + 130 * scale),
            (cx + side * 84 * scale, cy + 174 * scale),
            (cx + side * 20 * scale, cy + 92 * scale),
        ]
        od.polygon(pts1, fill=c)
        od.polygon(pts2, fill=(c[0], c[1], c[2], 52))
        for i in range(5):
            off = 34 + i * 32
            od.line(
                [(cx + side * 18 * scale, cy + i * 8 * scale),
                 (cx + side * off * scale, cy - (70 - i * 16) * scale)],
                fill=(c[0], c[1], c[2], 52), width=max(1, int(2 * scale))
            )
    od.ellipse((cx - 10 * scale, cy - 35 * scale, cx + 10 * scale, cy + 74 * scale), fill=(c[0], c[1], c[2], 72))
    od.line((cx - 4 * scale, cy - 32 * scale, cx - 34 * scale, cy - 86 * scale), fill=(c[0], c[1], c[2], 60), width=2)
    od.line((cx + 4 * scale, cy - 32 * scale, cx + 34 * scale, cy - 86 * scale), fill=(c[0], c[1], c[2], 60), width=2)
    overlay = overlay.filter(ImageFilter.GaussianBlur(1.2))
    draw.bitmap((0, 0), overlay)


def star(draw, x, y, s=11, fill=ACCENT):
    draw.polygon([(x, y - s), (x + s * .25, y - s * .25), (x + s, y), (x + s * .25, y + s * .25),
                  (x, y + s), (x - s * .25, y + s * .25), (x - s, y), (x - s * .25, y - s * .25)], fill=fill)


def sparkle(draw, x, y, s=18, fill=ACCENT, outline=None, width=2):
    pts = [
        (x, y - s), (x + s * .22, y - s * .22), (x + s, y),
        (x + s * .22, y + s * .22), (x, y + s),
        (x - s * .22, y + s * .22), (x - s, y), (x - s * .22, y - s * .22),
    ]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def draw_star_field(draw):
    big = [
        (136, 220, 22), (1018, 185, 28), (1075, 420, 18), (178, 615, 16),
        (1120, 900, 18), (96, 1300, 14), (1100, 1690, 16), (160, 2240, 18),
        (1050, 2760, 22), (180, 3230, 16),
    ]
    for x, y, s in big:
        sparkle(draw, x, y, s, fill=(98, 180, 220, 72), outline=(95, 165, 207, 95), width=1)
    small = [
        (232, 132), (298, 302), (952, 326), (100, 482), (1080, 650),
        (232, 930), (1016, 1136), (176, 1510), (1082, 1430), (252, 1832),
        (1010, 2088), (120, 2495), (1088, 2442), (240, 2906), (982, 3140),
    ]
    for x, y in small:
        sparkle(draw, x, y, 8, fill=(99, 174, 216, 95))
    for x, y in [(340, 160), (890, 560), (315, 1190), (930, 1515), (335, 2580), (915, 2940)]:
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(88, 165, 210, 110))


def draw_orbit_tags(draw, x, y, w, tags):
    h = 178
    cx = x + w / 2
    cy = y + h / 2 + 4
    rx = w / 2 - 88
    ry = h / 2 - 32
    orbit_box = (cx - rx, cy - ry, cx + rx, cy + ry)
    for start in range(0, 360, 32):
        draw.arc(orbit_box, start, start + 18, fill=(151, 207, 234, 145), width=2)
    draw.arc((cx - rx * .72, cy - ry * .64, cx + rx * .72, cy + ry * .64), 18, 340, fill=(207, 234, 246, 120), width=1)
    sparkle(draw, cx, cy, 18, fill=(77, 157, 202, 120), outline=(93, 171, 213, 95), width=1)

    if len(tags) == 6:
        positions = [
            (cx - rx + 36, cy - 34),
            (cx - rx + 36, cy + 34),
            (cx, cy - 58),
            (cx, cy + 58),
            (cx + rx - 36, cy - 34),
            (cx + rx - 36, cy + 34),
        ]
    else:
        angles = [-160, -105, -50, 0, 50, 105, 160]
        positions = []
        for deg in angles:
            rad = math.radians(deg)
            positions.append((cx + math.cos(rad) * rx, cy + math.sin(rad) * ry))
    for label, (tx, ty) in zip(tags, positions):
        bw = 108
        bh = 46
        bx = tx - bw / 2
        by = ty - bh / 2
        rounded(draw, (bx, by, bx + bw, by + bh), 23, (247, 252, 255), outline=(187, 224, 241), width=1)
        tw, th = text_size(draw, label, F["note"])
        group_w = tw + 42
        gx = bx + (bw - group_w) / 2
        sparkle(draw, gx + 7, by + 22, 5, fill=(75, 155, 200, 155))
        draw_text_center_y(draw, gx + 21, by + bh / 2, label, F["note"], INK)
        sparkle(draw, gx + 21 + tw + 14, by + 22, 5, fill=(75, 155, 200, 155))
    return h


def service_card(draw, y, en, zh, price_main, price_sub, desc, chips, points, note, structured_points=None, orbit_tags=None):
    x, w = 88, W - 176
    desc_w = w - 365
    desc_y = y + 188
    desc_h = paragraph_height(draw, desc, F["body"], desc_w, 11)
    chip_y = max(y + 282, desc_y + desc_h + 24)
    chip_boxes = []
    cx = x + 48
    cy = chip_y
    if orbit_tags:
        chip_bottom = chip_y + 178
    else:
        for label in chips:
            tw, _ = text_size(draw, label, F["note"])
            chip_w = tw + 50
            if cx + chip_w > x + w - 48:
                cx = x + 48
                cy += 64
            chip_boxes.append((label, cx, cy, chip_w))
            cx += chip_w + 18
        chip_bottom = cy + 52

    rows = math.ceil(len(points) / 2)
    extra_structured = 0
    if structured_points:
        for _, st_rows in structured_points:
            cols = 2 if len(st_rows) >= 4 else min(len(st_rows), 3)
            st_row_count = math.ceil(len(st_rows) / cols)
            extra_structured += 48 + st_row_count * 66 + (st_row_count - 1) * 14 + 30
    grid_top = chip_bottom + 42
    row_h = 88
    points_height = rows * row_h + max(0, rows - 1) * 22 if points else 0
    grid_bottom = grid_top + extra_structured + points_height
    note_text = "说明：" + note
    note_y = grid_bottom + 82
    note_h = paragraph_height(draw, note_text, F["note"], w - 122, 8)
    box_h = note_y - y + note_h + 70
    rounded(draw, (x, y, x + w, y + box_h), 0, PAPER, outline=LINE, width=2)
    draw.rectangle((x + 18, y + 18, x + w - 18, y + box_h - 18), outline=(222, 239, 248), width=1)

    draw.text((x + 48, y + 52), " ".join(en), font=F["h_en"], fill=(105, 158, 189))
    draw.text((x + 48, y + 86), zh, font=F["h"], fill=INK)
    price_x1 = x + w - 300
    price_x2 = x + w - 46
    draw_center_in(draw, (price_x1, y + 54, price_x2, y + 120), price_main, F["price"], fill=(32, 73, 100))
    draw_center_in(draw, (price_x1, y + 142, price_x2, y + 170), price_sub, F["small"], fill=MUTED)

    paragraph(draw, (x + 48, desc_y), desc, F["body"], INK, desc_w, 11)

    if orbit_tags:
        draw_orbit_tags(draw, x + 48, chip_y, w - 96, orbit_tags)
    else:
        for label, bx, by, chip_w in chip_boxes:
            rounded(draw, (bx, by, bx + chip_w, by + 52), 26, (235, 247, 253), outline=(191, 224, 241), width=1)
            tw, _ = text_size(draw, label, F["note"])
            draw_text_center_y(draw, bx + (chip_w - tw) / 2, by + 26, label, F["note"], INK)

    if structured_points:
        for st_title, st_rows in structured_points:
            cols = 2 if len(st_rows) >= 4 else min(len(st_rows), 3)
            st_row_count = math.ceil(len(st_rows) / cols)
            item_w = (w - 96 - (cols - 1) * 14) / cols
            item_h = 66
            title_y = grid_top
            draw.text((x + 48, title_y), st_title, font=F["body_b"], fill=INK)
            item_y = title_y + 48
            for idx, (label, detail) in enumerate(st_rows, start=1):
                col = (idx - 1) % cols
                row = (idx - 1) // cols
                bx = x + 48 + col * (item_w + 14)
                by = item_y + row * (item_h + 14)
                rounded(draw, (bx, by, bx + item_w, by + item_h), 0, CARD, outline=(221, 238, 247), width=1)
                sparkle(draw, bx + 31, by + 33, 10, fill=(75, 155, 200, 180))
                draw_text_center_y(draw, bx + 58, by + item_h / 2, f"{label} {detail}", F["mini"], INK)
            grid_top = item_y + st_row_count * item_h + (st_row_count - 1) * 14 + 30

    if points:
        col_w = (w - 110) / 2
        for i, p in enumerate(points):
            col = i % 2
            row = i // 2
            bx = x + 48 + col * (col_w + 14)
            by = grid_top + row * (row_h + 22)
            rounded(draw, (bx, by, bx + col_w, by + row_h), 0, CARD, outline=(221, 238, 247), width=1)
            sparkle(draw, bx + 30, by + 40, 11, fill=(75, 155, 200, 180))
            paragraph_center_y(draw, bx + 54, by + row_h / 2, p, F["note"], INK, col_w - 74, 6)

    draw.line((x + 48, note_y + 8, x + 48, note_y + note_h - 2), fill=ACCENT, width=5)
    paragraph(draw, (x + 72, note_y), note_text, F["note"], INK, w - 122, 8)
    return y + box_h + 52


def small_section(draw, y, title, rows, dark=False):
    x, w = 88, W - 176
    fill = (229, 246, 254) if dark else PAPER
    text = INK
    muted = MUTED
    line = (181, 218, 237) if dark else (222, 239, 248)
    h = 440 if dark and len(rows) <= 4 else 390 if len(rows) <= 3 else 420
    rounded(draw, (x, y, x + w, y + h), 0, fill, outline=LINE, width=2)
    draw.text((x + 48, y + 44), title, font=F["h"], fill=text)
    cy = y + 150
    left_x = x + 48
    right_x = x + 470
    right_w = x + w - 48 - right_x
    left_font = F["table"] if dark else F["body"]
    right_font = F["table_b"] if dark else F["body_b"]
    row_step = 72 if dark else 66
    line_offset = 56 if dark else 50
    for l, r in rows:
        draw.text((left_x, cy), l, font=left_font, fill=muted)
        paragraph(draw, (right_x, cy), r, right_font, text, right_w, 6)
        if cy + line_offset < y + h - 48:
            draw.line((x + 48, cy + line_offset, x + w - 48, cy + line_offset), fill=line, width=1)
        cy += row_step
    return y + h + 52


img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

# Soft white-blue glow
for r, alpha in [(980, 70), (700, 55), (460, 40)]:
    draw.ellipse((W / 2 - r / 2, 42, W / 2 + r / 2, 42 + r * .72), fill=(231, 247, 255, alpha))
draw_star_field(draw)

draw.rounded_rectangle((38, 28, W - 38, H - 28), 42, outline=(126, 184, 214), width=2)
draw.rounded_rectangle((52, 42, W - 52, H - 42), 34, outline=(218, 238, 248), width=1)
for x in [W / 2 - 78, W / 2, W / 2 + 78]:
    sparkle(draw, x, 38, 13, fill=(61, 139, 184, 170))

y = 390
draw_center(draw, y, "M Y S T I C   S E R V I C E   P R I C E   L I S T", F["eyebrow"], fill=(91, 137, 166))
y += 50
draw_center(draw, y, "神秘学咨询服务价目表", F["title"], fill=INK)
y += 102
draw_center(draw, y, "Lian Yue Xian", F["brand"], fill=(58, 102, 130))
y += 62
draw_center(draw, y, "塔罗 · 阿卡西记录  |  适合近期问题、关系议题与灵性探索", F["body"], fill=MUTED)
y += 50
rounded(draw, (300, y, W - 300, y + 58), 0, (255, 255, 255), outline=LINE, width=1)
draw_center(draw, y + 14, "咨询形式：文字 / 语音条 / 语音电话，可按项目沟通", F["note"], fill=INK)
y += 108

y = service_card(
    draw, y, "TAROT READING", "塔罗牌咨询",
    "68元", "塔罗单项",
    "适合解析近期具体问题，例如关系后续发展、选择判断、当下状态与行动建议。",
    [],
    [],
    "塔罗更适合看“近期具体事件与行动建议”，问题越清晰，解读越精准。可自带牌阵，每张牌均价20元。",
    structured_points=[
        ("不占主题", [
            ("生死健康", "相关"),
            ("考试", "是否通过"),
            ("投资/博彩", "相关"),
            ("国家/法律", "相关"),
            ("无关他人", "隐私窥探"),
            ("不信/无事", "不占"),
        ]),
    ],
    orbit_tags=["感情", "事业", "运势", "人际", "状态", "桃花"]
)

y = service_card(
    draw, y, "AKASHIC RECORDS", "阿卡西记录解读",
    "188元", "30分钟",
    "适合探索灵魂课题、关系牵引、重复模式、前世影响、潜意识阻碍与当下阶段的高我指引。",
    ["30分钟188元", "准备3-4个问题", "超时5分钟30元"],
    [
        "个人灵魂探索：天赋才华、今生课题、前世故事",
        "情感关系：父母、爱人、朋友等亲密关系类型",
        "事业财富：财务卡点、职业选择、工作问题",
        "身心健康：身体疾病的实相与可能原因",
        "特殊类目：宠物沟通、物品能量解读",
        "更适合开放式探索，不适合替代现实决策",
    ],
    "阅读前24小时不饮酒、不吃生食，保持放松；需提供姓名与生日，提问时选择开放式问题。"
)

y = small_section(draw, y, "下单流程", [
    ("1 选择服务", "确认塔罗 / 阿卡西与对应套餐"),
    ("2 私信沟通", "说明问题、需求与背景信息"),
    ("3 付款预约", "扫码付款后截图，预约解读时间"),
    ("4 等待解读", "默认语音条，语音电话可提前沟通"),
], dark=True)

y = small_section(draw, y, "咨询前请准备", [
    ("塔罗类", "一个清晰、具体、与自己相关的问题"),
    ("阿卡西类", "想探索的主题或困扰，建议3-4问"),
    ("提问原则", "真实开放，不窥探隐私，不只求指定答案"),
], dark=False)

footer_1 = "所有解读以帮助你理解自身状态、梳理方向和看见可能性为主。"
footer_2 = "温馨提示：玄学咨询不替代医疗、法律、心理治疗或财务投资建议。"
footer_y = y + 14
paragraph_center(draw, footer_y, footer_1, F["mini"], MUTED, W - 284, 8)
paragraph_center(draw, footer_y + 42, footer_2, F["mini"], MUTED, W - 284, 8)

# Subtle texture
noise = Image.effect_noise((W, H), 9).convert("L")
texture = Image.new("RGB", (W, H), (255, 255, 255))
texture.putalpha(noise.point(lambda p: int(p * 0.08)))
img = Image.alpha_composite(img.convert("RGBA"), texture).convert("RGB")

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, quality=98)
print(OUT)
