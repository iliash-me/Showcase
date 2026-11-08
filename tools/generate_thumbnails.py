#!/usr/bin/env python3
"""
Generate placeholder screenshots (SVG) for the showcase page.

Every demo homepage and inner page gets a tall, full-page "screenshot" that
the showcase scrolls through on hover. Once your real template is ready,
replace each generated file with a real full-page screenshot (PNG/JPG/WebP,
~800px wide) and update the matching `src` in index.html.

Usage:  python3 tools/generate_thumbnails.py
Output: assets/img/demos/*.svg, assets/img/pages/*.svg
"""
from __future__ import annotations

import os
import random
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 800          # canvas width
PAD = 64         # side padding
CW = W - PAD * 2  # content width
FONT = "Inter, 'Plus Jakarta Sans', 'Segoe UI', Helvetica, Arial, sans-serif"


# --------------------------------------------------------------------------- #
# Colour helpers
# --------------------------------------------------------------------------- #
def _rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in c)


def mix(a: str, b: str, t: float) -> str:
    A, B = _rgb(a), _rgb(b)
    return _hex([A[i] + (B[i] - A[i]) * t for i in range(3)])


def palette(primary: str, dark: bool) -> dict:
    if dark:
        bg, surface, line, heading, muted = "#0b1020", "#151b30", "#2a3352", "#eef1fa", "#39446a"
        footer = "#070a15"
    else:
        bg, surface, line, heading, muted = "#ffffff", "#f4f6fb", "#e3e7ef", "#111827", "#c9d0dd"
        footer = "#0f172a"
    return dict(
        p=primary, p2=mix(primary, "#ffffff" if dark else "#000000", 0.25),
        soft=mix(primary, bg, 0.86), bg=bg, surface=surface, line=line,
        heading=heading, muted=muted, footer=footer, dark=dark,
        card="#1a2140" if dark else "#ffffff", border="#252d4b" if dark else "#e8ebf2",
    )


# --------------------------------------------------------------------------- #
# Canvas
# --------------------------------------------------------------------------- #
class Canvas:
    def __init__(self, primary: str, dark: bool, name: str, seed: int):
        self.c = palette(primary, dark)
        self.name = name
        self.parts: list[str] = []
        self.defs: list[str] = []
        self.y = 0
        self._id = 0
        self.rnd = random.Random(seed)

    # primitives ------------------------------------------------------------ #
    def uid(self, prefix="g"):
        self._id += 1
        return f"{prefix}{self._id}"

    def add(self, s: str):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill, r=0, extra=""):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" {extra}/>')

    def circle(self, cx, cy, r, fill, extra=""):
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" {extra}/>')

    def text(self, x, y, s, size, fill, weight=700, anchor="start", spacing=-0.5):
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(s)}</text>'
        )

    def grad(self, c1, c2, vertical=False):
        gid = self.uid("lg")
        coords = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="1"'
        self.defs.append(
            f'<linearGradient id="{gid}" {coords}><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>'
        )
        return f"url(#{gid})"

    def shadow(self):
        if not any('id="sh"' in d for d in self.defs):
            self.defs.append(
                '<filter id="sh" x="-20%" y="-20%" width="140%" height="160%">'
                '<feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#0b1020" flood-opacity="0.14"/></filter>'
            )
        return 'filter="url(#sh)"'

    # composites ------------------------------------------------------------ #
    def lines(self, x, y, w, n, color=None, h=8, gap=16, center=False):
        color = color or self.c["muted"]
        for i in range(n):
            lw = w * (0.62 if i == n - 1 and n > 1 else 1)
            lx = x + (w - lw) / 2 if center else x
            self.rect(lx, y + i * gap, lw, h, color, r=h / 2)
        return y + n * gap

    def button(self, x, y, w=118, h=40, filled=True, color=None):
        color = color or self.c["p"]
        if filled:
            self.rect(x, y, w, h, color, r=8)
            self.rect(x + 22, y + h / 2 - 4, w - 44, 8, "#ffffff", r=4, extra='opacity="0.9"')
        else:
            self.rect(x + 1, y + 1, w - 2, h - 2, "none", r=8, extra=f'stroke="{self.c["border"] if self.c["dark"] else "#d5dae5"}" stroke-width="2"')
            self.rect(x + 22, y + h / 2 - 4, w - 44, 8, self.c["heading"], r=4, extra='opacity="0.75"')

    def image(self, x, y, w, h, r=14, kind=None):
        """Decorative image placeholder."""
        c = self.c
        kind = kind or self.rnd.choice(["landscape", "abstract", "person", "abstract"])
        clip = self.uid("cp")
        self.defs.append(f'<clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>')
        a = mix(c["p"], "#ffffff", 0.55)
        b = c["p"]
        self.add(f'<g clip-path="url(#{clip})">')
        if kind == "landscape":
            self.rect(x, y, w, h, self.grad(a, b, vertical=True))
            self.circle(x + w * 0.72, y + h * 0.3, min(w, h) * 0.1, "#ffffff", 'opacity="0.85"')
            self.add(
                f'<polygon points="{x},{y + h} {x + w * 0.32},{y + h * 0.48} {x + w * 0.6},{y + h} " fill="#ffffff" opacity="0.35"/>'
                f'<polygon points="{x + w * 0.3},{y + h} {x + w * 0.66},{y + h * 0.55} {x + w},{y + h * 0.82} {x + w},{y + h}" fill="#ffffff" opacity="0.55"/>'
            )
        elif kind == "person":
            self.rect(x, y, w, h, self.grad(mix(c["p"], "#ffffff", 0.75), mix(c["p"], "#ffffff", 0.35)))
            s = min(w, h)
            self.circle(x + w / 2, y + h * 0.42, s * 0.16, mix(c["p"], "#000000", 0.25), 'opacity="0.55"')
            self.add(
                f'<ellipse cx="{x + w / 2:.1f}" cy="{y + h * 0.98:.1f}" rx="{s * 0.34:.1f}" ry="{s * 0.3:.1f}" '
                f'fill="{mix(c["p"], "#000000", 0.25)}" opacity="0.55"/>'
            )
        elif kind == "dashboard":
            self.rect(x, y, w, h, c["card"])
            self.rect(x, y, w * 0.2, h, mix(c["card"], c["p"], 0.06))
            for i in range(6):
                self.rect(x + 14, y + 22 + i * 22, w * 0.2 - 28, 8, c["muted"] if i else c["p"], r=4)
            ix = x + w * 0.2 + 18
            iw = w * 0.8 - 36
            kw = (iw - 24) / 3
            for i in range(3):
                self.rect(ix + i * (kw + 12), y + 18, kw, 54, mix(c["card"], c["p"], 0.08 if i else 0.9), r=8)
                self.rect(ix + i * (kw + 12) + 12, y + 32, kw * 0.5, 7, "#ffffff" if i == 0 else c["muted"], r=3)
                self.rect(ix + i * (kw + 12) + 12, y + 48, kw * 0.32, 12, "#ffffff" if i == 0 else c["heading"], r=4, extra='opacity="0.8"')
            cy0 = y + 90
            ch = h - 110
            self.rect(ix, cy0, iw * 0.62, ch, mix(c["card"], c["p"], 0.04), r=8)
            pts = []
            for i in range(9):
                px = ix + 14 + i * (iw * 0.62 - 28) / 8
                py = cy0 + ch - 18 - (ch - 40) * (0.25 + 0.6 * self.rnd.random() * (0.5 + i / 16))
                pts.append(f"{px:.1f},{py:.1f}")
            self.add(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c["p"]}" stroke-width="3" stroke-linejoin="round"/>')
            bx = ix + iw * 0.62 + 12
            bw = iw * 0.38 - 12
            self.rect(bx, cy0, bw, ch, mix(c["card"], c["p"], 0.04), r=8)
            for i in range(5):
                bh = (ch - 40) * (0.3 + 0.7 * self.rnd.random())
                self.rect(bx + 12 + i * (bw - 24) / 5, cy0 + ch - 14 - bh, (bw - 24) / 5 - 6, bh, c["p"], r=3,
                          extra=f'opacity="{0.45 + i * 0.1:.2f}"')
        else:  # abstract
            self.rect(x, y, w, h, self.grad(mix(c["p"], "#ffffff", 0.2), mix(c["p"], "#000000", 0.35)))
            for _ in range(3):
                self.circle(x + self.rnd.random() * w, y + self.rnd.random() * h,
                            min(w, h) * (0.2 + self.rnd.random() * 0.35), "#ffffff",
                            f'opacity="{0.08 + self.rnd.random() * 0.12:.2f}"')
        self.add("</g>")

    def section_head(self, y, center=True, x=None):
        c = self.c
        if center:
            self.rect(W / 2 - 40, y, 80, 8, c["p"], r=4)
            self.rect(W / 2 - 160, y + 22, 320, 18, c["heading"], r=6, extra='opacity="0.85"')
            self.lines(W / 2 - 180, y + 54, 360, 2, center=True)
        else:
            x = PAD if x is None else x
            self.rect(x, y, 80, 8, c["p"], r=4)
            self.rect(x, y + 22, 260, 18, c["heading"], r=6, extra='opacity="0.85"')
            self.rect(x, y + 46, 190, 18, c["heading"], r=6, extra='opacity="0.85"')
        return y + 100

    def card(self, x, y, w, h, r=12):
        c = self.c
        self.rect(x, y, w, h, c["card"], r=r, extra=f'stroke="{c["border"]}"')

    # page chrome ------------------------------------------------------------ #
    def nav(self, transparent=False, on_dark=False):
        c = self.c
        y = self.y
        if not transparent:
            self.rect(0, y, W, 68, c["bg"])
            self.rect(0, y + 67, W, 1, c["border"])
        txt = "#ffffff" if on_dark else c["heading"]
        self.rect(PAD, y + 24, 22, 22, c["p"], r=6)
        self.text(PAD + 30, y + 41, self.name, 18, txt, 800)
        lx = W - PAD - 132 - 4 * 62
        for i in range(4):
            self.rect(lx + i * 62, y + 31, 44, 7, txt, r=3, extra='opacity="0.55"')
        self.button(W - PAD - 112, y + 16, 112, 36)
        self.y += 68

    def footer(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 250, c["footer"])
        self.rect(PAD, y + 54, 20, 20, c["p"], r=5)
        self.text(PAD + 28, y + 70, self.name, 16, "#ffffff", 800)
        self.lines(PAD, y + 92, 190, 3, "#2a3352", h=7, gap=14)
        for i in range(3):
            fx = PAD + 300 + i * 130
            self.rect(fx, y + 56, 60, 9, "#ffffff", r=4, extra='opacity="0.85"')
            for j in range(4):
                self.rect(fx, y + 84 + j * 20, 70 - (j % 2) * 18, 7, "#2a3352", r=3)
        self.rect(PAD, y + 196, CW, 1, "#1d2440")
        self.rect(PAD, y + 216, 180, 7, "#2a3352", r=3)
        for i in range(4):
            self.circle(W - PAD - 10 - i * 30, y + 220, 10, "#1d2440")
        self.y += 250

    # heroes ----------------------------------------------------------------- #
    def hero(self, kind, headline):
        getattr(self, f"hero_{kind}")(headline)

    def _badge(self, x, y, center=False):
        c = self.c
        w = 170
        if center:
            x = W / 2 - w / 2
        self.rect(x, y, w, 28, c["soft"], r=14)
        self.circle(x + 16, y + 14, 5, c["p"])
        self.rect(x + 30, y + 10, w - 46, 8, c["p"], r=4, extra='opacity="0.7"')

    def hero_split(self, headline):
        c = self.c
        self.nav()
        y = self.y
        self.rect(0, y, W, 470, c["bg"])
        self.circle(W - 80, y + 60, 160, c["soft"], 'opacity="0.6"')
        self._badge(PAD, y + 70)
        for i, line in enumerate(headline):
            self.text(PAD, y + 146 + i * 44, line, 38, c["heading"], 800, spacing=-1.2)
        self.lines(PAD, y + 146 + len(headline) * 44 - 10, 290, 3)
        by = y + 146 + len(headline) * 44 + 50
        self.button(PAD, by, 132, 46)
        self.button(PAD + 146, by, 120, 46, filled=False)
        for i in range(3):
            self.circle(PAD + 14 + i * 22, by + 84, 14, mix(c["p"], "#ffffff", 0.3 + i * 0.2), f'stroke="{c["bg"]}" stroke-width="3"')
        self.lines(PAD + 84, by + 76, 110, 2, h=7, gap=14)
        self.image(424, y + 56, 312, 360, r=20, kind=self.rnd.choice(["person", "landscape"]))
        sh = self.shadow()
        self.rect(384, y + 330, 170, 64, c["card"], r=12, extra=sh)
        self.circle(410, y + 362, 14, c["soft"])
        self.circle(410, y + 362, 6, c["p"])
        self.lines(434, y + 352, 100, 2, h=7, gap=14)
        self.y += 470

    def hero_center(self, headline):
        c = self.c
        self.nav()
        y = self.y
        self.rect(0, y, W, 640, self.grad(c["bg"], c["soft"], vertical=True))
        self._badge(0, y + 64, center=True)
        for i, line in enumerate(headline):
            self.text(W / 2, y + 144 + i * 46, line, 40, c["heading"], 800, anchor="middle", spacing=-1.4)
        ty = y + 144 + len(headline) * 46 - 12
        self.lines(W / 2 - 200, ty, 400, 2, center=True)
        self.button(W / 2 - 136, ty + 50, 128, 46)
        self.button(W / 2 + 8, ty + 50, 128, 46, filled=False)
        sh = self.shadow()
        self.rect(PAD + 20, ty + 136, CW - 40, 330, c["card"], r=14, extra=sh)
        self.image(PAD + 30, ty + 146, CW - 60, 310, r=10, kind="dashboard")
        self.y += 640

    def hero_full(self, headline):
        c = self.c
        y = self.y
        self.image(0, y, W, 560, r=0, kind=self.rnd.choice(["landscape", "abstract"]))
        self.rect(0, y, W, 560, self.grad("#0b1020", "#0b102000"), extra='opacity="0.75"')
        self.nav(transparent=True, on_dark=True)
        self.rect(PAD, y + 150, 120, 8, "#ffffff", r=4, extra='opacity="0.7"')
        for i, line in enumerate(headline):
            self.text(PAD, y + 214 + i * 50, line, 44, "#ffffff", 800, spacing=-1.4)
        ty = y + 214 + len(headline) * 50 - 14
        self.lines(PAD, ty, 330, 2, "#ffffff55")
        self.button(PAD, ty + 50, 140, 48)
        self.button(PAD + 154, ty + 50, 128, 48, filled=True, color="#ffffff22")
        self.y = y + 560
        # stats strip
        self.rect(0, self.y, W, 110, c["p"])
        for i in range(4):
            sx = PAD + i * (CW / 4)
            self.rect(sx, self.y + 34, 70, 20, "#ffffff", r=5)
            self.rect(sx, self.y + 66, 100, 7, "#ffffff", r=3, extra='opacity="0.6"')
        self.y += 110

    def hero_app(self, headline):
        c = self.c
        self.nav()
        y = self.y
        self.rect(0, y, W, 520, self.grad(c["soft"], c["bg"]))
        self._badge(PAD, y + 80)
        for i, line in enumerate(headline):
            self.text(PAD, y + 156 + i * 44, line, 38, c["heading"], 800, spacing=-1.2)
        ty = y + 156 + len(headline) * 44 - 10
        self.lines(PAD, ty, 300, 3)
        for i in range(2):
            self.rect(PAD + i * 146, ty + 70, 134, 46, "#0b1020", r=10)
            self.circle(PAD + i * 146 + 24, ty + 93, 9, "#ffffff")
            self.rect(PAD + i * 146 + 42, ty + 82, 70, 7, "#ffffff", r=3, extra='opacity="0.6"')
            self.rect(PAD + i * 146 + 42, ty + 96, 80, 10, "#ffffff", r=4)
        sh = self.shadow()
        for k, (px, py, s) in enumerate([(530, y + 40, 1.0), (440, y + 110, 0.82)][::-1]):
            pw, ph = 200 * s, 410 * s
            self.rect(px, py, pw, ph, "#0b1020", r=30 * s, extra=sh)
            self.image(px + 9 * s, py + 9 * s, pw - 18 * s, ph - 18 * s, r=22 * s, kind="abstract")
            self.rect(px + pw / 2 - 30 * s, py + 16 * s, 60 * s, 12 * s, "#0b1020", r=6 * s)
            for j in range(3):
                self.rect(px + 22 * s, py + (200 + j * 52) * s, pw - 44 * s, 40 * s, "#ffffff", r=10 * s, extra='opacity="0.9"')
                self.circle(px + 40 * s, py + (220 + j * 52) * s, 9 * s, c["p"])
                self.rect(px + 58 * s, py + (215 + j * 52) * s, 80 * s, 8 * s, c["muted"], r=4 * s)
        self.y += 520

    def hero_portfolio(self, headline):
        c = self.c
        self.nav()
        y = self.y
        self.rect(0, y, W, 520, c["bg"])
        self.circle(W - 210, y + 250, 170, c["soft"])
        self.image(W - 360, y + 90, 300, 330, r=150, kind="person")
        self.rect(PAD, y + 110, 150, 10, c["p"], r=5)
        for i, line in enumerate(headline):
            self.text(PAD, y + 190 + i * 56, line, 52, c["heading"], 800, spacing=-2)
        ty = y + 190 + len(headline) * 56 - 18
        self.lines(PAD, ty, 280, 3)
        self.button(PAD, ty + 70, 140, 48)
        for i in range(4):
            self.circle(PAD + 180 + i * 40, ty + 94, 14, c["surface"])
        self.y += 520

    def hero_shop(self, headline):
        c = self.c
        self.rect(0, 0, W, 34, c["heading"])
        self.rect(W / 2 - 120, 13, 240, 8, c["bg"], r=4, extra='opacity="0.5"')
        self.y = 34
        self.nav()
        y = self.y
        self.rect(PAD - 30, y + 24, CW + 60, 420, self.grad(mix(c["p"], "#ffffff", 0.88), mix(c["p"], "#ffffff", 0.7)), r=22)
        self.text(PAD + 20, y + 120, "NEW SEASON", 14, c["p"], 800, spacing=2)
        for i, line in enumerate(headline):
            self.text(PAD + 20, y + 170 + i * 48, line, 42, "#111827", 800, spacing=-1.4)
        ty = y + 170 + len(headline) * 48 - 12
        self.lines(PAD + 20, ty, 260, 2, mix(c["p"], "#ffffff", 0.45))
        self.button(PAD + 20, ty + 46, 140, 46, color="#111827")
        self.image(W - PAD - 280, y + 54, 260, 360, r=130, kind="person")
        self.rect(W - PAD - 320, y + 330, 104, 104, c["p"], r=52)
        self.text(W - PAD - 268, y + 382, "-40%", 22, "#ffffff", 800, anchor="middle")
        self.text(W - PAD - 268, y + 404, "OFF", 12, "#ffffff", 700, anchor="middle", spacing=1)
        self.y += 470
        # categories
        cw = (CW - 3 * 16) / 4
        for i in range(4):
            cx = PAD + i * (cw + 16)
            self.rect(cx, self.y + 10, cw, 90, c["surface"], r=14)
            self.circle(cx + 40, self.y + 55, 24, c["soft"])
            self.lines(cx + 76, self.y + 46, cw - 96, 2, h=7, gap=14)
        self.y += 120

    # sections --------------------------------------------------------------- #
    def logos(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 120, c["bg"])
        self.rect(W / 2 - 110, y + 30, 220, 7, c["muted"], r=3)
        lw = (CW - 4 * 30) / 5
        for i in range(5):
            lx = PAD + i * (lw + 30)
            self.circle(lx + 12, y + 77, 10, c["muted"])
            self.rect(lx + 28, y + 71, lw - 30, 12, c["muted"], r=6)
        self.y += 120

    def features3(self, alt=False):
        c = self.c
        y = self.y
        self.rect(0, y, W, 380, c["surface"] if not alt else c["bg"])
        y2 = self.section_head(y + 60)
        fw = (CW - 2 * 20) / 3
        for i in range(3):
            fx = PAD + i * (fw + 20)
            self.card(fx, y2, fw, 190)
            self.rect(fx + 24, y2 + 26, 46, 46, c["p"] if i == 1 else c["soft"], r=12)
            self.rect(fx + 38, y2 + 40, 18, 18, "#ffffff" if i == 1 else c["p"], r=5)
            self.rect(fx + 24, y2 + 94, fw * 0.55, 12, c["heading"], r=5, extra='opacity="0.85"')
            self.lines(fx + 24, y2 + 122, fw - 48, 3, h=7, gap=14)
        self.y += 380

    def split(self, flip=False):
        c = self.c
        y = self.y
        self.rect(0, y, W, 440, c["bg"])
        ix = PAD if not flip else W / 2 + 10
        tx = W / 2 + 24 if not flip else PAD
        self.image(ix, y + 70, CW / 2 - 10, 300, r=18)
        self.section_head(y + 90, center=False, x=tx)
        ly = self.lines(tx, y + 180, CW / 2 - 40, 3)
        for i in range(3):
            self.circle(tx + 10, ly + 22 + i * 30, 10, c["soft"])
            self.circle(tx + 10, ly + 22 + i * 30, 4, c["p"])
            self.rect(tx + 30, ly + 18 + i * 30, 160 + (i % 2) * 40, 8, c["heading"], r=4, extra='opacity="0.6"')
        self.button(tx, ly + 112)
        self.y += 440

    def stats(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 200, c["bg"])
        self.rect(PAD - 20, y + 30, CW + 40, 140, self.grad(c["p"], c["p2"]), r=20)
        for i in range(4):
            sx = PAD + 20 + i * ((CW - 40) / 4)
            self.rect(sx, y + 72, 84, 24, "#ffffff", r=6)
            self.rect(sx, y + 110, 110, 8, "#ffffff", r=4, extra='opacity="0.6"')
        self.y += 200

    def testimonials(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 400, c["surface"])
        y2 = self.section_head(y + 60)
        tw = (CW - 20) / 2
        for i in range(2):
            tx = PAD + i * (tw + 20)
            self.card(tx, y2, tw, 200)
            for s in range(5):
                self.add(self._star(tx + 30 + s * 20, y2 + 34, 7, "#f5b301"))
            self.lines(tx + 24, y2 + 60, tw - 48, 4, h=7, gap=15)
            self.circle(tx + 46, y2 + 156, 20, mix(c["p"], "#ffffff", 0.3 + i * 0.25))
            self.rect(tx + 76, y2 + 144, 100, 9, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(tx + 76, y2 + 162, 70, 7, c["muted"], r=3)
        self.y += 400

    @staticmethod
    def _star(cx, cy, r, fill):
        import math
        pts = []
        for k in range(10):
            rr = r if k % 2 == 0 else r * 0.45
            a = math.pi / 2 + k * math.pi / 5
            pts.append(f"{cx + rr * math.cos(a):.1f},{cy - rr * math.sin(a):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'

    def blog(self, head=True):
        c = self.c
        y = self.y
        h = 420 if head else 330
        self.rect(0, y, W, h, c["bg"])
        y2 = self.section_head(y + 60) if head else y + 40
        bw = (CW - 40) / 3
        for i in range(3):
            bx = PAD + i * (bw + 20)
            self.image(bx, y2, bw, 130, r=12)
            self.rect(bx, y2 + 148, 60, 7, c["p"], r=3)
            self.rect(bx, y2 + 166, bw * 0.9, 11, c["heading"], r=5, extra='opacity="0.85"')
            self.rect(bx, y2 + 184, bw * 0.6, 11, c["heading"], r=5, extra='opacity="0.85"')
            self.lines(bx, y2 + 210, bw, 2, h=7, gap=14)
        self.y += h

    def cta(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 260, c["bg"])
        self.rect(PAD - 20, y + 40, CW + 40, 180, self.grad(mix(c["p"], "#000000", 0.2), c["p"]), r=22)
        self.circle(W - PAD - 40, y + 60, 90, "#ffffff", 'opacity="0.08"')
        self.circle(PAD + 40, y + 220, 70, "#ffffff", 'opacity="0.06"')
        self.rect(W / 2 - 170, y + 92, 340, 20, "#ffffff", r=7)
        self.rect(W / 2 - 130, y + 124, 260, 8, "#ffffff", r=4, extra='opacity="0.6"')
        self.button(W / 2 - 66, y + 152, 132, 44, color="#ffffff")
        self.rect(W / 2 - 44, y + 170, 88, 8, c["p"], r=4)
        self.y += 260

    def gallery(self, head=True, filters=False):
        c = self.c
        y = self.y
        h = 600 if head else 500
        self.rect(0, y, W, h, c["bg"])
        y2 = self.section_head(y + 60) if head else y + 40
        if filters:
            for i in range(5):
                fx = W / 2 - 230 + i * 94
                self.rect(fx, y2 - 6, 82, 30, c["p"] if i == 0 else c["surface"], r=15)
            y2 += 44
        gw = (CW - 32) / 3
        for i in range(6):
            gx = PAD + (i % 3) * (gw + 16)
            gy = y2 + (i // 3) * 206
            self.image(gx, gy, gw, 190, r=14)
        self.y += h + (44 if filters else 0)

    def team(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 420, c["surface"])
        y2 = self.section_head(y + 60)
        tw = (CW - 3 * 16) / 4
        for i in range(4):
            tx = PAD + i * (tw + 16)
            self.image(tx, y2, tw, 170, r=14, kind="person")
            self.rect(tx + tw * 0.15, y2 + 186, tw * 0.7, 11, c["heading"], r=5, extra='opacity="0.85"')
            self.rect(tx + tw * 0.3, y2 + 206, tw * 0.4, 7, c["p"], r=3)
        self.y += 420

    def pricing(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 560, c["bg"])
        y2 = self.section_head(y + 60)
        pw = (CW - 40) / 3
        for i in range(3):
            px = PAD + i * (pw + 20)
            hi = i == 1
            py = y2 - (16 if hi else 0)
            ph = 380 + (32 if hi else 0)
            if hi:
                self.rect(px, py, pw, ph, self.grad(c["p"], c["p2"]), r=16)
            else:
                self.card(px, py, pw, ph, r=16)
            tc = "#ffffff" if hi else c["heading"]
            mc = "#ffffff88" if hi else c["muted"]
            self.rect(px + 24, py + 30, 70, 9, tc, r=4, extra='opacity="0.7"')
            self.rect(px + 24, py + 56, 90, 28, tc, r=6)
            for j in range(6):
                self.circle(px + 30, py + 122 + j * 30, 6, "#ffffff" if hi else c["p"], 'opacity="0.85"')
                self.rect(px + 46, py + 118 + j * 30, pw * 0.55 - (j % 3) * 10, 8, mc, r=4)
            if hi:
                self.button(px + 24, py + ph - 68, pw - 48, 44, color="#ffffff")
                self.rect(px + pw / 2 - 34, py + ph - 50, 68, 8, c["p"], r=4)
            else:
                self.button(px + 24, py + ph - 68, pw - 48, 44, filled=False)
        self.y += 560

    def faq(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 470, c["surface"])
        y2 = self.section_head(y + 60)
        for i in range(5):
            fy = y2 + i * 62
            self.card(PAD + 60, fy, CW - 120, 50, r=10)
            self.rect(PAD + 84, fy + 21, 240 + (i % 3) * 50, 9, c["heading"], r=4, extra='opacity="0.75"')
            self.circle(W - PAD - 88, fy + 25, 11, c["p"] if i == 0 else c["soft"])
        self.y += 470

    def products(self, head=True):
        c = self.c
        y = self.y
        h = 640 if head else 560
        self.rect(0, y, W, h, c["bg"])
        y2 = self.section_head(y + 50) if head else y + 30
        pw = (CW - 3 * 16) / 4
        for i in range(8):
            px = PAD + (i % 4) * (pw + 16)
            py = y2 + (i // 4) * 250
            self.rect(px, py, pw, 170, c["surface"], r=12)
            self.image(px + 20, py + 20, pw - 40, 130, r=60 if i % 2 else 10,
                       kind="person" if i % 3 == 0 else "abstract")
            if i in (0, 5):
                self.rect(px + 10, py + 10, 42, 20, c["p"], r=10)
            self.rect(px, py + 184, pw * 0.8, 10, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(px, py + 204, pw * 0.35, 12, c["p"], r=4)
            for s in range(5):
                self.add(self._star(px + pw - 56 + s * 11, py + 210, 4, "#f5b301"))
        self.y += h

    def page_header(self, title):
        c = self.c
        self.nav()
        y = self.y
        self.rect(0, y, W, 230, self.grad(mix(c["p"], "#000000", 0.25), c["p"]))
        self.circle(W - 80, y + 40, 120, "#ffffff", 'opacity="0.07"')
        self.circle(90, y + 220, 90, "#ffffff", 'opacity="0.06"')
        self.text(W / 2, y + 120, title, 38, "#ffffff", 800, anchor="middle", spacing=-1)
        self.rect(W / 2 - 70, y + 150, 140, 26, "#ffffff22", r=13)
        self.rect(W / 2 - 50, y + 159, 100, 8, "#ffffff", r=4, extra='opacity="0.7"')
        self.y += 230

    def article(self):
        c = self.c
        y = self.y
        mw = CW * 0.66
        self.rect(0, y, W, 900, c["bg"])
        self.image(PAD, y + 50, mw, 280, r=14)
        ty = y + 360
        self.rect(PAD, ty, 80, 8, c["p"], r=4)
        self.rect(PAD, ty + 22, mw * 0.85, 18, c["heading"], r=6, extra='opacity="0.85"')
        ty = self.lines(PAD, ty + 62, mw, 6)
        self.rect(PAD, ty + 16, 4, 70, c["p"])
        self.lines(PAD + 20, ty + 26, mw - 20, 3, c["heading"] + "88", h=9, gap=18)
        ty = self.lines(PAD, ty + 110, mw, 7)
        self.image(PAD, ty + 16, mw / 2 - 8, 140, r=12)
        self.image(PAD + mw / 2 + 8, ty + 16, mw / 2 - 8, 140, r=12)
        self.lines(PAD, ty + 180, mw, 4)
        sx = PAD + mw + 30
        sw = CW - mw - 30
        self.card(sx, y + 50, sw, 52, r=10)
        self.rect(sx + 16, y + 72, sw * 0.5, 8, c["muted"], r=4)
        for k, hgt in enumerate([200, 220, 160]):
            by = y + 126 + sum([200, 220, 160][:k]) + k * 22
            self.card(sx, by, sw, hgt, r=12)
            self.rect(sx + 18, by + 22, sw * 0.5, 11, c["heading"], r=5, extra='opacity="0.85"')
            for j in range((hgt - 60) // 30):
                self.rect(sx + 18, by + 56 + j * 30, sw - 36 - (j % 2) * 30, 8, c["muted"], r=4)
        self.y += 900

    def bigimage(self):
        y = self.y
        self.rect(0, y, W, 420, self.c["bg"])
        self.image(PAD, y + 50, CW, 330, r=18, kind="landscape")
        self.y += 420

    def form(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 600, c["bg"])
        cw = (CW - 3 * 16) / 3
        for i in range(3):
            cx = PAD + i * (cw + 16)
            self.card(cx, y + 50, cw, 110)
            self.circle(cx + 36, y + 90, 18, c["soft"])
            self.circle(cx + 36, y + 90, 7, c["p"])
            self.lines(cx + 64, y + 80, cw - 84, 2, h=8, gap=16)
        fw = CW * 0.56
        self.card(PAD, y + 190, fw, 360, r=16)
        self.rect(PAD + 26, y + 220, 160, 14, c["heading"], r=5, extra='opacity="0.85"')
        for r in range(2):
            for k in range(2):
                self.rect(PAD + 26 + k * (fw / 2 - 16), y + 256 + r * 56, fw / 2 - 36, 40, c["surface"], r=8)
        self.rect(PAD + 26, y + 368, fw - 52, 110, c["surface"], r=8)
        self.button(PAD + 26, y + 494, 150, 40)
        mx = PAD + fw + 20
        self.rect(mx, y + 190, CW - fw - 20, 360, mix(c["p"], "#ffffff", 0.88), r=16)
        for k in range(6):
            self.rect(mx, y + 230 + k * 55, CW - fw - 20, 3, "#ffffff")
            self.rect(mx + 20 + k * 40, y + 190, 3, 360, "#ffffff")
        self.circle(mx + (CW - fw - 20) / 2, y + 350, 14, c["p"])
        self.circle(mx + (CW - fw - 20) / 2, y + 350, 5, "#ffffff")
        self.y += 600

    def cart(self):
        c = self.c
        y = self.y
        self.rect(0, y, W, 520, c["bg"])
        tw = CW * 0.64
        self.rect(PAD, y + 50, tw, 44, c["surface"], r=8)
        for i in range(3):
            ry = y + 110 + i * 100
            self.image(PAD + 12, ry, 76, 76, r=10, kind="abstract")
            self.rect(PAD + 106, ry + 20, 140, 10, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(PAD + 106, ry + 42, 70, 8, c["muted"], r=4)
            self.rect(PAD + tw - 170, ry + 22, 84, 32, c["surface"], r=8)
            self.rect(PAD + tw - 60, ry + 32, 50, 11, c["p"], r=4)
            self.rect(PAD, ry + 90, tw, 1, c["border"])
        sx = PAD + tw + 24
        sw = CW - tw - 24
        self.card(sx, y + 50, sw, 300, r=14)
        self.rect(sx + 20, y + 74, 100, 12, c["heading"], r=5, extra='opacity="0.85"')
        for j in range(4):
            self.rect(sx + 20, y + 112 + j * 34, 70, 8, c["muted"], r=4)
            self.rect(sx + sw - 70, y + 112 + j * 34, 50, 8, c["heading"], r=4, extra='opacity="0.6"')
        self.button(sx + 20, y + 280, sw - 40, 44)
        self.y += 520

    # full-screen specials ------------------------------------------------- #
    def special_login(self):
        c = self.c
        self.rect(0, 0, W, 1100, c["surface"])
        self.image(0, 0, W / 2, 1100, r=0, kind="abstract")
        self.text(60, 100, self.name, 22, "#ffffff", 800)
        self.text(60, 820, "Welcome back.", 40, "#ffffff", 800, spacing=-1)
        self.lines(60, 850, 260, 2, "#ffffff66")
        fx = W / 2 + 60
        fw = W / 2 - 120
        self.rect(fx, 260, 180, 22, c["heading"], r=6, extra='opacity="0.85"')
        self.lines(fx, 300, fw, 1)
        for k in range(2):
            self.rect(fx, 350 + k * 90, 80, 8, c["heading"], r=4, extra='opacity="0.6"')
            self.rect(fx, 368 + k * 90, fw, 46, c["bg"], r=10, extra=f'stroke="{c["border"]}"')
        self.button(fx, 560, fw, 48)
        self.rect(fx, 640, fw, 1, c["border"])
        for k in range(2):
            self.rect(fx + k * (fw / 2 + 8), 670, fw / 2 - 8, 46, c["bg"], r=10, extra=f'stroke="{c["border"]}"')
        self.y = 1100

    def special_404(self):
        c = self.c
        self.nav()
        self.rect(0, 68, W, 1000, c["bg"])
        self.circle(W / 2, 420, 260, c["soft"])
        self.text(W / 2, 470, "404", 190, c["p"], 900, anchor="middle", spacing=-8)
        self.rect(W / 2 - 150, 560, 300, 20, c["heading"], r=7, extra='opacity="0.85"')
        self.lines(W / 2 - 180, 600, 360, 2, center=True)
        self.button(W / 2 - 70, 660, 140, 46)
        self.y = 820
        self.footer()

    def special_coming(self):
        c = self.c
        self.image(0, 0, W, 1100, r=0, kind="abstract")
        self.text(W / 2, 140, self.name, 26, "#ffffff", 800, anchor="middle")
        self.text(W / 2, 420, "Launching Soon", 56, "#ffffff", 800, anchor="middle", spacing=-2)
        self.lines(W / 2 - 200, 456, 400, 2, "#ffffff66", center=True)
        for i, n in enumerate(["24", "08", "36", "12"]):
            bx = W / 2 - 230 + i * 120
            self.rect(bx, 540, 100, 110, "#ffffff1f", r=16)
            self.text(bx + 50, 606, n, 40, "#ffffff", 800, anchor="middle")
            self.rect(bx + 26, 622, 48, 7, "#ffffff", r=3, extra='opacity="0.6"')
        self.rect(W / 2 - 200, 720, 400, 54, "#ffffff", r=27)
        self.rect(W / 2 + 60, 726, 134, 42, mix(c["p"], "#000000", 0.2), r=21)
        self.y = 1100

    # output ----------------------------------------------------------------- #
    def svg(self) -> str:
        h = int(self.y)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">'
            f'<defs>{"".join(self.defs)}</defs><rect width="{W}" height="{h}" fill="{self.c["bg"]}"/>'
            f'{"".join(self.parts)}</svg>\n'
        )


# --------------------------------------------------------------------------- #
# Definitions
# --------------------------------------------------------------------------- #
BRAND = "#5b5bf7"

DEMOS = [
    # file,          name,         colour,   dark,  hero,        headline,                         sections
    ("01-corporate", "Corpix",   "#2563eb", False, "split",     ["Grow your", "business faster"], ["logos", "features3", "split", "stats", "testimonials", "blog", "cta"]),
    ("02-agency",    "Studio",   "#ff5a36", True,  "full",      ["We craft bold", "digital brands"], ["gallery", "split:flip", "team", "testimonials", "cta"]),
    ("03-saas",      "Flowly",   "#6d5dfc", False, "center",    ["Analytics that", "work for you"], ["logos", "features3", "split", "pricing", "testimonials", "faq", "cta"]),
    ("04-marketing", "Rankly",   "#10b981", False, "split",     ["Marketing that", "drives results"], ["features3", "stats", "split:flip", "pricing", "blog", "cta"]),
    ("05-portfolio", "Alex.",    "#f59e0b", True,  "portfolio", ["Hi, I'm Alex", "Designer."], ["gallery", "split", "testimonials", "cta"]),
    ("06-app",       "Appify",   "#ec4899", False, "app",       ["Your life,", "in one app"], ["logos", "features3", "split", "stats", "pricing", "faq", "cta"]),
    ("07-consulting", "Advisa",  "#0f766e", False, "full",      ["Strategy for", "lasting growth"], ["features3:alt", "split", "team", "blog", "cta"]),
    ("08-fintech",   "Payora",   "#0ea5e9", True,  "center",    ["Banking built", "for the future"], ["logos", "features3", "split:flip", "stats", "pricing", "cta"]),
    ("09-startup",   "Launchr",  "#8b5cf6", False, "center",    ["Launch your", "idea today"], ["features3", "split", "split:flip", "testimonials", "faq", "cta"]),
    ("10-shop",      "Vestra",   "#ef4444", False, "shop",      ["Summer", "Collection"], ["products", "split:flip", "testimonials", "cta"]),
    ("11-architecture", "Forma", "#c2410c", True,  "full",      ["Spaces that", "inspire living"], ["gallery", "split:flip", "team", "blog", "cta"]),
    ("12-medical",   "Medica",   "#06b6d4", False, "split",     ["Care that puts", "you first"], ["features3", "split", "team", "testimonials", "form", "cta"]),
]

PAGES = [
    ("about",           "About Us",       ["split", "stats", "team", "testimonials", "cta"]),
    ("services",        "Services",       ["features3", "features3:alt", "split", "cta"]),
    ("service-details", "Service Details", ["article", "faq", "cta"]),
    ("pricing",         "Pricing",        ["pricing", "faq", "cta"]),
    ("team",            "Our Team",       ["team", "team", "cta"]),
    ("portfolio",       "Portfolio",      ["gallery:filters", "cta"]),
    ("project-details", "Project Details", ["bigimage", "split", "gallery:nohead", "cta"]),
    ("blog",            "Blog",           ["blog:nohead", "blog:nohead", "cta"]),
    ("blog-single",     "Blog Details",   ["article", "blog"]),
    ("shop",            "Shop",           ["products:nohead", "products:nohead"]),
    ("cart",            "Cart",           ["cart", "products"]),
    ("contact",         "Contact Us",     ["form", "cta"]),
    ("faq",             "FAQ",            ["faq", "faq", "cta"]),
    ("login",           None,             ["special_login"]),
    ("404",             None,             ["special_404"]),
    ("coming-soon",     None,             ["special_coming"]),
]


def run_sections(cv: Canvas, sections):
    for s in sections:
        name, _, opt = s.partition(":")
        fn = getattr(cv, name)
        if name == "split":
            fn(flip=opt == "flip")
        elif name == "features3":
            fn(alt=opt == "alt")
        elif name == "gallery":
            fn(head=opt != "nohead", filters=opt == "filters")
        elif name in ("blog", "products"):
            fn(head=opt != "nohead")
        else:
            fn()


def main():
    demo_dir = os.path.join(ROOT, "assets", "img", "demos")
    page_dir = os.path.join(ROOT, "assets", "img", "pages")
    os.makedirs(demo_dir, exist_ok=True)
    os.makedirs(page_dir, exist_ok=True)

    for i, (fname, name, color, dark, hero, headline, sections) in enumerate(DEMOS):
        cv = Canvas(color, dark, name, seed=i + 7)
        cv.hero(hero, headline)
        run_sections(cv, sections)
        cv.footer()
        with open(os.path.join(demo_dir, f"{fname}.svg"), "w") as fh:
            fh.write(cv.svg())

    for i, (fname, title, sections) in enumerate(PAGES):
        cv = Canvas(BRAND, False, "Nexora", seed=100 + i)
        if title:
            cv.page_header(title)
            run_sections(cv, sections)
            cv.footer()
        else:
            run_sections(cv, sections)
        with open(os.path.join(page_dir, f"{fname}.svg"), "w") as fh:
            fh.write(cv.svg())

    print(f"Generated {len(DEMOS)} demo and {len(PAGES)} page thumbnails.")


if __name__ == "__main__":
    main()
