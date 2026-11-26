"""HUDdy palette. Source of truth: HUDdy Soft Contrast Spec 1.0
(/workspace/handover/HUDdy-Soft-Contrast/HUDdy-Soft-Contrast-Spec-1.0.md, sha256 8626a226adcd441356bd87a21b5db5a5e345997084d33602a7e440978686e5f9).
Soft values lift the 1.0 near-blacks and cap the brightest whites; hues stay within ±2° and accents are unchanged.
"""

def _h(c): c = c.lstrip('#'); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
def mix(a, b, t):
    A, B = _h(a), _h(b)
    return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(A, B))
def rgb(c): return ', '.join(str(v) for v in _h(c))

# --- Soft Contrast Spec 1.0 §2 (canonical HUDdy) ---
BG = '#080e19'; SURFACE = '#0d192c'; PANEL = '#112138'; FG = '#c2cfdc'; MUTED = '#7d93ad'
ACCENT = '#5ee1ff'; SECONDARY = '#93a8bf'; OK = '#3dffa8'; WARN = '#ffb547'; ERR = '#ff5470'
NEON = '#3ef0ff'; MIDNIGHT = '#64d2ff'   # branches 7 and 8
DISABLED = '#2e3744'
INK_HIGH = '#d6e4f2'; PANE = '#275e6d'; HAIRLINE = '#1b2e41'; SEL = '#142c3d'; BRACKET = '#47aac2'; ON_ACCENT = '#080e19'
# Mix target only (bright ANSI and gradients that must stay at their 1.0 values). Never a theme token.
MIX_WHITE = '#ffffff'
# Decorative derived tokens stay at their 1.0 values (spec §2, §4.2): do not re-mix toward the lifted background.
_DERIVE_BG = '#03060b'
MAGENTA = '#c792ff'                      # no magenta/purple exists in HUDdy; picked to sit at the palette's lightness
def bright(c): return mix(c, MIX_WHITE, 0.3)   # bright ANSI variants: 30% toward white (unchanged from 1.0)
DIM = lambda c, t=0.6: mix(c, _DERIVE_BG, t)   # dim graph starts: 60% toward the 1.0 background
INACTIVE = mix(MUTED, _DERIVE_BG, 0.5)         # #404c5c
FAINT = mix(MUTED, _DERIVE_BG, 0.25)           # #5e7084

ANSI = [DISABLED, ERR, OK, WARN, MIDNIGHT, MAGENTA, ACCENT, SECONDARY,
        MUTED, bright(ERR), bright(OK), bright(WARN), bright(MIDNIGHT), bright(MAGENTA), NEON, INK_HIGH]
