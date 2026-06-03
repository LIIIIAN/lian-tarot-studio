from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W, H = 1242, 3460
BASE = Path("/Users/ninez/Documents/海报")
PNG = BASE / "阿卡西记录可探索方向.png"
JPG = BASE / "阿卡西记录可探索方向_最终版.jpg"
PREVIEW = BASE / "akashic_directions.jpg"

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
    "eyebrow": font(FONT_AVENIR, 27),
    "title": font(FONT_SONG_HEAVY, 64),
    "brand": font(FONT_BODONI, 38),
    "h_en": font(FONT_AVENIR, 20),
    "h": font(FONT_SONG_BOLD, 39),
    "section": font(FONT_SONG_MEDIUM, 29),
    "body": font(FONT_SONG_LIGHT, 25),
    "note": font(FONT_SONG_LIGHT, 23),
    "mini": font(FONT_SONG_LIGHT, 20),
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


def paragraph(draw, x, y, text, fnt, fill, max_w, gap=10):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def center(draw, y, text, fnt, fill=INK):
    tw, th = text_size(draw, text, fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)
    return y + th


def center_box(draw, box, text, fnt, fill=INK):
    x1, y1, x2, y2 = box
    tb = draw.textbbox((0, 0), text, font=fnt)
    tw = tb[2] - tb[0]
    text_y = y1 + (y2 - y1) / 2 - (tb[1] + tb[3]) / 2 - 2
    draw.text((x1 + (x2 - x1 - tw) / 2, text_y), text, font=fnt, fill=fill)


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
                    (1080, 930, 16), (118, 1320, 14), (1060, 1660, 18), (180, 2140, 16),
                    (1030, 2630, 16), (190, 3060, 14)]:
        sparkle(draw, x, y, s, fill=(98, 180, 220, 70), outline=(95, 165, 207, 90))
    for x, y in [(232, 132), (298, 302), (952, 326), (100, 482), (1080, 650),
                 (232, 1010), (1016, 1180), (176, 1510), (1082, 1430), (252, 1832),
                 (1000, 2180), (240, 2450), (930, 2960), (300, 3260)]:
        sparkle(draw, x, y, 8, fill=(99, 174, 216, 95))


def card(draw, x, y, w, title, questions):
    padding = 32
    title_h = 44
    line_h = 33
    body_lines = []
    for q in questions:
        body_lines.append(wrap(draw, q, F["body"], w - padding * 2 - 34))
    h = padding + title_h + 24 + sum(len(lines) * line_h + 10 for lines in body_lines) + padding - 8
    round_rect(draw, (x, y, x + w, y + h), 0, PAPER, outline=LINE, width=1)
    tw, _ = text_size(draw, title, F["section"])
    draw.text((x + (w - tw) / 2, y + padding), title, font=F["section"], fill=INK)
    cy = y + padding + title_h + 16
    for lines in body_lines:
        sparkle(draw, x + padding + 10, cy + 14, 7, fill=(75, 155, 200, 170))
        ly = cy
        for line in lines:
            draw.text((x + padding + 34, ly), line, font=F["body"], fill=INK)
            ly += line_h
        cy = ly + 10
    return h


sections = [
    ("人生方向与使命", [
        "我的人生课题是什么",
        "我这一阶段最需要学习什么",
        "我的天赋优势在哪里",
        "什么样的工作更适合我",
        "为什么我总是感到迷茫",
        "我的人生使命是什么",
    ]),
    ("情感与亲密关系", [
        "为什么总是吸引同类型伴侣",
        "当前关系中的课题是什么",
        "我和对方之间需要学习什么",
        "为什么很难建立稳定关系",
        "如何疗愈过去的情感创伤",
    ]),
    ("原生家庭与成长经历", [
        "我的限制性信念来自哪里",
        "为什么总想讨好别人",
        "为什么害怕被拒绝",
        "为什么缺乏安全感",
        "家庭模式如何影响我的人生",
    ]),
    ("财富与事业", [
        "财富卡点在哪里",
        "为什么努力却难以获得回报",
        "对金钱有哪些潜意识信念",
        "适合创业还是上班",
        "当前事业阶段的重点是什么",
    ]),
    ("重复出现的人生模式", [
        "为什么总遇到类似问题",
        "为什么总在关键时刻退缩",
        "为什么总感觉自己不配得到幸福",
        "为什么一直陷入同样的人际关系困境",
    ]),
    ("自我认知与内在成长", [
        "我的核心特质是什么",
        "我有哪些被忽略的优势",
        "如何建立自信",
        "如何与真实的自己连接",
        "如何减少内耗",
    ]),
    ("灵性探索", [
        "灵魂成长主题",
        "前世今生体验",
        "灵魂契约",
        "灵魂关系",
        "灵性天赋",
    ]),
    ("可定制问题", [
        "可围绕你的具体困扰定制提问",
        "适合开放式探索与深层原因梳理",
        "可根据关系、事业、家庭、自我成长调整方向",
        "建议带着一个清晰主题进入解读",
    ]),
]

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

for r, alpha in [(980, 70), (700, 55), (460, 40)]:
    draw.ellipse((W / 2 - r / 2, 42, W / 2 + r / 2, 42 + r * .72), fill=(231, 247, 255, alpha))
star_field(draw)

draw.rounded_rectangle((38, 28, W - 38, H - 28), 42, outline=(126, 184, 214), width=2)
draw.rounded_rectangle((52, 42, W - 52, H - 42), 34, outline=(218, 238, 248), width=1)
for sx in [W / 2 - 78, W / 2, W / 2 + 78]:
    sparkle(draw, sx, 38, 13, fill=(61, 139, 184, 170))

y = 345
center(draw, y, "AKASHIC RECORDS EXPLORATION", F["eyebrow"], fill=(91, 137, 166))
y += 50
center(draw, y, "阿卡西记录可探索方向", F["title"], fill=INK)
y += 90
center(draw, y, "Lian Yue Xian", F["brand"], fill=(58, 102, 130))
y += 58
center(draw, y, "灵魂课题 · 关系模式 · 内在成长 · 生命方向", F["body"], fill=MUTED)
y += 52
consult_box = (390, y, W - 390, y + 54)
round_rect(draw, consult_box, 0, (255, 255, 255), outline=LINE, width=1)
center_box(draw, consult_box, "咨询模式：文字 / 语音条 / 语音电话", F["note"], fill=INK)
y += 112

main_x, main_w = 78, W - 156
main_y = y
main_h = 2370
round_rect(draw, (main_x, main_y, main_x + main_w, main_y + main_h), 0, PAPER, outline=LINE, width=2)
draw.rectangle((main_x + 18, main_y + 18, main_x + main_w - 18, main_y + main_h - 18), outline=(222, 239, 248), width=1)

y = main_y + 50
draw.text((main_x + 48, y), "A K A S H I C   R E C O R D S", font=F["h_en"], fill=(105, 158, 189))
y += 38
draw.text((main_x + 48, y), "什么是阿卡西记录", font=F["h"], fill=INK)
y += 72
intro_box_h = 330
round_rect(draw, (main_x + 48, y, main_x + main_w - 48, y + intro_box_h), 0, CARD, outline=LINE, width=1)
intro_y = y + 34
intro_lines = [
    "阿卡西记录（Akashic Records）源于古老灵性传统。“Akasha”一词意为以太或宇宙空间。",
    "在相关传统中，阿卡西记录被描述为一个非物质的信息场域，记录着灵魂的经验、选择与成长历程。",
    "阿卡西阅读是一种透过冥想、专注与内在连接，获取关于个人成长议题洞见的实践方式。",
    "阅读的重点并非预言未来，而是帮助来访者理解当下、觉察模式，并为未来选择提供新的视角。",
]
for line in intro_lines:
    intro_y = paragraph(draw, main_x + 82, intro_y, line, F["note"], INK, main_w - 164, 7)
    intro_y += 7
y += intro_box_h + 48
draw.text((main_x + 48, y), "可探索的方向有哪些", font=F["h"], fill=INK)
y += 76
intro = "阿卡西记录更适合用来探索“为什么我会重复某种模式”“这段关系带给我的灵魂功课是什么”“我现在卡住的深层原因是什么”等开放式议题。"
y = paragraph(draw, main_x + 48, y, intro, F["body"], INK, main_w - 96, 12)
y += 42

col_gap = 24
col_w = (main_w - 96 - col_gap) / 2
left_x = main_x + 48
right_x = left_x + col_w + col_gap
col_y = [y, y]
for i, (title, qs) in enumerate(sections):
    col = i % 2
    x = left_x if col == 0 else right_x
    h = card(draw, x, col_y[col], col_w, title, qs)
    col_y[col] += h + 26

y = max(col_y) + 32
draw.line((main_x + 48, y + 8, main_x + 48, y + 92), fill=ACCENT, width=5)
paragraph(
    draw, main_x + 72, y,
    "适合带着具体主题进入探索，也适合在迷茫、反复内耗、关系或事业卡住时，梳理自己真正需要看见的深层模式。",
    F["note"], INK, main_w - 122, 8
)

footer_y = main_y + main_h + 48
note_h = 250
round_rect(draw, (main_x, footer_y, main_x + main_w, footer_y + note_h), 0, PAPER, outline=LINE, width=2)
draw.text((main_x + 48, footer_y + 44), "温馨提示", font=F["h"], fill=INK)
paragraph(
    draw, main_x + 48, footer_y + 132,
    "本服务旨在协助个人进行内在探索与能量觉察，不构成医疗、心理诊断、法律或财务建议，也不保证未来结果。",
    F["body"], INK, main_w - 96, 12
)

PNG.parent.mkdir(parents=True, exist_ok=True)
img.save(PNG, quality=98)
img.save(JPG, quality=98, optimize=True)
img.save(PREVIEW, quality=98, optimize=True)

print(PNG)
print(JPG)
print(PREVIEW)
