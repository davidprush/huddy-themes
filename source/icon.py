from PIL import Image, ImageDraw
from palette import *
S = 4; N = 128 * S
im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle([0, 0, N - 1, N - 1], radius=22 * S, fill=BG, outline=HAIRLINE, width=2 * S)
L, m, wdt = 26 * S, 14 * S, 5 * S
for (x, y, sx, sy) in [(m, m, 1, 1), (N - m, m, -1, 1), (m, N - m, 1, -1), (N - m, N - m, -1, -1)]:
    d.line([(x, y), (x + sx * L, y)], fill=ACCENT, width=wdt); d.line([(x, y), (x, y + sy * L)], fill=ACCENT, width=wdt)
c = N // 2; r = 34 * S
d.ellipse([c - r, c - r, c + r, c + r], outline=PANE, width=3 * S)
r2 = 22 * S; d.arc([c - r2, c - r2, c + r2, c + r2], 200, 340, fill=OK, width=4 * S)
d.arc([c - r2, c - r2, c + r2, c + r2], 20, 160, fill=WARN, width=4 * S)
for a, b in [((c - r - 8 * S, c), (c - r + 10 * S, c)), ((c + r - 10 * S, c), (c + r + 8 * S, c)),
             ((c, c - r - 8 * S), (c, c - r + 10 * S)), ((c, c + r - 10 * S), (c, c + r + 8 * S))]:
    d.line([a, b], fill=ACCENT, width=3 * S)
d.ellipse([c - 6 * S, c - 6 * S, c + 6 * S, c + 6 * S], fill=ERR)
import os
OUT = os.environ.get('OUT', '/workspace/huddy-1.1-src/pack')
im.resize((128, 128), Image.LANCZOS).save(os.path.join(OUT, 'vscode/huddy-theme/icon-huddy.png'))
