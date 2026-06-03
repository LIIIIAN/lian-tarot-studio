from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W, H = 1242, 2000
BASE = Path("/Users/ninez/Documents/海报")

BG = (248, 252, 255)
PAPER = (255, 255, 255)
CARD = (249, 253, 255)
INK = (38, 55, 74)
MUTED = (101, 128, 153)
LINE = (184, 218, 238)
ACCENT = (72, 154, 198)

FONT_SONG_LIGHT = "/Users/ninez/Library/Fonts/SOURCEHANSERIFSC-LIGHT.OTF"
FONT_SONG_MEDIUM = "/Users/ninez/Library/Fonts/SourceHanSerifCN-Medium-6.otf"
FONT_SONG_BOLD = "/Users/ninez/Library/Fonts/SOURCEHANSERIFSC-BOLD.OTF"
FONT_SONG_HEAVY = "/Users/ninez/Library/Fonts/SOURCEHANSERIFSC-HEAVY.OTF"
FONT_AVENIR = "/System/Library/Fonts/Avenir.ttc"
FONT_BODONI = "/System/Library/Fonts/Supplemental/Bodoni 72 OS.ttc"


def font(path, size):
    return ImageFont.truetype(path, size)


F = {
    "eyebrow": font(FONT_AVENIR, 25),
    "title": font(FONT_SONG_HEAVY, 68),
    "brand": font(FONT_BODONI, 36),
    "subtitle": font(FONT_SONG_LIGHT, 28),
    "section": font(FONT_SONG_BOLD, 39),
    "body": font(FONT_SONG_LIGHT, 31),
    "note": font(FONT_SONG_LIGHT, 24),
    "card_num": font(FONT_BODONI, 56),
}


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def center(draw, y, text, fnt, fill=INK):
    tw, th = text_size(draw, text, fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)
    return y + th


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
    for x, y, s in [
        (136, 220, 22), (1018, 185, 28), (1075, 420, 18), (178, 615, 16),
        (1080, 930, 16), (118, 1320, 14), (1060, 1660, 18),
    ]:
        sparkle(draw, x, y, s, fill=(98, 180, 220, 70), outline=(95, 165, 207, 90))
    for x, y in [
        (232, 132), (298, 302), (952, 326), (100, 482), (1080, 650),
        (232, 1010), (1016, 1180), (176, 1510), (1082, 1430), (930, 1780),
    ]:
        sparkle(draw, x, y, 8, fill=(99, 174, 216, 95))


def draw_card(draw, cx, cy, number, w=84, h=120):
    x1, y1 = cx - w / 2, cy - h / 2
    x2, y2 = cx + w / 2, cy + h / 2
    draw.rounded_rectangle((x1, y1, x2, y2), 15, fill=(244, 251, 255), outline=(159, 205, 228), width=2)
    draw.rounded_rectangle((x1 + 10, y1 + 10, x2 - 10, y2 - 10), 10, outline=(211, 235, 247), width=2)
    for radius, alpha in [(39, 28), (29, 44), (18, 68)]:
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(95, 178, 218, alpha), width=2)
    for angle in range(0, 360, 45):
        a = math.radians(angle)
        sparkle(draw, cx + math.cos(a) * 43, cy + math.sin(a) * 43, 5, fill=(108, 190, 226, 115))
    sparkle(draw, cx, cy, 18, fill=(90, 172, 213, 125), outline=(83, 159, 202, 110))
    tw, th = text_size(draw, str(number), F["card_num"])
    draw.rounded_rectangle((cx - tw / 2 - 12, cy - th / 2 - 5, cx + tw / 2 + 12, cy + th / 2 + 8), 10, fill=(255, 255, 255, 205))
    draw.text((cx - tw / 2, cy - th / 2 - 8), str(number), font=F["card_num"], fill=INK)


def make_canvas():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    for r, alpha in [(980, 70), (700, 55), (460, 40)]:
        draw.ellipse((W / 2 - r / 2, 42, W / 2 + r / 2, 42 + r * .72), fill=(231, 247, 255, alpha))
    star_field(draw)
    draw.rounded_rectangle((38, 28, W - 38, H - 28), 42, outline=(126, 184, 214), width=2)
    draw.rounded_rectangle((52, 42, W - 52, H - 42), 34, outline=(218, 238, 248), width=1)
    for x in [W / 2 - 78, W / 2, W / 2 + 78]:
        sparkle(draw, x, 38, 13, fill=(61, 139, 184, 170))
    return img, draw


def save_outputs(img, name, preview_name):
    jpg = BASE / f"{name}_最终版.jpg"
    preview = BASE / preview_name
    img.save(jpg, quality=95, subsampling=0)
    img.resize((621, round(H * 621 / W)), Image.Resampling.LANCZOS).save(preview, quality=92)
    print(jpg)


def make_spread(name, english, subtitle, positions, meanings, note, card_w=84, card_h=120):
    img, draw = make_canvas()
    y = 224
    center(draw, y, f"TAROT SPREAD · {english}", F["eyebrow"], fill=(91, 137, 166))
    y += 52
    title_font = F["title"] if len(name) <= 7 else font(FONT_SONG_HEAVY, 59)
    center(draw, y, name, title_font)
    y += 92
    center(draw, y, "Lian Yue Xian", F["brand"], fill=(58, 102, 130))
    y += 64
    center(draw, y, subtitle, F["subtitle"], fill=MUTED)

    box = (145, 570, W - 145, 1218)
    draw.rectangle(box, fill=PAPER, outline=LINE, width=2)
    draw.rectangle((box[0] + 18, box[1] + 18, box[2] - 18, box[3] - 18), outline=(222, 239, 248), width=1)
    for number, cx, cy in positions:
        draw_card(draw, cx, cy, number, card_w, card_h)

    panel = (145, 1260, W - 145, 1780)
    draw.rectangle(panel, fill=PAPER, outline=LINE, width=2)
    draw.rectangle((panel[0] + 18, panel[1] + 18, panel[2] - 18, panel[3] - 18), outline=(222, 239, 248), width=1)
    draw.text((205, 1315), "位置含义", font=F["section"], fill=INK)
    two_cols = len(meanings) > 6
    col_x = [225, 695]
    row_gap = 62 if not two_cols else 66
    for i, text in enumerate(meanings):
        col = i // math.ceil(len(meanings) / 2) if two_cols else 0
        row = i % math.ceil(len(meanings) / 2) if two_cols else i
        x = col_x[col]
        yy = 1415 + row * row_gap
        sparkle(draw, x, yy + 18, 8, fill=(75, 155, 200, 180))
        draw.text((x + 33, yy), text, font=F["body"], fill=INK)

    draw.line((165, 1840, W - 165, 1840), fill=LINE, width=1)
    center(draw, 1872, note, F["note"], fill=MUTED)
    save_outputs(img, name, f"{english.lower().replace(' ', '_')}_preview.jpg")


def make_choice_spread():
    name = "二选一牌阵"
    img, draw = make_canvas()

    y = 224
    center(draw, y, "TAROT SPREAD · CHOICE READING", F["eyebrow"], fill=(91, 137, 166))
    y += 52
    center(draw, y, name, F["title"])
    y += 92
    center(draw, y, "Lian Yue Xian", F["brand"], fill=(58, 102, 130))
    y += 64
    center(draw, y, "适合在两个方向之间进行梳理与比较", F["subtitle"], fill=MUTED)

    box = (145, 570, W - 145, 1218)
    draw.rectangle(box, fill=PAPER, outline=LINE, width=2)
    draw.rectangle((box[0] + 18, box[1] + 18, box[2] - 18, box[3] - 18), outline=(222, 239, 248), width=1)
    positions = {
        1: (W / 2, 1049),
        2: (W / 2 - 182, 894),
        3: (W / 2 + 182, 894),
        4: (W / 2 - 300, 739),
        5: (W / 2 + 300, 739),
    }
    for number, (cx, cy) in positions.items():
        draw_card(draw, cx, cy, number)
    draw.line((W / 2 - 9, 986, W / 2 - 132, 934), fill=(183, 220, 238), width=3)
    draw.line((W / 2 + 9, 986, W / 2 + 132, 934), fill=(183, 220, 238), width=3)
    draw.line((W / 2 - 182, 834, W / 2 - 270, 779), fill=(183, 220, 238), width=3)
    draw.line((W / 2 + 182, 834, W / 2 + 270, 779), fill=(183, 220, 238), width=3)

    panel = (145, 1260, W - 145, 1780)
    draw.rectangle(panel, fill=PAPER, outline=LINE, width=2)
    draw.rectangle((panel[0] + 18, panel[1] + 18, panel[2] - 18, panel[3] - 18), outline=(222, 239, 248), width=1)
    draw.text((205, 1315), "位置含义", font=F["section"], fill=INK)
    meanings = [
        "1：事情的现状",
        "2：选择 A 的发展",
        "3：选择 B 的发展",
        "4：选择 A 的结果",
        "5：选择 B 的结果",
    ]
    yy = 1415
    for text in meanings:
        sparkle(draw, 230, yy + 18, 8, fill=(75, 155, 200, 180))
        draw.text((263, yy), text, font=F["body"], fill=INK)
        yy += 62

    draw.line((165, 1840, W - 165, 1840), fill=LINE, width=1)
    center(draw, 1872, "补充说明：如需第三或第四个选项，可对应增加两张牌。", F["note"], fill=MUTED)

    save_outputs(img, name, "choice_spread_preview.jpg")


if __name__ == "__main__":
    make_choice_spread()
    make_spread(
        "十字关系牌阵",
        "RELATIONSHIP CROSS",
        "适合梳理人际与情感关系中的彼此感受",
        [
            (3, W / 2, 739),
            (1, W / 2 - 250, 894),
            (4, W / 2, 894),
            (2, W / 2 + 250, 894),
            (5, W / 2, 1049),
        ],
        ["1：当事人的感受", "2：对方的感受", "3：环境", "4：现在", "5：未来"],
        "适合用于理解一段关系目前所处的位置，以及接下来的发展方向。",
    )
    make_spread(
        "恋人维纳斯牌阵",
        "VENUS LOVE",
        "适合观察恋爱关系中的行动、想法与未来走向",
        [
            (3, W / 2, 662),
            (1, W / 2 - 215, 817),
            (2, W / 2 + 215, 817),
            (4, W / 2, 817),
            (6, W / 2 - 215, 972),
            (5, W / 2, 972),
            (7, W / 2 + 215, 972),
            (8, W / 2, 1127),
        ],
        [
            "1：求问者行动表现", "2：对方行动表现", "3：环境外界影响", "4：目前发展状况",
            "5：障碍或帮助", "6：求问者内心想法", "7：对方内心想法", "8：未来结果",
        ],
        "从双方表现、内心想法与外界影响出发，完整观察恋爱关系的发展状态。",
    )
    make_spread(
        "X情人复合牌阵",
        "RECONNECTION",
        "适合梳理复合议题中的现状、阻碍与可能结果",
        [
            (1, W / 2 - 330, 662),
            (2, W / 2 - 200, 817),
            (3, W / 2, 894),
            (8, W / 2 - 200, 972),
            (9, W / 2 - 330, 1127),
            (6, W / 2 + 330, 662),
            (7, W / 2 + 200, 817),
            (4, W / 2 + 200, 972),
            (5, W / 2 + 330, 1127),
        ],
        [
            "1：你们的过去", "2：求问者的现状", "3：旧情人的现状", "4：求问者真实感受",
            "5：旧情人真实感受", "6：复合的阻碍", "7：复合的帮助", "8：尚未知晓的事", "9：整体结果",
        ],
        "复合牌阵用于观察关系状态与影响因素，不代表对未来结果的保证。",
    )
    make_spread(
        "四季牌阵",
        "SEASONAL OUTLOOK",
        "适合在节气节点回顾未来三个月的整体方向",
        [
            (5, W / 2, 739),
            (3, W / 2 - 225, 894),
            (1, W / 2, 894),
            (2, W / 2 + 225, 894),
            (4, W / 2, 1049),
        ],
        [
            "1：本季度整体运势", "2：风 · 宝剑｜计划 / 决策 / 学习", "3：火 · 权杖｜事业 / 目标 / 行动力",
            "4：水 · 圣杯｜感情 / 人际 / 情绪", "5：土 · 星币｜财务 / 健康 / 安全感",
        ],
        "一年四次使用机会：春分、夏至、秋分、冬至，各观测未来三个月。",
    )
