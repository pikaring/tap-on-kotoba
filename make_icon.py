# -*- coding: utf-8 -*-
"""紹介ページ用のアイコンを生成する。

ゲームの画面そのものを絵にする。空欄の青を下地に、選択肢のタイルを2枚。
奥は墨の「言」、手前は空欄の「？」。外部の画像素材は使わず、ここで描く。

    py make_icon.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
S = 1024

BLUE = (26, 78, 138)        # 下地（空欄の青）
BLUE_DEEP = (20, 60, 108)   # 下地の陰
TILE = (253, 250, 243)      # タイルの面（生成り）
TILE_EDGE = (200, 187, 160)
INK = (27, 25, 21)          # 「言」
GREEN = (19, 107, 58)       # 正解の緑（アクセント）

# Windows（作業環境）→ Linux（CI やコンテナ）の順に探す
FONTS = [
    r'C:\Windows\Fonts\meiryob.ttc', r'C:\Windows\Fonts\YuGothB.ttc',
    r'C:\Windows\Fonts\BIZ-UDGothicB.ttc', r'C:\Windows\Fonts\msgothic.ttc',
    '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
    '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf',
]


def font(size):
    for p in FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def tile(img, x, y, w, h, angle, text, color, underline=False):
    """角の丸いタイルを1枚、少し傾けて貼る。"""
    pad = int(S * 0.06)
    layer = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = int(S * 0.035)
    # 下の縁（厚み）
    d.rounded_rectangle((pad, pad + int(S * 0.016), pad + w, pad + h + int(S * 0.016)),
                        radius=r, fill=TILE_EDGE)
    d.rounded_rectangle((pad, pad, pad + w, pad + h), radius=r, fill=TILE,
                        outline=TILE_EDGE, width=int(S * 0.007))
    f = font(int(h * 0.62))
    bb = d.textbbox((0, 0), text, font=f)
    tx = pad + (w - (bb[2] - bb[0])) / 2 - bb[0]
    ty = pad + (h - (bb[3] - bb[1])) / 2 - bb[1] - (h * 0.04 if underline else 0)
    d.text((tx, ty), text, font=f, fill=color)
    if underline:
        uw = int(w * 0.46)
        uy = pad + int(h * 0.80)
        d.rounded_rectangle((pad + (w - uw) // 2, uy, pad + (w + uw) // 2, uy + int(S * 0.022)),
                            radius=int(S * 0.011), fill=color)
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(layer, (x - (layer.width - w) // 2, y - (layer.height - h) // 2))


def draw(img):
    d = ImageDraw.Draw(img)
    # 下地：上から下へ、青がゆっくり深くなる
    grad = Image.new('RGB', (1, S))
    gd = ImageDraw.Draw(grad)
    for y in range(S):
        t = y / (S - 1)
        gd.point((0, y), fill=tuple(round(a + (b - a) * t) for a, b in zip(BLUE, BLUE_DEEP)))
    grad = grad.resize((S, S)).convert('RGBA')
    mask = Image.new('L', (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, S, S), radius=int(S * 0.22), fill=255)
    img.paste(grad, (0, 0), mask)
    # 進み具合の帯（小さいサイズでは消える程度に薄く）
    for i in range(4):
        x = int(S * (0.20 + i * 0.16))
        c = GREEN if i < 2 else (74, 118, 170)
        d.rounded_rectangle((x, int(S * 0.115), x + int(S * 0.11), int(S * 0.155)),
                            radius=int(S * 0.02), fill=c)

    w, h = int(S * 0.40), int(S * 0.46)
    tile(img, int(S * 0.10), int(S * 0.30), w, h, 7, '言', INK)
    tile(img, int(S * 0.50), int(S * 0.36), w, h, -6, '？', BLUE, underline=True)


img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
draw(img)

os.makedirs(ASSETS, exist_ok=True)
img.resize((512, 512), Image.LANCZOS).save(os.path.join(ASSETS, 'icon.png'))
img.save(os.path.join(ASSETS, 'favicon.ico'), sizes=[(48, 48), (32, 32), (16, 16)])
print('書き出し:', os.path.join(ASSETS, 'icon.png'))
print('書き出し:', os.path.join(ASSETS, 'favicon.ico'))

sizes = [256, 128, 64, 48, 32, 16]
strip = Image.new('RGBA', (sum(sizes) + 20 * len(sizes), 280), (250, 250, 250, 255))
x = 10
for s in sizes:
    small = img.resize((s, s), Image.LANCZOS)
    strip.paste(small, (x, 10), small)
    x += s + 20
strip.save(os.path.join(HERE, 'icon_preview.png'))
print('確認用:', os.path.join(HERE, 'icon_preview.png'))

# 小さいサイズでも各要素が残っているかを画素で確認する
print('\n--- 小サイズでの見え方（色の占める割合）---')
for s in (48, 32, 16):
    im = img.resize((s, s), Image.LANCZOS).convert('RGB')
    px = list(im.convert('RGB').getdata())
    tile_px = sum(1 for c in px if c[0] > 215 and c[1] > 205 and c[2] > 180)
    blue_px = sum(1 for c in px if c[2] - c[0] > 40 and c[2] > 70)
    green_px = sum(1 for c in px if c[1] - c[0] > 25 and c[1] - c[2] > 25)
    print(f'  {s:>3}px: タイル(生成り) {tile_px / len(px) * 100:4.1f}%  '
          f'下地(青) {blue_px / len(px) * 100:4.1f}%  進み具合(緑) {green_px / len(px) * 100:4.1f}%')
