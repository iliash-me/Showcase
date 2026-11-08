"""
Placeholder "screenshots" of web-application screens: admin dashboards,
app pages, SaaS panels, POS terminals and WordPress admin screens.

Used by generate_thumbnails.py — run that script, not this one.
"""
from __future__ import annotations

import math

from generate_thumbnails import Canvas, mix, W as SITE_W

AW = 1200  # app screenshots are rendered wider than website ones

GREEN, AMBER, RED, BLUE = "#12b981", "#f59e0b", "#ef4444", "#3b82f6"


class AppCanvas(Canvas):
    """Canvas with an application shell (sidebar / top bar) and dashboard widgets."""

    def __init__(self, primary, dark, name, seed, sidebar="light"):
        super().__init__(primary, dark, name, seed)
        self.width = AW
        self.sidebar = sidebar  # light | dark | horizontal | wp | none
        self.bgfill = "#0b1020" if dark else "#f3f5fa"
        self._sidebar_slot = None
        self.x0 = 40
        self.cw = AW - 80

    # ------------------------------------------------------------------ shell
    def shell(self, title, active=1, crumbs=True):
        c = self.c
        sb = self.sidebar
        dark = c["dark"]
        self.y = 0
        if sb in ("light", "dark", "wp"):
            top = 32 if sb == "wp" else 0
            sw = 170 if sb == "wp" else 236
            if sb == "wp":
                sfill, stext = "#1d2327", "#c3c4c7"
            elif sb == "dark":
                sfill, stext = ("#101528" if not dark else "#0f1428"), "#aab2cf"
            else:
                sfill, stext = c["card"], c["subtle"]
            self._sidebar_slot = (len(self.parts), sw, sfill, top)
            self.add("")  # replaced in svg()
            if sb == "wp":
                self.rect(0, 0, AW, 32, "#1d2327")
                self.circle(18, 16, 9, "#c3c4c7")
                for i in range(4):
                    self.rect(40 + i * 70, 12, 50, 8, "#c3c4c7", r=4, extra='opacity="0.55"')
                self.circle(AW - 24, 16, 9, "#c3c4c7")
            else:
                self.rect(22, 22, 28, 28, c["p"], r=8)
                self.text(60, 43, self.name, 18, "#ffffff" if sb == "dark" else c["heading"], 800)
            iy = top + (24 if sb == "wp" else 92)
            gap = 36 if sb == "wp" else 40
            for i in range(14 if sb == "wp" else 11):
                if sb != "wp" and i in (0, 6):
                    self.rect(26, iy - 4, 60, 6, stext, r=3, extra='opacity="0.5"')
                    iy += 26
                if i == active:
                    afill = "#2271b1" if sb == "wp" else (c["p"] if sb == "dark" else c["soft"])
                    self.rect(0 if sb == "wp" else 14, iy - 13, sw if sb == "wp" else sw - 28, 34, afill, r=0 if sb == "wp" else 9)
                    col = "#ffffff" if sb in ("wp", "dark") else c["p"]
                else:
                    col = stext
                self.rect(28, iy - 4, 16, 16, col, r=4, extra='opacity="0.85"')
                self.rect(54, iy, 70 + (i * 23) % 50, 8, col, r=4, extra='opacity="0.85"')
                iy += gap
            # top bar
            self.rect(sw, top, AW - sw, 64, c["card"])
            self.rect(sw, top + 63, AW - sw, 1, c["border"])
            self.rect(sw + 28, top + 16, 280, 32, c["surface"], r=16)
            self.circle(sw + 48, top + 32, 6, c["muted"])
            self.rect(sw + 62, top + 28, 120, 8, c["muted"], r=4)
            for i in range(3):
                self.circle(AW - 200 + i * 40, top + 32, 15, c["surface"])
            self.circle(AW - 200 + 40 * 2 + 14, top + 22, 4, RED)
            self.circle(AW - 64, top + 32, 17, mix(c["p"], "#ffffff", 0.4))
            self.rect(AW - 40, top + 28, 18, 8, c["muted"], r=4)
            self.x0 = sw + 28
            self.cw = AW - sw - 56
            self.y = top + 64 + 28
        elif sb == "horizontal":
            self.rect(0, 0, AW, 64, c["card"])
            self.rect(40, 18, 28, 28, c["p"], r=8)
            self.text(78, 39, self.name, 18, c["heading"], 800)
            self.rect(260, 16, 300, 32, c["surface"], r=16)
            for i in range(3):
                self.circle(AW - 200 + i * 40, 32, 15, c["surface"])
            self.circle(AW - 64, 32, 17, mix(c["p"], "#ffffff", 0.4))
            self.rect(0, 64, AW, 52, c["card"])
            self.rect(0, 64, AW, 1, c["border"])
            self.rect(0, 115, AW, 1, c["border"])
            for i in range(8):
                nx = 40 + i * 132
                if i == active:
                    self.rect(nx - 10, 76, 124, 28, c["soft"], r=8)
                col = c["p"] if i == active else c["subtle"]
                self.rect(nx, 84, 12, 12, col, r=3)
                self.rect(nx + 20, 86, 70, 8, col, r=4, extra='opacity="0.8"')
            self.x0, self.cw = 40, AW - 80
            self.y = 116 + 28
        else:  # none: slim top bar only
            self.rect(0, 0, AW, 60, c["card"])
            self.rect(0, 59, AW, 1, c["border"])
            self.rect(24, 16, 28, 28, c["p"], r=8)
            self.text(62, 37, self.name, 18, c["heading"], 800)
            for i in range(4):
                self.rect(260 + i * 110, 18, 96, 24, c["soft"] if i == 0 else c["surface"], r=12)
            self.circle(AW - 48, 30, 16, mix(c["p"], "#ffffff", 0.4))
            self.rect(AW - 190, 18, 120, 24, c["surface"], r=12)
            self.x0, self.cw = 24, AW - 48
            self.y = 60 + 20
        if title:
            self.text(self.x0, self.y + 24, title, 22, c["heading"], 800, spacing=-0.5)
            if crumbs:
                self.rect(self.x0 + self.cw - 170, self.y + 10, 170, 10, c["muted"], r=5)
            self.y += 52

    def svg(self):
        self.y += 28
        if self._sidebar_slot:
            idx, sw, fill, top = self._sidebar_slot
            border = "" if self.sidebar == "wp" else f'<rect x="{sw - 1}" y="0" width="1" height="{int(self.y)}" fill="{self.c["border"]}"/>'
            self.parts[idx] = f'<rect x="0" y="{top}" width="{sw}" height="{int(self.y) - top}" fill="{fill}"/>' + border
        return super().svg()

    # ---------------------------------------------------------------- helpers
    def label(self, x, y, s, size=12, color=None, weight=600, anchor="start"):
        self.text(x, y, s, size, color or self.c["subtle"], weight, anchor=anchor, spacing=0)

    def card_title(self, x, y, w, title, action=True):
        self.text(x + 20, y + 32, title, 15, self.c["heading"], 700, spacing=-0.2)
        if action:
            self.rect(x + w - 92, y + 16, 72, 26, self.c["surface"], r=8)
            self.rect(x + w - 76, y + 26, 40, 6, self.c["muted"], r=3)

    def pill(self, x, y, text, color, w=None):
        w = w or (len(text) * 7 + 18)
        self.rect(x, y, w, 22, mix(color, self.c["card"], 0.84), r=11)
        self.text(x + w / 2, y + 15, text, 11, color, 700, anchor="middle", spacing=0)
        return w

    def spark(self, x, y, w, h, color, n=10):
        pts = []
        v = 0.5
        for i in range(n):
            v = min(0.95, max(0.05, v + (self.rnd.random() - 0.42) * 0.35))
            pts.append(f"{x + i * w / (n - 1):.1f},{y + h - v * h:.1f}")
        self.add(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')

    def series(self, n, lo=0.2, hi=0.9):
        v = (lo + hi) / 2
        out = []
        for _ in range(n):
            v = min(hi, max(lo, v + (self.rnd.random() - 0.45) * 0.25))
            out.append(v)
        return out

    def checkbox(self, x, y, on, size=18):
        c = self.c
        if on:
            self.rect(x, y, size, size, c["p"], r=5)
            self.add(f'<path d="M{x + size * 0.25:.1f} {y + size * 0.52:.1f} l{size * 0.17:.1f} {size * 0.17:.1f} l{size * 0.33:.1f} -{size * 0.36:.1f}" '
                     f'fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            self.rect(x + 1, y + 1, size - 2, size - 2, "none", r=5, extra=f'stroke="{c["muted"]}" stroke-width="2"')

    def toggle(self, x, y, on):
        c = self.c
        self.rect(x, y, 40, 22, c["p"] if on else c["muted"], r=11)
        self.circle(x + (29 if on else 11), y + 11, 8, "#ffffff")

    def avatar(self, cx, cy, r, i=0):
        cols = [self.c["p"], AMBER, GREEN, "#ec4899", BLUE, "#8b5cf6"]
        self.circle(cx, cy, r, mix(cols[i % len(cols)], "#ffffff", 0.35))
        self.circle(cx, cy - r * 0.18, r * 0.36, "#ffffff", 'opacity="0.75"')

    # ---------------------------------------------------------------- widgets
    def kpis(self, items, y=None, h=120):
        c = self.c
        y = self.y if y is None else y
        n = len(items)
        gap = 20
        kw = (self.cw - gap * (n - 1)) / n
        for i, (label, val, delta, up) in enumerate(items):
            kx = self.x0 + i * (kw + gap)
            self.card(kx, y, kw, h)
            self.label(kx + 20, y + 32, label)
            self.text(kx + 20, y + 70, val, 26, c["heading"], 800, spacing=-0.8)
            col = GREEN if up else RED
            self.pill(kx + 20, y + 84, ("▲ " if up else "▼ ") + delta, col)
            self.rect(kx + kw - 58, y + 18, 40, 40, c["p"] if i == 0 else c["soft"], r=11)
            self.rect(kx + kw - 46, y + 30, 16, 16, "#ffffff" if i == 0 else c["p"], r=4)
            self.spark(kx + kw - 112, y + 76, 92, 26, col)
        self.y = y + h + 24

    def chart(self, x, y, w, h, kind, title):
        c = self.c
        self.card(x, y, w, h)
        self.card_title(x, y, w, title)
        ix, iy, iw, ih = x + 24, y + 62, w - 48, h - 90
        if kind in ("area", "line2", "bar"):
            for k in range(5):
                gy = iy + k * ih / 4
                self.rect(ix, gy, iw, 1, c["border"])
        if kind in ("area", "line2"):
            n = 14
            for si, (col, fill) in enumerate([(c["p"], True), (AMBER, False)][: 2 if kind == "line2" else 1]):
                vals = self.series(n, 0.15 if si else 0.3, 0.7 if si else 0.95)
                pts = [(ix + i * iw / (n - 1), iy + ih - v * ih) for i, v in enumerate(vals)]
                ps = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
                if fill:
                    g = self.grad(c["p"] + "55", c["p"] + "00", vertical=True)
                    self.add(f'<polygon points="{ix:.1f},{iy + ih:.1f} {ps} {ix + iw:.1f},{iy + ih:.1f}" fill="{g}"/>')
                dash = 'stroke-dasharray="7 6"' if si else ""
                self.add(f'<polyline points="{ps}" fill="none" stroke="{col}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" {dash}/>')
            px, py = pts[-4] if kind == "area" else (ix + iw * 0.7, iy + ih * 0.3)
        elif kind == "bar":
            n = 12
            bw = iw / n
            for i in range(n):
                v1, v2 = 0.3 + self.rnd.random() * 0.65, 0.2 + self.rnd.random() * 0.5
                self.rect(ix + i * bw + bw * 0.18, iy + ih - v1 * ih, bw * 0.28, v1 * ih, c["p"], r=3)
                self.rect(ix + i * bw + bw * 0.52, iy + ih - v2 * ih, bw * 0.28, v2 * ih, mix(c["p"], c["card"], 0.65), r=3)
        elif kind in ("donut", "radial"):
            cx, cy = x + w / 2, iy + min(ih * 0.42, 110)
            r = min(iw, ih) * 0.28
            C = 2 * math.pi * r
            if kind == "donut":
                segs = [(0.42, c["p"]), (0.26, mix(c["p"], "#ffffff", 0.45)), (0.18, AMBER), (0.14, GREEN)]
                off = 0
                for frac, col in segs:
                    L = frac * C
                    self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{col}" stroke-width="{r * 0.42:.1f}" '
                             f'stroke-dasharray="{L - 3:.1f} {C - L + 3:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 {cx:.1f} {cy:.1f})"/>')
                    off += L
                self.text(cx, cy + 4, "8,240", 18, c["heading"], 800, anchor="middle")
                self.label(cx, cy + 22, "Total", 11, anchor="middle")
                ly = cy + r + 40
                for k, (frac, col) in enumerate(segs):
                    lx = x + 28 + (k % 2) * (w / 2 - 14)
                    yy = ly + (k // 2) * 30
                    self.circle(lx + 5, yy - 4, 5, col)
                    self.rect(lx + 18, yy - 8, 60, 8, c["muted"], r=4)
                    self.text(lx + w / 2 - 50, yy, f"{int(frac * 100)}%", 12, c["heading"], 700, anchor="end", spacing=0)
            else:
                self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{c["surface"]}" stroke-width="{r * 0.28:.1f}"/>')
                L = 0.72 * C
                self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{c["p"]}" stroke-width="{r * 0.28:.1f}" stroke-linecap="round" '
                         f'stroke-dasharray="{L:.1f} {C:.1f}" transform="rotate(-90 {cx:.1f} {cy:.1f})"/>')
                self.text(cx, cy + 8, "72%", 24, c["heading"], 800, anchor="middle")
                self.label(cx, cy + r + 44, "of monthly target reached", 12, anchor="middle")
                self.button(cx - 70, cy + r + 62, 140, 36)
        elif kind == "hbar":
            rows = int(ih // 44)
            for k in range(rows):
                yy = iy + k * 44
                self.rect(ix, yy, 80, 8, c["muted"], r=4)
                v = 0.9 - k * 0.12
                self.rect(ix, yy + 16, iw, 8, c["surface"], r=4)
                self.rect(ix, yy + 16, iw * v, 8, c["p"], r=4, extra=f'opacity="{1 - k * 0.12:.2f}"')
        elif kind == "map":
            self.rect(ix, iy, iw, ih, c["surface"], r=10)
            for k in range(1, 6):
                self.rect(ix, iy + k * ih / 6, iw, 1.5, c["border"])
                self.rect(ix + k * iw / 6, iy, 1.5, ih, c["border"])
            pts = [(0.15, 0.7), (0.35, 0.45), (0.55, 0.55), (0.8, 0.25)]
            path = " ".join(f"{'M' if i == 0 else 'L'}{ix + px * iw:.1f} {iy + py * ih:.1f}" for i, (px, py) in enumerate(pts))
            self.add(f'<path d="{path}" fill="none" stroke="{c["p"]}" stroke-width="3" stroke-dasharray="8 6"/>')
            for px, py in pts:
                self.circle(ix + px * iw, iy + py * ih, 8, c["p"])
                self.circle(ix + px * iw, iy + py * ih, 3, "#ffffff")

    def table(self, x, y, w, title, rows=5, cols=("Name", "Date", "Amount", "Status"), avatar=True, thumb=False,
              status=("Paid", "Pending", "Paid", "Failed", "Paid", "Active", "Pending", "Paid"), progress=False, check=False):
        c = self.c
        rh = 56
        h = 62 + 40 + rows * rh + 10
        self.card(x, y, w, h)
        if title:
            self.card_title(x, y, w, title)
            ty = y + 62
        else:
            ty = y + 12
            h -= 50
        self.rect(x + 1, ty, w - 2, 40, c["surface"])
        first = w * 0.34
        rest = (w - first - 40) / (len(cols) - 1)
        colx = [x + 20] + [x + 20 + first + i * rest for i in range(len(cols) - 1)]
        for i, name in enumerate(cols):
            self.label(colx[i] + (30 if check and i == 0 else 0), ty + 25, name.upper(), 11, weight=700)
        for r in range(rows):
            ry = ty + 40 + r * rh
            cx = colx[0]
            if check:
                self.checkbox(cx, ry + 19, r == 1)
                cx += 30
            if thumb:
                self.image(cx, ry + 10, 36, 36, r=8, kind="abstract")
            elif avatar:
                self.avatar(cx + 17, ry + 28, 17, r)
            nx = cx + (48 if (thumb or avatar) else 0)
            self.rect(nx, ry + 18, 90 + (r * 37) % 60, 9, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(nx, ry + 34, 60 + (r * 23) % 40, 7, c["muted"], r=3)
            for i in range(1, len(cols)):
                cx = colx[i]
                last = i == len(cols) - 1
                if last and status:
                    s = status[r % len(status)]
                    col = {"Paid": GREEN, "Active": GREEN, "Delivered": GREEN, "In Stock": GREEN, "Completed": GREEN,
                           "Pending": AMBER, "Low Stock": AMBER, "Shipped": BLUE, "Draft": c["subtle"],
                           "Failed": RED, "Out of Stock": RED, "Cancelled": RED}.get(s, c["p"])
                    self.pill(cx, ry + 17, s, col)
                elif progress and i == len(cols) - 2:
                    v = 0.25 + ((r * 0.23) % 0.7)
                    self.rect(cx, ry + 25, rest - 30, 7, c["surface"], r=4)
                    self.rect(cx, ry + 25, (rest - 30) * v, 7, c["p"], r=4)
                else:
                    self.rect(cx, ry + 24, rest * (0.35 + ((r + i) * 0.13) % 0.35), 8, c["muted"], r=4)
            if r < rows - 1:
                self.rect(x + 20, ry + rh, w - 40, 1, c["border"])
        return h

    def list_card(self, x, y, w, h, title, thumb=False, values=None):
        c = self.c
        self.card(x, y, w, h)
        self.card_title(x, y, w, title)
        rows = int((h - 70) // 56)
        values = values or ["$2,480", "$1,920", "$1,350", "$980", "$740", "$610", "$420"]
        for r in range(rows):
            ry = y + 66 + r * 56
            if thumb:
                self.image(x + 20, ry, 40, 40, r=10, kind="abstract")
            else:
                self.avatar(x + 40, ry + 20, 20, r + 2)
            self.rect(x + 72, ry + 8, 100 + (r * 31) % 50, 9, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(x + 72, ry + 25, 70, 7, c["muted"], r=3)
            self.text(x + w - 20, ry + 25, values[r % len(values)], 13, c["heading"], 700, anchor="end", spacing=0)

    def grid2(self, ratio=0.64):
        """Return (x1, w1, x2, w2) for a two-column row."""
        w1 = (self.cw - 24) * ratio
        return self.x0, w1, self.x0 + w1 + 24, self.cw - w1 - 24

    # ------------------------------------------------------------ app screens
    def calendar(self, x, y, w, h):
        c = self.c
        self.card(x, y, w, h)
        narrow = w < 600
        self.text(x + 24 if not narrow else x + 20, y + 38, "November 2026", 15 if narrow else 18, c["heading"], 800, spacing=-0.3)
        for i in range(1 if narrow else 3):
            self.rect(x + w - (64 if narrow else 260) + i * 80, y + 18, 44 if narrow else 72, 30, c["p"] if i == 0 else c["surface"], r=8)
        gx, gy, gw, gh = x + 20, y + 70, w - 40, h - 90
        cw_, rh = gw / 7, (gh - 30) / 5
        for d, name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            self.label(gx + d * cw_ + 10, gy + 18, name, 11, weight=700)
        cols = [c["p"], GREEN, AMBER, "#ec4899", BLUE]
        for r in range(5):
            for d in range(7):
                cx, cy = gx + d * cw_, gy + 30 + r * rh
                self.rect(cx, cy, cw_, rh, "none", extra=f'stroke="{c["border"]}"')
                day = r * 7 + d - 1
                if 0 < day <= 30:
                    self.text(cx + 10, cy + 20, str(day), 12, c["heading"] if day != 8 else "#ffffff", 600, spacing=0)
                    if day == 8:
                        self.circle(cx + 17, cy + 16, 11, c["p"])
                        self.text(cx + 17, cy + 20, "8", 12, "#ffffff", 700, anchor="middle", spacing=0)
                    if self.rnd.random() < 0.32:
                        col = self.rnd.choice(cols)
                        span = 1 if d == 6 else self.rnd.choice([1, 1, 2])
                        self.rect(cx + 6, cy + 32, cw_ * span - 12, 22, mix(col, c["card"], 0.8), r=5)
                        self.rect(cx + 6, cy + 32, 3, 22, col)
                        self.rect(cx + 16, cy + 40, cw_ * span * 0.5, 6, col, r=3)

    def kanban(self, x, y, w, h):
        c = self.c
        names = ["To Do", "In Progress", "Review", "Done"]
        colw = (w - 3 * 20) / 4
        tags = [(c["p"], "Design"), (GREEN, "Dev"), (AMBER, "Bug"), ("#ec4899", "UX"), (BLUE, "API")]
        for k in range(4):
            cx = x + k * (colw + 20)
            self.rect(cx, y, colw, h, c["surface"] if not c["dark"] else "#121831", r=14)
            self.text(cx + 18, y + 32, names[k], 14, c["heading"], 700, spacing=0)
            self.pill(cx + colw - 48, y + 16, str(3 + k % 2), c["p"], w=30)
            cy = y + 52
            for j in range(4 - (k % 2)):
                ch = 110 + (j * 37 + k * 19) % 60
                if cy + ch > y + h - 14:
                    break
                self.card(cx + 12, cy, colw - 24, ch, r=10)
                col, t = tags[(j + k) % len(tags)]
                self.pill(cx + 26, cy + 14, t, col)
                self.rect(cx + 26, cy + 48, (colw - 52) * 0.85, 9, c["heading"], r=4, extra='opacity="0.8"')
                self.rect(cx + 26, cy + 64, (colw - 52) * 0.6, 7, c["muted"], r=3)
                for a in range(2 + j % 2):
                    self.avatar(cx + 38 + a * 18, cy + ch - 22, 11, a + j)
                self.rect(cx + colw - 76, cy + ch - 26, 40, 8, c["muted"], r=4)
                cy += ch + 12

    def chat(self, x, y, w, h, ai=False):
        c = self.c
        self.card(x, y, w, h, r=14)
        lw = 300
        self.rect(x + lw, y, 1, h, c["border"])
        self.rect(x + 20, y + 20, lw - 40, 38, c["surface"], r=10)
        if ai:
            self.button(x + 20, y + 20, lw - 40, 38)
        for r in range(int((h - 90) // 64)):
            ry = y + 76 + r * 64
            if r == 0:
                self.rect(x + 10, ry - 6, lw - 20, 58, c["soft"], r=10)
            if ai:
                self.rect(x + 24, ry + 8, 28, 28, c["surface"] if r else c["card"], r=8)
                self.rect(x + 34, ry + 18, 8, 8, c["p"], r=2)
            else:
                self.avatar(x + 42, ry + 22, 20, r)
                if r % 3 == 0:
                    self.circle(x + 56, ry + 36, 5, GREEN, f'stroke="{c["card"]}" stroke-width="2"')
            self.rect(x + 74, ry + 10, 110 + (r * 29) % 50, 9, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(x + 74, ry + 27, 150, 7, c["muted"], r=3)
            if not ai:
                self.rect(x + lw - 56, ry + 10, 32, 7, c["muted"], r=3)
        mx = x + lw
        mw = w - lw
        self.rect(mx, y + 70, mw, 1, c["border"])
        if ai:
            self.rect(mx + 24, y + 22, 30, 30, self.grad(c["p"], "#ec4899"), r=9)
            self.text(mx + 66, y + 43, "AI Assistant", 15, c["heading"], 700, spacing=0)
        else:
            self.avatar(mx + 42, y + 36, 19, 0)
            self.rect(mx + 72, y + 26, 120, 9, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(mx + 72, y + 42, 60, 7, GREEN, r=3)
        for i in range(3):
            self.circle(x + w - 40 - i * 40, y + 36, 15, c["surface"])
        by = y + 96
        msgs = [(False, 2, 0.55), (True, 1, 0.4), (False, 3, 0.65), (True, 2, 0.5), (False, 2, 0.45)]
        for k, (mine, lines, frac) in enumerate(msgs):
            bw = mw * frac
            bh = 26 + lines * 16
            code = ai and k == 2
            if code:
                bh += 110
            if by + bh > y + h - 90:
                break
            bx = mx + mw - bw - 28 if mine else mx + 72
            if not mine:
                if ai:
                    self.rect(mx + 26, by, 30, 30, self.grad(c["p"], "#ec4899"), r=9)
                else:
                    self.avatar(mx + 44, by + 16, 16, 0)
            self.rect(bx, by, bw, bh, c["p"] if mine else c["surface"], r=14)
            for li in range(lines):
                self.rect(bx + 16, by + 16 + li * 16, (bw - 32) * (0.6 if li == lines - 1 and lines > 1 else 1), 7,
                          "#ffffff" if mine else c["muted"], r=3, extra='opacity="0.85"' if mine else "")
            if code:
                cy = by + 16 + lines * 16 + 6
                self.rect(bx + 14, cy, bw - 28, 96, "#0f1426", r=10)
                palette = ["#c084fc", "#7dd3fc", "#fbbf24", "#86efac"]
                for li in range(5):
                    self.rect(bx + 30 + (li % 2) * 20, cy + 16 + li * 15, 60 + (li * 47) % 140, 6, palette[li % 4], r=3)
            by += bh + 18
        self.rect(mx + 24, y + h - 70, mw - 48, 48, c["surface"], r=12)
        self.rect(mx + 44, y + h - 50, 200, 8, c["muted"], r=4)
        self.rect(x + w - 76, y + h - 64, 36, 36, c["p"], r=10)
        self.add(f'<path d="M{x + w - 66} {y + h - 46} l16 -6 -6 16 -2 -8z" fill="#fff"/>')

    def email(self, x, y, w, h):
        c = self.c
        self.card(x, y, w, h, r=14)
        lw = 230
        self.rect(x + lw, y, 1, h, c["border"])
        self.button(x + 20, y + 20, lw - 40, 42)
        for r in range(8):
            ry = y + 90 + r * 40
            if r == 0:
                self.rect(x + 10, ry - 12, lw - 20, 36, c["soft"], r=8)
            col = c["p"] if r == 0 else c["subtle"]
            self.rect(x + 26, ry, 14, 14, col, r=4, extra='opacity="0.8"')
            self.rect(x + 52, ry + 3, 80 + (r * 17) % 40, 8, col, r=4, extra='opacity="0.8"')
            if r in (0, 2):
                self.pill(x + lw - 58, ry - 4, str(12 if r == 0 else 3), c["p"] if r == 0 else AMBER, w=34)
        self.label(x + 26, y + 440, "LABELS", 11, weight=700)
        for k, col in enumerate([GREEN, AMBER, "#ec4899", BLUE]):
            self.circle(x + 32, y + 470 + k * 32, 5, col)
            self.rect(x + 50, y + 466 + k * 32, 70, 8, c["subtle"], r=4, extra='opacity="0.6"')
        mx, mw = x + lw, w - lw
        self.checkbox(mx + 24, y + 26, False)
        for i in range(4):
            self.circle(mx + 76 + i * 36, y + 35, 12, c["surface"])
        self.rect(x + w - 300, y + 20, 276, 32, c["surface"], r=16)
        self.rect(mx, y + 70, mw, 1, c["border"])
        rows = int((h - 80) // 54)
        for r in range(rows):
            ry = y + 71 + r * 54
            unread = r in (0, 1, 4)
            if unread:
                self.rect(mx + 1, ry, mw - 2, 53, mix(c["p"], c["card"], 0.95))
            self.checkbox(mx + 24, ry + 18, r == 3)
            self.add(self._star(mx + 66, ry + 27, 7, AMBER if r in (1, 5) else c["muted"]))
            self.avatar(mx + 100, ry + 27, 15, r)
            self.rect(mx + 126, ry + 22, 110, 9, c["heading"], r=4, extra=f'opacity="{0.9 if unread else 0.5}"')
            sx = mx + 270
            if r in (0, 3, 6):
                sx += self.pill(sx, ry + 16, ["Work", "Team", "Social"][r // 3 % 3], [GREEN, BLUE, "#ec4899"][r // 3 % 3]) + 10
            self.rect(sx, ry + 22, mw - (sx - mx) - 110, 9, c["heading"] if unread else c["muted"], r=4,
                      extra='opacity="0.55"' if unread else "")
            self.rect(x + w - 70, ry + 22, 46, 8, c["muted"], r=4)
            self.rect(mx + 1, ry + 53, mw - 2, 1, c["border"])

    def files(self, x, y, w):
        c = self.c
        fw = (w - 3 * 20) / 4
        cols = [c["p"], AMBER, GREEN, "#ec4899"]
        for i in range(4):
            fx = x + i * (fw + 20)
            self.card(fx, y, fw, 150)
            col = cols[i]
            self.add(f'<path d="M{fx + 22} {y + 30} h22 l6 7 h22 a4 4 0 0 1 4 4 v28 a4 4 0 0 1 -4 4 h-50 a4 4 0 0 1 -4 -4 v-35 a4 4 0 0 1 4 -4z" fill="{col}"/>')
            self.rect(fx + 22, y + 92, fw * 0.5, 10, c["heading"], r=4, extra='opacity="0.85"')
            self.rect(fx + 22, y + 112, fw - 44, 6, c["surface"], r=3)
            self.rect(fx + 22, y + 112, (fw - 44) * (0.3 + i * 0.15), 6, col, r=3)
            self.label(fx + 22, y + 138, f"{12 + i * 9} files", 11)
        return 170

    def invoice(self, x, y, w, h):
        c = self.c
        dw = w * 0.72
        self.card(x, y, dw, h, r=14)
        self.rect(x + 40, y + 40, 32, 32, c["p"], r=9)
        self.text(x + 82, y + 64, self.name, 20, c["heading"], 800)
        self.text(x + dw - 40, y + 60, "INVOICE", 26, c["p"], 800, anchor="end", spacing=1)
        self.label(x + dw - 40, y + 82, "#INV-2026-0042", 12, anchor="end")
        for k in range(2):
            bx = x + 40 + k * (dw / 2 - 20)
            self.label(bx, y + 130, "BILLED TO" if k else "FROM", 11, weight=700)
            self.rect(bx, y + 146, 140, 10, c["heading"], r=4, extra='opacity="0.8"')
            self.lines(bx, y + 166, 180, 3, h=7, gap=14)
        ty = y + 240
        self.rect(x + 40, ty, dw - 80, 40, c["soft"], r=8)
        for i, name in enumerate(["ITEM", "QTY", "RATE", "AMOUNT"]):
            self.label(x + 60 + (0 if i == 0 else (dw - 120) * (0.45 + i * 0.17)), ty + 25, name, 11, c["p"], 700)
        for r in range(4):
            ry = ty + 56 + r * 48
            self.rect(x + 60, ry, 170 - (r * 23) % 60, 9, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(x + 60, ry + 16, 110, 7, c["muted"], r=3)
            for i in range(1, 4):
                self.rect(x + 60 + (dw - 120) * (0.45 + i * 0.17), ry + 2, 40, 8, c["muted"], r=4)
            self.rect(x + 40, ry + 34, dw - 80, 1, c["border"])
        sy = ty + 56 + 4 * 48 + 10
        for k, (lab, val) in enumerate([("Subtotal", "$4,250.00"), ("Tax (10%)", "$425.00"), ("Total", "$4,675.00")]):
            big = k == 2
            self.label(x + dw - 260, sy + k * 32 + 14, lab, 13 if not big else 15, c["heading"] if big else None, 700 if big else 600)
            self.text(x + dw - 40, sy + k * 32 + 14, val, 15 if big else 13, c["p"] if big else c["heading"], 800 if big else 600, anchor="end", spacing=0)
        self.rect(x + 40, y + h - 90, dw - 80, 1, c["border"])
        self.lines(x + 40, y + h - 66, dw * 0.6, 2, h=7, gap=14)
        ax = x + dw + 24
        aw = w - dw - 24
        self.card(ax, y, aw, 260, r=14)
        self.button(ax + 20, y + 24, aw - 40, 44)
        for k in range(3):
            self.button(ax + 20, y + 84 + k * 56, aw - 40, 44, filled=False)
        self.card(ax, y + 280, aw, 160, r=14)
        self.label(ax + 20, y + 312, "Payment status", 12)
        self.pill(ax + 20, y + 326, "Paid", GREEN, w=60)
        self.lines(ax + 20, y + 370, aw - 40, 3, h=7, gap=16)

    def profile(self, x, y, w):
        c = self.c
        self.card(x, y, w, 300, r=14)
        self.image(x + 1, y + 1, w - 2, 170, r=14, kind="landscape")
        self.circle(x + 90, y + 180, 54, c["card"])
        self.avatar(x + 90, y + 180, 48, 0)
        self.text(x + 160, y + 212, "Sophia Carter", 22, c["heading"], 800)
        self.label(x + 160, y + 234, "Product Designer · San Francisco", 13)
        self.button(x + w - 160, y + 190, 136, 40)
        for i, t in enumerate(["Overview", "Projects", "Team", "Activity"]):
            col = c["p"] if i == 0 else c["subtle"]
            self.text(x + 40 + i * 120, y + 284, t, 13, col, 700, spacing=0)
            if i == 0:
                self.rect(x + 40, y + 296, 66, 3, c["p"], r=2)
        y2 = y + 324
        x1, w1, x2, w2 = x, w * 0.36, x + w * 0.36 + 24, w - w * 0.36 - 24
        self.card(x1, y2, w1, 400, r=14)
        self.card_title(x1, y2, w1, "About", action=False)
        self.lines(x1 + 20, y2 + 56, w1 - 40, 4, h=7, gap=15)
        for k in range(5):
            self.rect(x1 + 20, y2 + 140 + k * 40, 16, 16, c["soft"], r=4)
            self.rect(x1 + 46, y2 + 144 + k * 40, 120 + (k * 27) % 60, 8, c["muted"], r=4)
        self.card(x2, y2, w2, 400, r=14)
        self.card_title(x2, y2, w2, "Recent Activity")
        for k in range(5):
            ky = y2 + 70 + k * 64
            self.circle(x2 + 32, ky + 10, 8, [c["p"], GREEN, AMBER, "#ec4899", BLUE][k])
            if k < 4:
                self.rect(x2 + 31, ky + 22, 2, 46, c["border"])
            self.rect(x2 + 56, ky + 4, 220 + (k * 41) % 90, 9, c["heading"], r=4, extra='opacity="0.8"')
            self.rect(x2 + 56, ky + 22, 160, 7, c["muted"], r=3)
            self.rect(x2 + w2 - 90, ky + 4, 66, 7, c["muted"], r=3)
        return 724

    def form(self, x, y, w, h, title, gateways=None, tabs=("General", "Appearance", "Payments", "Email", "API Keys", "Advanced")):
        c = self.c
        tw = 220
        self.card(x, y, tw, h, r=14)
        for i, t in enumerate(tabs):
            ty = y + 20 + i * 46
            if i == (2 if gateways else 0):
                self.rect(x + 12, ty, tw - 24, 38, c["soft"], r=9)
            col = c["p"] if i == (2 if gateways else 0) else c["subtle"]
            self.rect(x + 28, ty + 12, 14, 14, col, r=4)
            self.text(x + 54, ty + 24, t, 13, col, 600, spacing=0)
        fx, fw = x + tw + 24, w - tw - 24
        self.card(fx, y, fw, h, r=14)
        self.text(fx + 28, y + 42, title, 17, c["heading"], 800, spacing=-0.2)
        self.label(fx + 28, y + 64, "Manage your configuration and preferences", 12)
        self.rect(fx + 28, y + 84, fw - 56, 1, c["border"])
        yy = y + 108
        if gateways:
            for k, (gname, gcol, on) in enumerate(gateways):
                self.rect(fx + 28, yy, fw - 56, 64, c["card"], r=12, extra=f'stroke="{c["border"]}"')
                self.rect(fx + 44, yy + 14, 84, 36, gcol, r=8)
                self.text(fx + 86, yy + 37, gname, 12, "#ffffff", 800, anchor="middle", spacing=0)
                self.rect(fx + 148, yy + 20, 120, 9, c["heading"], r=4, extra='opacity="0.8"')
                self.rect(fx + 148, yy + 36, 180, 7, c["muted"], r=3)
                self.button(fx + fw - 200, yy + 15, 96, 34, filled=False)
                self.toggle(fx + fw - 88, yy + 21, on)
                yy += 78
        else:
            half = (fw - 56 - 20) / 2
            for r in range(3):
                for k in range(2):
                    ix = fx + 28 + k * (half + 20)
                    self.rect(ix, yy, 90, 8, c["heading"], r=4, extra='opacity="0.65"')
                    self.rect(ix, yy + 18, half, 42, c["surface"], r=9, extra=f'stroke="{c["border"]}"')
                    self.rect(ix + 14, yy + 35, half * 0.4, 8, c["muted"], r=4)
                yy += 84
            self.rect(fx + 28, yy, 110, 8, c["heading"], r=4, extra='opacity="0.65"')
            self.rect(fx + 28, yy + 18, fw - 56, 96, c["surface"], r=9, extra=f'stroke="{c["border"]}"')
            yy += 140
            for k in range(3):
                self.toggle(fx + 28, yy, k != 1)
                self.rect(fx + 82, yy + 4, 180 + k * 30, 8, c["heading"], r=4, extra='opacity="0.65"')
                self.rect(fx + 82, yy + 18, 240, 6, c["muted"], r=3)
                yy += 46
        self.button(fx + 28, y + h - 68, 140, 42)
        self.button(fx + 182, y + h - 68, 110, 42, filled=False)

    def plans(self, x, y, w):
        c = self.c
        pw = (w - 40) / 3
        for i, (name, price) in enumerate([("Starter", "$9"), ("Pro", "$29"), ("Business", "$79")]):
            px = x + i * (pw + 20)
            hi = i == 1
            self.card(px, y, pw, 400, r=14)
            if hi:
                self.rect(px, y, pw, 400, "none", r=14, extra=f'stroke="{c["p"]}" stroke-width="2"')
                self.pill(px + pw - 100, y + 20, "Popular", c["p"], w=78)
            self.text(px + 24, y + 44, name, 16, c["heading"], 700, spacing=0)
            self.text(px + 24, y + 96, price, 38, c["heading"], 800, spacing=-1)
            self.label(px + 24 + len(price) * 22 + 6, y + 96, "/month", 13)
            for k in range(6):
                self.circle(px + 32, y + 134 + k * 34, 8, c["soft"])
                self.add(f'<path d="M{px + 28} {y + 134 + k * 34} l3 3 5 -6" fill="none" stroke="{c["p"]}" stroke-width="2" stroke-linecap="round"/>')
                self.rect(px + 50, y + 130 + k * 34, pw * 0.5 - (k % 3) * 12, 8, c["muted"], r=4)
            self.button(px + 24, y + 340, pw - 48, 40, filled=hi)
            self.toggle(px + pw - 64, y + 30 + 0, True) if not hi else None
        return 420

    # AI screens
    def writer(self, x, y, w, h):
        c = self.c
        lw = 360
        self.card(x, y, lw, h, r=14)
        self.text(x + 24, y + 40, "Blog Post Writer", 17, c["heading"], 800, spacing=-0.2)
        self.label(x + 24, y + 62, "Generate SEO-friendly articles", 12)
        yy = y + 90
        for lab, tall in [("Template", False), ("Topic / Keywords", True), ("Tone of voice", False), ("Language", False)]:
            self.label(x + 24, yy, lab, 12, c["heading"], 700)
            hh = 96 if tall else 42
            self.rect(x + 24, yy + 10, lw - 48, hh, c["surface"], r=9, extra=f'stroke="{c["border"]}"')
            self.rect(x + 38, yy + 27, (lw - 76) * (0.7 if tall else 0.45), 8, c["muted"], r=4)
            if tall:
                self.rect(x + 38, yy + 43, (lw - 76) * 0.5, 8, c["muted"], r=4)
            yy += hh + 34
        self.label(x + 24, yy, "Creativity", 12, c["heading"], 700)
        self.rect(x + 24, yy + 18, lw - 48, 6, c["surface"], r=3)
        self.rect(x + 24, yy + 18, (lw - 48) * 0.65, 6, c["p"], r=3)
        self.circle(x + 24 + (lw - 48) * 0.65, yy + 21, 9, "#ffffff", f'stroke="{c["p"]}" stroke-width="3"')
        self.rect(x + 24, y + h - 72, lw - 48, 48, self.grad(c["p"], "#ec4899"), r=11)
        self.text(x + lw / 2, y + h - 43, "✦ Generate Content", 14, "#ffffff", 700, anchor="middle", spacing=0)
        dx, dw = x + lw + 24, w - lw - 24
        self.card(dx, y, dw, h, r=14)
        for i in range(9):
            self.rect(dx + 24 + i * 34, y + 20, 24, 24, c["surface"], r=6)
        self.button(dx + dw - 240, y + 14, 100, 36, filled=False)
        self.button(dx + dw - 128, y + 14, 104, 36)
        self.rect(dx, y + 64, dw, 1, c["border"])
        self.text(dx + 40, y + 120, "10 Proven Ways to Boost", 26, c["heading"], 800, spacing=-0.8)
        self.text(dx + 40, y + 154, "Remote Team Productivity", 26, c["heading"], 800, spacing=-0.8)
        yy = self.lines(dx + 40, y + 184, dw - 80, 5, gap=18)
        self.rect(dx + 40, yy + 16, 220, 14, c["heading"], r=5, extra='opacity="0.8"')
        yy = self.lines(dx + 40, yy + 48, dw - 80, 4, gap=18)
        self.rect(dx + 36, yy + 10, dw * 0.55, 46, mix(c["p"], c["card"], 0.85), r=6)
        self.lines(dx + 44, yy + 22, dw * 0.5, 2, c["p"] + "99", gap=16)
        self.rect(dx + 36 + dw * 0.55, yy + 10, 2, 46, c["p"])
        yy = self.lines(dx + 40, yy + 76, dw - 80, 3, gap=18)
        self.rect(dx, y + h - 50, dw, 1, c["border"])
        self.label(dx + 24, y + h - 20, "1,284 words  ·  6 min read", 12)
        self.pill(dx + dw - 120, y + h - 36, "SEO 92/100", GREEN, w=96)

    def image_gen(self, x, y, w, h):
        c = self.c
        self.card(x, y, w, 150, r=14)
        self.rect(x + 24, y + 24, w - 220, 52, c["surface"], r=12, extra=f'stroke="{c["border"]}"')
        self.label(x + 44, y + 55, "A futuristic city skyline at sunset, cinematic lighting, ultra detailed", 13)
        self.rect(x + w - 180, y + 24, 156, 52, self.grad(c["p"], "#ec4899"), r=12)
        self.text(x + w - 102, y + 55, "✦ Generate", 14, "#ffffff", 700, anchor="middle", spacing=0)
        for i, t in enumerate(["Photorealistic", "Digital Art", "3D Render", "Anime", "Watercolor", "Cinematic"]):
            self.rect(x + 24 + i * 128, y + 98, 116, 30, c["soft"] if i == 0 else c["surface"], r=15)
            self.text(x + 82 + i * 128, y + 118, t, 12, c["p"] if i == 0 else c["subtle"], 600, anchor="middle", spacing=0)
        gy = y + 174
        gw = (w - 3 * 18) / 4
        for i in range(8):
            gx = x + (i % 4) * (gw + 18)
            yy = gy + (i // 4) * (gw + 18)
            if yy + gw > y + h:
                break
            self.image(gx, yy, gw, gw, r=14, kind=["landscape", "abstract", "abstract", "landscape"][i % 4])
            if i == 1:
                self.rect(gx, yy, gw, gw, "#0b1020aa", r=14)
                self.text(gx + gw / 2, yy + gw / 2 - 6, "Generating… 64%", 14, "#ffffff", 700, anchor="middle", spacing=0)
                self.rect(gx + 30, yy + gw / 2 + 10, gw - 60, 6, "#ffffff33", r=3)
                self.rect(gx + 30, yy + gw / 2 + 10, (gw - 60) * 0.64, 6, "#ffffff", r=3)
            elif i in (0, 4):
                for b in range(2):
                    self.rect(gx + gw - 44 - b * 40, yy + 12, 32, 32, "#ffffffdd", r=9)
                    self.rect(gx + gw - 34 - b * 40, yy + 22, 12, 12, c["p"], r=3)

    def templates(self, x, y, w):
        c = self.c
        for i, t in enumerate(["All", "Blog", "Marketing", "Social Media", "Email", "Website", "SEO"]):
            tw = len(t) * 8 + 32
            px = x + sum(len(s) * 8 + 42 for s in ["All", "Blog", "Marketing", "Social Media", "Email", "Website", "SEO"][:i])
            self.rect(px, y, tw, 34, c["p"] if i == 0 else c["card"], r=17, extra="" if i == 0 else f'stroke="{c["border"]}"')
            self.text(px + tw / 2, y + 22, t, 12, "#ffffff" if i == 0 else c["subtle"], 600, anchor="middle", spacing=0)
        cw_ = (w - 3 * 20) / 4
        cols = [c["p"], "#ec4899", AMBER, GREEN, BLUE, "#8b5cf6"]
        names = ["Blog Post", "Product Description", "Facebook Ads", "Instagram Caption", "Email Newsletter",
                 "SEO Meta Tags", "Landing Page Copy", "YouTube Script", "Cold Email", "Press Release", "FAQ Generator", "Tweet Thread"]
        for i in range(12):
            cx = x + (i % 4) * (cw_ + 20)
            cy = y + 58 + (i // 4) * 196
            self.card(cx, cy, cw_, 176, r=14)
            col = cols[i % len(cols)]
            self.rect(cx + 20, cy + 20, 44, 44, mix(col, c["card"], 0.85), r=12)
            self.rect(cx + 34, cy + 34, 16, 16, col, r=4)
            self.add(self._star(cx + cw_ - 30, cy + 34, 8, AMBER if i % 3 == 0 else c["muted"]))
            self.text(cx + 20, cy + 94, names[i], 14, c["heading"], 700, spacing=-0.2)
            self.lines(cx + 20, cy + 110, cw_ - 40, 2, h=7, gap=14)
            self.pill(cx + 20, cy + 140, ["Blog", "eCommerce", "Ads", "Social", "Email", "SEO"][i % 6], col)
        return 58 + 3 * 196

    # POS screens
    def pos_terminal(self, x, y, w, h):
        c = self.c
        lw = w * 0.64
        self.rect(x, y, lw - 220, 46, c["card"], r=12, extra=f'stroke="{c["border"]}"')
        self.label(x + 44, y + 28, "Search products or scan barcode…", 13)
        self.rect(x + lw - 204, y, 204, 46, c["card"], r=12, extra=f'stroke="{c["border"]}"')
        for i in range(4):
            self.rect(x + lw - 190 + i * 46, y + 11, 24, 24, c["surface"], r=6)
        cats = ["All Items", "Beverages", "Bakery", "Snacks", "Dairy", "Fruits"]
        cx = x
        for i, t in enumerate(cats):
            tw = len(t) * 8 + 34
            self.rect(cx, y + 64, tw, 36, c["p"] if i == 0 else c["card"], r=10, extra="" if i == 0 else f'stroke="{c["border"]}"')
            self.text(cx + tw / 2, y + 87, t, 12, "#ffffff" if i == 0 else c["subtle"], 600, anchor="middle", spacing=0)
            cx += tw + 10
        pw = (lw - 3 * 16) / 4
        prices = ["$4.50", "$3.20", "$6.80", "$2.40", "$5.10", "$8.90", "$1.80", "$3.60", "$7.20", "$4.00", "$2.90", "$5.50"]
        for i in range(12):
            px = x + (i % 4) * (pw + 16)
            py = y + 120 + (i // 4) * 214
            if py + 200 > y + h:
                break
            self.card(px, py, pw, 200, r=12)
            if i in (1, 6):
                self.rect(px, py, pw, 200, "none", r=12, extra=f'stroke="{c["p"]}" stroke-width="2"')
            self.image(px + 10, py + 10, pw - 20, 110, r=9, kind="abstract" if i % 3 else "landscape")
            self.rect(px + 14, py + 136, pw * 0.65, 9, c["heading"], r=4, extra='opacity="0.85"')
            self.rect(px + 14, py + 152, pw * 0.4, 7, c["muted"], r=3)
            self.text(px + 14, py + 184, prices[i], 15, c["p"], 800, spacing=0)
            self.rect(px + pw - 42, py + 164, 28, 28, c["soft"], r=8)
            self.text(px + pw - 28, py + 184, "+", 16, c["p"], 800, anchor="middle")
        rx, rw = x + lw + 24, w - lw - 24
        self.card(rx, y, rw, h, r=14)
        self.text(rx + 24, y + 40, "Current Order", 17, c["heading"], 800, spacing=-0.2)
        self.label(rx + rw - 24, y + 40, "#1048", 13, anchor="end")
        self.rect(rx + 24, y + 58, rw - 48, 44, c["surface"], r=10)
        self.avatar(rx + 46, y + 80, 13, 1)
        self.rect(rx + 68, y + 76, 120, 8, c["heading"], r=4, extra='opacity="0.7"')
        items = [("Cappuccino", "$9.00"), ("Croissant", "$6.40"), ("Orange Juice", "$5.10"), ("Blueberry Muffin", "$7.20"), ("Greek Yogurt", "$4.00")]
        for k, (name, price) in enumerate(items):
            iy = y + 122 + k * 66
            self.image(rx + 24, iy, 46, 46, r=10, kind="abstract")
            self.text(rx + 84, iy + 18, name, 13, c["heading"], 700, spacing=0)
            self.rect(rx + 84, iy + 28, 92, 26, c["surface"], r=8)
            self.text(rx + 98, iy + 46, "–", 13, c["subtle"], 700, anchor="middle")
            self.text(rx + 130, iy + 46, str(1 + k % 3), 13, c["heading"], 700, anchor="middle")
            self.text(rx + 162, iy + 46, "+", 13, c["p"], 700, anchor="middle")
            self.text(rx + rw - 24, iy + 30, price, 14, c["heading"], 700, anchor="end", spacing=0)
        sy = y + 122 + len(items) * 66 + 10
        self.rect(rx + 24, sy, rw - 48, 1, c["border"])
        for k, (lab, val) in enumerate([("Subtotal", "$31.70"), ("Discount", "-$3.17"), ("Tax (8%)", "$2.28")]):
            self.label(rx + 24, sy + 30 + k * 28, lab, 13)
            self.text(rx + rw - 24, sy + 30 + k * 28, val, 13, c["heading"], 600, anchor="end", spacing=0)
        ty = sy + 30 + 3 * 28 + 8
        self.rect(rx + 24, ty - 18, rw - 48, 1, c["border"])
        self.text(rx + 24, ty + 12, "Total", 18, c["heading"], 800)
        self.text(rx + rw - 24, ty + 12, "$30.81", 22, c["p"], 800, anchor="end", spacing=-0.5)
        bw3 = (rw - 48 - 20) / 3
        for k, t in enumerate(["Cash", "Card", "Wallet"]):
            bx = rx + 24 + k * (bw3 + 10)
            self.rect(bx, ty + 36, bw3, 58, c["soft"] if k == 1 else c["surface"], r=10,
                      extra=f'stroke="{c["p"]}" stroke-width="2"' if k == 1 else "")
            self.rect(bx + bw3 / 2 - 9, ty + 46, 18, 14, c["p"] if k == 1 else c["subtle"], r=3)
            self.text(bx + bw3 / 2, ty + 82, t, 12, c["p"] if k == 1 else c["subtle"], 700, anchor="middle", spacing=0)
        self.rect(rx + 24, y + h - 80, rw - 48, 56, c["p"], r=12)
        self.text(rx + rw / 2, y + h - 45, "Charge $30.81", 16, "#ffffff", 800, anchor="middle", spacing=0)

    def barcodes(self, x, y, w):
        c = self.c
        lw_ = (w - 3 * 20) / 4
        names = ["Cappuccino", "Croissant", "Orange Juice", "Muffin", "Greek Yogurt", "Bagel", "Iced Tea", "Brownie"]
        for i in range(8):
            lx = x + (i % 4) * (lw_ + 20)
            ly = y + (i // 4) * 200
            self.card(lx, ly, lw_, 180, r=12)
            self.text(lx + lw_ / 2, ly + 32, names[i], 14, c["heading"], 700, anchor="middle", spacing=0)
            self.text(lx + lw_ / 2, ly + 54, f"${2 + i * 0.85:.2f}", 13, c["p"], 800, anchor="middle", spacing=0)
            bx = lx + 26
            while bx < lx + lw_ - 30:
                bw_ = self.rnd.choice([1.5, 2, 3, 4])
                self.rect(bx, ly + 70, bw_, 70, c["heading"])
                bx += bw_ + self.rnd.choice([1.5, 2, 3])
            self.text(lx + lw_ / 2, ly + 160, f"8 901234 5{i}678 {i}", 11, c["subtle"], 600, anchor="middle", spacing=1)
        return 400

    def roles(self, x, y, w, h):
        c = self.c
        self.card(x, y, w, h, r=14)
        self.card_title(x, y, w, "Role Permissions")
        roles = ["Admin", "Manager", "Cashier", "Accountant"]
        mods = ["Dashboard", "POS / Sales", "Products", "Purchases", "Inventory", "Customers", "Suppliers",
                "Expenses", "Reports", "Users & Roles", "Settings"]
        first = 260
        colw = (w - first - 40) / len(roles)
        self.rect(x + 1, y + 62, w - 2, 44, c["surface"])
        self.label(x + 24, y + 89, "MODULE", 11, weight=700)
        for k, r in enumerate(roles):
            self.label(x + first + k * colw + colw / 2, y + 89, r.upper(), 11, weight=700, anchor="middle")
        grants = {0: [1] * 11, 1: [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], 2: [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], 3: [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0]}
        for m, name in enumerate(mods):
            ry = y + 106 + m * 48
            if ry + 48 > y + h:
                break
            self.text(x + 24, ry + 29, name, 13, c["heading"], 600, spacing=0)
            for k in range(len(roles)):
                self.checkbox(x + first + k * colw + colw / 2 - 10, ry + 14, bool(grants[k][m]), size=20)
            self.rect(x + 20, ry + 47, w - 40, 1, c["border"])

    # WordPress screens
    def wp_importer(self, x, y, w):
        c = self.c
        self.rect(x, y, w, 56, c["card"], extra=f'stroke="{c["border"]}"')
        self.rect(x, y, 4, 56, c["p"])
        self.label(x + 24, y + 33, "Import a starter site with one click — content, widgets, menus and theme options included.", 13)
        cw_ = (w - 2 * 24) / 3
        names = ["Restaurant", "Law Firm", "Real Estate", "Yoga Studio", "Travel", "Construction"]
        for i in range(6):
            cx = x + (i % 3) * (cw_ + 24)
            cy = y + 84 + (i // 3) * 300
            self.rect(cx, cy, cw_, 280, c["card"], extra=f'stroke="{c["border"]}"')
            self.image(cx + 1, cy + 1, cw_ - 2, 190, r=0, kind=["landscape", "abstract", "person"][i % 3])
            self.text(cx + 18, cy + 226, names[i], 15, c["heading"], 700, spacing=0)
            self.button(cx + cw_ - 196, cy + 206, 84, 34, filled=False)
            self.button(cx + cw_ - 102, cy + 206, 84, 34)
            if i == 1:
                self.rect(cx + 1, cy + 1, cw_ - 2, 190, "#0b1020bb")
                self.text(cx + cw_ / 2, cy + 90, "Importing… 68%", 15, "#ffffff", 700, anchor="middle", spacing=0)
                self.rect(cx + 40, cy + 108, cw_ - 80, 8, "#ffffff33", r=4)
                self.rect(cx + 40, cy + 108, (cw_ - 80) * 0.68, 8, c["p"], r=4)
        return 84 + 600

    def builder(self):
        """Visual page-builder screen (drag & drop editor)."""
        c = self.c
        H = 900
        pw = 300
        self.rect(0, 0, pw, H, "#f4f5f7")
        self.rect(0, 0, pw, 56, c["p"])
        self.rect(18, 20, 18, 16, "#ffffff", r=3)
        self.rect(pw - 36, 20, 18, 16, "#ffffff", r=3)
        self.text(pw / 2, 34, "Widgets", 14, "#ffffff", 700, anchor="middle", spacing=0)
        self.rect(16, 72, pw - 32, 38, "#ffffff", r=8, extra='stroke="#e3e6ea"')
        self.rect(30, 87, 110, 8, "#c9ced6", r=4)
        tw = (pw - 32 - 12) / 2
        names = ["Heading", "Image", "Text", "Button", "Icon Box", "Gallery", "Video", "Testimonial", "Pricing", "Counter", "Tabs", "Form"]
        for i, nm in enumerate(names):
            tx = 16 + (i % 2) * (tw + 12)
            ty = 128 + (i // 2) * 104
            self.rect(tx, ty, tw, 92, "#ffffff", r=10, extra='stroke="#e3e6ea"')
            self.rect(tx + tw / 2 - 14, ty + 20, 28, 28, mix(c["p"], "#ffffff", 0.85) if i != 1 else c["p"], r=7)
            self.text(tx + tw / 2, ty + 72, nm, 12, "#3c434a", 600, anchor="middle", spacing=0)
        self.rect(0, H - 56, pw, 56, "#ffffff", extra='stroke="#e3e6ea"')
        for i in range(4):
            self.rect(20 + i * 40, H - 38, 20, 20, "#c9ced6", r=5)
        self.rect(pw - 116, H - 44, 96, 32, c["p"], r=8)
        self.text(pw - 68, H - 23, "Publish", 13, "#ffffff", 700, anchor="middle", spacing=0)
        # canvas
        cx, cw_ = pw + 30, AW - pw - 60
        self.rect(pw, 0, AW - pw, H, "#e9ebef")
        self.rect(cx, 24, cw_, H - 24, "#ffffff")
        self.rect(cx, 24, cw_, 60, "#ffffff", extra='stroke="#eef0f3"')
        self.rect(cx + 28, 44, 20, 20, c["p"], r=5)
        self.text(cx + 56, 60, self.name, 15, "#111827", 800)
        for i in range(4):
            self.rect(cx + cw_ - 380 + i * 70, 50, 50, 7, "#9aa1ad", r=3)
        self.button(cx + cw_ - 112, 38, 92, 32)
        hy = 84
        self.rect(cx, hy, cw_, 380, mix(c["p"], "#ffffff", 0.92))
        self.text(cx + 48, hy + 120, "Build beautiful", 40, "#111827", 800, spacing=-1.4)
        self.text(cx + 48, hy + 166, "websites visually", 40, "#111827", 800, spacing=-1.4)
        # selection outline on heading
        self.rect(cx + 38, hy + 80, 400, 104, "none", extra=f'stroke="{c["p"]}" stroke-width="2" stroke-dasharray="6 4"')
        self.rect(cx + 38, hy + 58, 96, 22, c["p"], r=4)
        self.text(cx + 86, hy + 73, "Heading", 11, "#ffffff", 700, anchor="middle", spacing=0)
        self.lines(cx + 48, hy + 210, 340, 2, "#c9ced6")
        self.button(cx + 48, hy + 262, 140, 46)
        self.image(cx + cw_ - 380, hy + 50, 330, 280, r=18, kind="person")
        fy = hy + 410
        fw = (cw_ - 96 - 40) / 3
        for i in range(3):
            fx = cx + 48 + i * (fw + 20)
            self.rect(fx, fy, fw, 170, "#ffffff", r=12, extra='stroke="#eceef2"')
            self.rect(fx + 20, fy + 22, 42, 42, mix(c["p"], "#ffffff", 0.85), r=10)
            self.rect(fx + 20, fy + 84, fw * 0.5, 11, "#111827", r=5, extra='opacity="0.85"')
            self.lines(fx + 20, fy + 108, fw - 40, 3, "#dfe3e8", h=7, gap=14)
        # drop placeholder
        self.rect(cx + 48, fy + 200, cw_ - 96, 90, "none", r=12, extra=f'stroke="{c["p"]}" stroke-width="2" stroke-dasharray="8 6"')
        self.circle(cx + cw_ / 2, fy + 245, 18, c["p"])
        self.text(cx + cw_ / 2, fy + 251, "+", 20, "#ffffff", 700, anchor="middle")
        # dragged widget ghost
        self.rect(cx + cw_ / 2 + 40, fy + 205, 120, 80, "#ffffff", r=10, extra=f'stroke="{c["p"]}" stroke-width="2" {self.shadow()}')
        self.rect(cx + cw_ / 2 + 86, fy + 220, 28, 28, c["p"], r=7)
        self.text(cx + cw_ / 2 + 100, fy + 270, "Gallery", 12, "#3c434a", 600, anchor="middle", spacing=0)
        self.y = H


# --------------------------------------------------------------------------- #
# Screen definitions
# --------------------------------------------------------------------------- #
ADMIN = "#0284c7"
AI = "#7c3aed"
POS = "#059669"
WP = "#e11d48"


def admin_dashboard(kind, dark=False, sidebar="light", name="Vantage", primary=ADMIN, seed=1):
    cv = AppCanvas(primary, dark, name, seed, sidebar)
    titles = {"analytics": "Analytics", "ecommerce": "eCommerce", "crm": "CRM", "project": "Projects",
              "finance": "Finance", "saas": "SaaS Metrics", "hrm": "HR Management", "logistics": "Logistics"}
    cv.shell(titles[kind] + " Dashboard", active=1 + (seed % 3))
    k = {
        "analytics": [("Total Visitors", "48.2k", "12.5%", True), ("Page Views", "126k", "8.1%", True), ("Bounce Rate", "32.4%", "2.3%", False), ("Avg. Session", "4m 12s", "5.6%", True)],
        "ecommerce": [("Revenue", "$84,250", "18.2%", True), ("Orders", "1,284", "9.4%", True), ("Customers", "3,912", "6.7%", True), ("Refunds", "$1,120", "1.8%", False)],
        "crm": [("New Leads", "642", "14.0%", True), ("Deals Won", "$212k", "11.3%", True), ("Conversion", "24.6%", "3.1%", True), ("Churned", "18", "4.2%", False)],
        "project": [("Active Projects", "28", "4 new", True), ("Tasks Done", "1,045", "16.4%", True), ("Hours Logged", "3,420h", "7.2%", True), ("Overdue", "7", "2 more", False)],
        "finance": [("Balance", "$128,430", "6.3%", True), ("Income", "$42,900", "12.0%", True), ("Expenses", "$18,240", "3.5%", False), ("Savings", "$24,660", "9.8%", True)],
        "saas": [("MRR", "$64,800", "9.1%", True), ("Active Users", "12,480", "13.6%", True), ("Churn Rate", "2.1%", "0.4%", True), ("ARPU", "$51.90", "3.2%", True)],
        "hrm": [("Employees", "248", "12 new", True), ("On Leave", "14", "3.0%", False), ("Open Roles", "19", "5 new", True), ("Payroll", "$412k", "2.4%", True)],
        "logistics": [("Shipments", "3,218", "10.2%", True), ("In Transit", "642", "4.8%", True), ("Delivered", "2,481", "12.1%", True), ("Delayed", "38", "1.2%", False)],
    }[kind]
    cv.kpis(k)
    x1, w1, x2, w2 = cv.grid2()
    y = cv.y
    big = {"analytics": ("area", "Traffic Overview"), "ecommerce": ("bar", "Sales Report"), "crm": ("line2", "Pipeline Value"),
           "project": ("bar", "Task Completion"), "finance": ("area", "Cash Flow"), "saas": ("line2", "MRR Growth"),
           "hrm": ("bar", "Attendance"), "logistics": ("map", "Live Tracking")}[kind]
    side = {"analytics": "donut", "ecommerce": "radial", "crm": "donut", "project": "radial", "finance": "donut",
            "saas": "radial", "hrm": "donut", "logistics": "hbar"}[kind]
    side_t = {"donut": "Breakdown", "radial": "Monthly Target", "hbar": "Top Routes"}[side]
    cv.chart(x1, y, w1, 360, big[0], big[1])
    if kind == "finance":
        cv.rect(x2, y, w2, 190, cv.grad(mix(cv.c["p"], "#000000", 0.25), cv.c["p"]), r=16)
        cv.circle(x2 + w2 - 40, y + 30, 70, "#ffffff", 'opacity="0.1"')
        cv.rect(x2 + 24, y + 28, 42, 30, "#ffd27a", r=6)
        cv.text(x2 + 24, y + 112, "•••• •••• •••• 4821", 18, "#ffffff", 700, spacing=1)
        cv.label(x2 + 24, y + 152, "ALEX MORGAN", 12, "#ffffffcc", 700)
        cv.label(x2 + w2 - 24, y + 152, "09/29", 12, "#ffffffcc", 700, anchor="end")
        cv.list_card(x2, y + 210, w2, 150, "Quick Transfer")
    else:
        cv.chart(x2, y, w2, 360, side, side_t)
    cv.y = y + 384
    y = cv.y
    tables = {
        "analytics": ("Top Pages", ("Page", "Views", "Avg. Time", "Status"), dict(avatar=False, status=("Active", "Active", "Draft", "Active", "Active"))),
        "ecommerce": ("Recent Orders", ("Product", "Customer", "Amount", "Status"), dict(thumb=True, status=("Delivered", "Pending", "Shipped", "Delivered", "Cancelled"))),
        "crm": ("Latest Leads", ("Contact", "Company", "Value", "Stage"), dict(status=("Active", "Pending", "Active", "Failed", "Active"))),
        "project": ("Project Status", ("Project", "Lead", "Progress", "Status"), dict(progress=True, status=("Active", "Pending", "Completed", "Active", "Active"))),
        "finance": ("Transactions", ("Description", "Date", "Amount", "Status"), dict(status=("Paid", "Paid", "Pending", "Paid", "Failed"))),
        "saas": ("New Subscriptions", ("Customer", "Plan", "MRR", "Status"), dict(status=("Active", "Active", "Pending", "Active", "Cancelled"))),
        "hrm": ("Employees", ("Employee", "Department", "Joined", "Status"), dict(status=("Active", "Active", "Pending", "Active", "Active"))),
        "logistics": ("Shipments", ("Shipment", "Destination", "ETA", "Status"), dict(avatar=False, status=("Delivered", "Shipped", "Pending", "Shipped", "Delivered"))),
    }[kind]
    th = cv.table(x1, y, w1, tables[0], 5, tables[1], **tables[2])
    if kind == "hrm":
        cv.calendar(x2, y, w2, th)
    else:
        cv.list_card(x2, y, w2, th, {"ecommerce": "Top Products", "logistics": "Drivers", "project": "Team"}.get(kind, "Top Performers"),
                     thumb=kind == "ecommerce")
    cv.y = y + th
    return cv


def admin_app(kind, name="Vantage", primary=ADMIN, seed=50, sidebar="light"):
    cv = AppCanvas(primary, False, name, seed, sidebar)
    title = {"chat": "Chat", "email": "Inbox", "calendar": "Calendar", "kanban": "Kanban Board", "file-manager": "File Manager",
             "invoice": "Invoice Details", "users": "Users", "profile": "User Profile", "pricing": "Pricing Plans",
             "settings": "Settings"}[kind]
    cv.shell(title, active=3 + seed % 4)
    x, y, w = cv.x0, cv.y, cv.cw
    if kind == "chat":
        cv.chat(x, y, w, 720)
        cv.y += 720
    elif kind == "email":
        cv.email(x, y, w, 720)
        cv.y += 720
    elif kind == "calendar":
        cv.calendar(x, y, w, 720)
        cv.y += 720
    elif kind == "kanban":
        cv.kanban(x, y, w, 720)
        cv.y += 720
    elif kind == "file-manager":
        h = cv.files(x, y, w)
        cv.y += h
        x1, w1, x2, w2 = cv.grid2(0.68)
        th = cv.table(x1, cv.y, w1, "Recent Files", 6, ("Name", "Owner", "Size", "Modified"), avatar=False, thumb=True, status=None)
        cv.chart(x2, cv.y, w2, th, "donut", "Storage")
        cv.y += th
    elif kind == "invoice":
        cv.invoice(x, y, w, 760)
        cv.y += 760
    elif kind == "users":
        cv.kpis([("Total Users", "12,480", "8.2%", True), ("Active", "9,812", "5.4%", True), ("Pending", "342", "1.2%", False), ("Banned", "28", "0.3%", True)])
        cv.y += cv.table(x, cv.y, w, "All Users", 8, ("User", "Role", "Plan", "Joined", "Status"), check=True,
                         status=("Active", "Active", "Pending", "Active", "Cancelled", "Active", "Pending", "Active"))
    elif kind == "profile":
        cv.y += cv.profile(x, y, w)
    elif kind == "pricing":
        cv.y += cv.plans(x, y, w)
        cv.y += cv.table(x, cv.y, w, "Plan Subscribers", 4, ("Customer", "Plan", "Billing", "Status"), status=("Active", "Active", "Pending", "Active"))
    elif kind == "settings":
        cv.form(x, y, w, 760, "General Settings")
        cv.y += 760
    return cv


def auth_page(kind, primary, name, seed):
    cv = Canvas(primary, False, name, seed)
    if kind == "login":
        cv.special_login()
    else:
        cv.special_404()
    return cv


def ai_screen(kind, seed):
    if kind == "landing":
        cv = Canvas(AI, False, "Quillo", seed)
        cv.hero("center", ["Create content", "10x faster with AI"])
        for s in ["logos", "features3", "split", "split", "pricing", "testimonials", "faq", "cta"]:
            getattr(cv, s)(**({"flip": True} if s == "split" and seed % 2 else {}))
        cv.footer()
        return cv
    sidebar = "dark" if kind.startswith("admin") else "light"
    cv = AppCanvas(AI, False, "Quillo", seed, sidebar)
    titles = {"dashboard": "Dashboard", "writer": "AI Writer", "image": "AI Image Generator", "chat": "AI Chat",
              "templates": "Templates", "documents": "My Documents", "admin-dashboard": "Admin Dashboard",
              "admin-plans": "Subscription Plans", "admin-gateways": "Payment Gateways", "admin-users": "Users",
              "admin-settings": "AI Settings", "admin-affiliate": "Affiliate Program"}
    cv.shell(titles[kind], active=1 + seed % 6)
    x, y, w = cv.x0, cv.y, cv.cw
    if kind == "dashboard":
        cv.kpis([("Words Generated", "184,520", "12%", True), ("Images Created", "1,248", "8%", True), ("Documents", "326", "5%", True), ("Credits Left", "62,400", "18%", False)])
        x1, w1, x2, w2 = cv.grid2()
        cv.chart(x1, cv.y, w1, 340, "area", "Usage This Month")
        cv.chart(x2, cv.y, w2, 340, "donut", "Usage by Tool")
        cv.y += 364
        th = cv.table(x1, cv.y, w1, "Recent Documents", 5, ("Document", "Template", "Words", "Status"), avatar=False,
                      status=("Completed", "Completed", "Draft", "Completed", "Draft"))
        cv.list_card(x2, cv.y, w2, th, "Favorite Templates", values=["Blog", "Ads", "Email", "SEO", "Social"])
        cv.y += th
    elif kind == "writer":
        cv.writer(x, y, w, 760)
        cv.y += 760
    elif kind == "image":
        cv.image_gen(x, y, w, 760)
        cv.y += 760
    elif kind == "chat":
        cv.chat(x, y, w, 740, ai=True)
        cv.y += 740
    elif kind == "templates":
        cv.y += cv.templates(x, y, w)
    elif kind == "documents":
        cv.y += cv.table(x, y, w, "All Documents", 9, ("Document", "Template", "Language", "Words", "Status"), avatar=False, check=True,
                         status=("Completed", "Draft", "Completed", "Completed", "Draft", "Completed", "Completed", "Draft", "Completed"))
    elif kind == "admin-dashboard":
        cv.kpis([("Total Revenue", "$48,920", "22%", True), ("Subscribers", "2,846", "14%", True), ("New Users", "612", "9%", True), ("API Cost", "$3,140", "6%", False)])
        x1, w1, x2, w2 = cv.grid2()
        cv.chart(x1, cv.y, w1, 340, "line2", "Revenue vs. API Cost")
        cv.chart(x2, cv.y, w2, 340, "donut", "Plans")
        cv.y += 364
        th = cv.table(x1, cv.y, w1, "Latest Transactions", 5, ("User", "Plan", "Amount", "Status"))
        cv.list_card(x2, cv.y, w2, th, "Top Users", values=["98k", "84k", "71k", "64k", "52k"])
        cv.y += th
    elif kind == "admin-plans":
        cv.y += cv.plans(x, y, w)
        cv.y += cv.table(x, cv.y, w, "Credit Packs", 4, ("Pack", "Words", "Images", "Price", "Status"), avatar=False, status=("Active", "Active", "Draft", "Active"))
    elif kind == "admin-gateways":
        cv.form(x, y, w, 720, "Payment Gateways", gateways=[
            ("Stripe", "#635bff", True), ("PayPal", "#003087", True), ("Razorpay", "#0c2451", True),
            ("Paystack", "#0ba4db", False), ("Mollie", "#111111", False), ("Bank", "#475569", True), ("Crypto", "#f7931a", False)])
        cv.y += 720
    elif kind == "admin-users":
        cv.y += cv.table(x, y, w, "Users", 10, ("User", "Plan", "Credits", "Joined", "Status"), check=True,
                         status=("Active", "Active", "Pending", "Active", "Cancelled", "Active", "Active", "Pending", "Active", "Active"))
    elif kind == "admin-settings":
        cv.form(x, y, w, 760, "AI Provider Settings", tabs=("OpenAI", "Anthropic", "Gemini", "Stable Diffusion", "Speech", "Limits"))
        cv.y += 760
    elif kind == "admin-affiliate":
        cv.kpis([("Affiliates", "418", "11%", True), ("Referrals", "2,104", "16%", True), ("Commission", "$9,820", "7%", True), ("Payouts", "$6,400", "3%", True)])
        cv.y += cv.table(x, cv.y, w, "Payout Requests", 6, ("Affiliate", "Method", "Amount", "Status"),
                         status=("Pending", "Paid", "Paid", "Pending", "Failed", "Paid"))
    return cv


def pos_screen(kind, seed):
    if kind == "login":
        return auth_page("login", POS, "Stockly", seed)
    sidebar = "none" if kind == "terminal" else "dark"
    cv = AppCanvas(POS, False, "Stockly", seed, sidebar)
    titles = {"dashboard": "Dashboard", "terminal": None, "products": "Products", "add-product": "Add Product",
              "purchase": "Purchase Invoice", "inventory": "Stock Inventory", "reports": "Sales Report",
              "barcodes": "Print Barcodes", "customers": "Customers", "roles": "Roles & Permissions", "settings": "Business Settings"}
    cv.shell(titles[kind], active=1 + seed % 7)
    x, y, w = cv.x0, cv.y, cv.cw
    if kind == "dashboard":
        cv.kpis([("Today's Sales", "$8,420", "14%", True), ("Purchases", "$3,180", "6%", True), ("Net Profit", "$2,940", "9%", True), ("Expenses", "$640", "3%", False)])
        x1, w1, x2, w2 = cv.grid2()
        cv.chart(x1, cv.y, w1, 340, "bar", "Sales vs. Purchases")
        cv.chart(x2, cv.y, w2, 340, "donut", "Sales by Category")
        cv.y += 364
        th = cv.table(x1, cv.y, w1, "Recent Sales", 5, ("Invoice", "Customer", "Total", "Payment"), avatar=False,
                      status=("Paid", "Paid", "Pending", "Paid", "Paid"))
        cv.list_card(x2, cv.y, w2, th, "Stock Alerts", thumb=True, values=["3 left", "5 left", "0 left", "2 left", "4 left"])
        cv.y += th
    elif kind == "terminal":
        cv.pos_terminal(x, y, w, 800)
        cv.y += 800
    elif kind == "products":
        cv.y += cv.table(x, y, w, "All Products", 9, ("Product", "SKU", "Category", "Price", "Stock", "Status"), thumb=True, check=True,
                         status=("In Stock", "In Stock", "Low Stock", "In Stock", "Out of Stock", "In Stock", "Low Stock", "In Stock", "In Stock"))
    elif kind == "add-product":
        cv.form(x, y, w, 760, "Product Information", tabs=("Basic Info", "Pricing", "Inventory", "Variants", "Images", "SEO"))
        cv.y += 760
    elif kind == "purchase":
        cv.invoice(x, y, w, 760)
        cv.y += 760
    elif kind == "inventory":
        cv.kpis([("Stock Value", "$184,200", "4%", True), ("Products", "1,248", "32 new", True), ("Low Stock", "18", "5", False), ("Warehouses", "3", "1 new", True)])
        cv.y += cv.table(x, cv.y, w, "Warehouse Stock", 7, ("Product", "Warehouse", "Qty", "Value", "Status"), thumb=True,
                         status=("In Stock", "Low Stock", "In Stock", "In Stock", "Out of Stock", "In Stock", "Low Stock"))
    elif kind == "reports":
        cv.kpis([("Revenue", "$248,900", "18%", True), ("Cost", "$162,400", "9%", False), ("Gross Profit", "$86,500", "24%", True), ("Margin", "34.7%", "2.1%", True)])
        x1, w1, x2, w2 = cv.grid2(0.6)
        cv.chart(x1, cv.y, w1, 360, "area", "Revenue Trend")
        cv.chart(x2, cv.y, w2, 360, "hbar", "Top Selling Products")
        cv.y += 384
        cv.y += cv.table(x, cv.y, w, "Daily Summary", 4, ("Date", "Orders", "Revenue", "Profit", "Status"), avatar=False,
                         status=("Completed", "Completed", "Completed", "Pending"))
    elif kind == "barcodes":
        cv.card(x, y, w, 90)
        cv.label(x + 24, y + 38, "Product", 12, cv.c["heading"], 700)
        cv.rect(x + 24, y + 48, w * 0.4, 30, cv.c["surface"], r=8)
        cv.label(x + w * 0.45, y + 38, "Paper size", 12, cv.c["heading"], 700)
        cv.rect(x + w * 0.45, y + 48, w * 0.25, 30, cv.c["surface"], r=8)
        cv.button(x + w - 160, y + 42, 136, 38)
        cv.y += 114
        cv.y += cv.barcodes(x, cv.y, w)
    elif kind == "customers":
        cv.y += cv.table(x, y, w, "Customers", 9, ("Customer", "Phone", "Orders", "Spent", "Status"), check=True,
                         status=("Active", "Active", "Active", "Pending", "Active", "Active", "Cancelled", "Active", "Active"))
    elif kind == "roles":
        cv.roles(x, y, w, 640)
        cv.y += 640
    elif kind == "settings":
        cv.form(x, y, w, 760, "Business Settings", tabs=("Business", "Tax & Currency", "Receipt", "Payment Methods", "Notifications", "Backup"))
        cv.y += 760
    return cv


def wp_site(i, name, color, dark, hero, headline, sections):
    cv = Canvas(color, dark, name, seed=200 + i)
    cv.hero(hero, headline)
    from generate_thumbnails import run_sections
    run_sections(cv, sections)
    cv.footer()
    return cv


WP_SITES = [
    ("01-restaurant", "Savora", "#b45309", True, "full", ["Taste the art", "of fine food"], ["gallery", "split:flip", "testimonials", "cta"]),
    ("02-law", "Lexway", "#1e3a8a", False, "full", ["Trusted legal", "counsel"], ["features3", "split", "team", "testimonials", "cta"]),
    ("03-real-estate", "Habitat", "#0d9488", False, "split", ["Find your", "dream home"], ["products:nohead", "split:flip", "team", "cta"]),
    ("04-yoga", "Zenla", "#65a30d", False, "split", ["Find balance,", "breathe deeply"], ["features3", "split", "pricing", "testimonials", "cta"]),
    ("05-magazine", "Daily", "#dc2626", False, "split", ["Stories worth", "reading"], ["blog", "blog:nohead", "split", "cta"]),
    ("06-travel", "Wander", "#0284c7", False, "full", ["Explore the", "world with us"], ["gallery", "split", "testimonials", "blog", "cta"]),
    ("07-construction", "Buildco", "#d97706", True, "full", ["We build", "your vision"], ["features3", "split:flip", "stats", "gallery:nohead", "cta"]),
    ("08-charity", "Hopewell", "#16a34a", False, "split", ["Together we", "change lives"], ["stats", "features3", "split:flip", "blog", "cta"]),
    ("09-fitness", "Ironfit", "#ef4444", True, "portfolio", ["Stronger", "every day."], ["features3", "pricing", "team", "cta"]),
    ("10-florist", "Bloom", "#db2777", False, "shop", ["Fresh flowers", "delivered"], ["products", "testimonials", "cta"]),
    ("11-education", "Learnly", "#7c3aed", False, "center", ["Learn new skills", "online"], ["logos", "features3", "split", "pricing", "faq", "cta"]),
    ("12-dental", "Smilecare", "#0891b2", False, "split", ["Healthy smiles", "start here"], ["features3", "split", "team", "form", "cta"]),
]


def generate(root):
    import os

    def save(cv, folder, fname):
        d = os.path.join(root, "assets", "img", folder)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f"{fname}.svg"), "w") as fh:
            fh.write(cv.svg())

    n = 0
    # Admin dashboard template
    for i, kind in enumerate(["analytics", "ecommerce", "crm", "project", "finance", "saas", "hrm", "logistics"]):
        sidebar = ["light", "dark", "light", "horizontal", "dark", "light", "dark", "light"][i]
        save(admin_dashboard(kind, dark=kind in ("finance",), sidebar=sidebar, seed=i + 1), "admin", f"dash-{kind}"); n += 1
    for mode, (dark, sb) in {"light": (False, "light"), "dark": (True, "dark"), "semi-dark": (False, "dark"), "horizontal": (False, "horizontal")}.items():
        save(admin_dashboard("analytics", dark=dark, sidebar=sb, seed=1), "admin", f"layout-{mode}"); n += 1
    for i, kind in enumerate(["chat", "email", "calendar", "kanban", "file-manager", "invoice", "users", "profile", "pricing", "settings"]):
        save(admin_app(kind, seed=50 + i), "admin", f"app-{kind}"); n += 1
    save(auth_page("login", ADMIN, "Vantage", 70), "admin", "app-login"); n += 1
    save(auth_page("404", ADMIN, "Vantage", 71), "admin", "app-404"); n += 1

    # AI SaaS script
    for i, kind in enumerate(["landing", "dashboard", "writer", "image", "chat", "templates",
                              "admin-dashboard", "admin-plans", "admin-gateways", "admin-users", "admin-settings", "admin-affiliate"]):
        save(ai_screen(kind, 300 + i), "ai", kind); n += 1

    # POS script
    for i, kind in enumerate(["dashboard", "terminal", "products", "add-product", "purchase", "inventory",
                              "reports", "barcodes", "customers", "roles", "settings", "login"]):
        save(pos_screen(kind, 400 + i), "pos", kind); n += 1

    # WordPress theme
    for i, (fname, name, color, dark, hero, headline, sections) in enumerate(WP_SITES):
        save(wp_site(i, name, color, dark, hero, headline, sections), "wp", fname); n += 1
    cv = AppCanvas(WP, False, "Aurelia", 500, sidebar="wp")
    cv.shell("Starter Sites", active=9, crumbs=False)
    cv.y += cv.wp_importer(cv.x0, cv.y, cv.cw)
    save(cv, "wp", "importer"); n += 1
    cv = AppCanvas(WP, False, "Aurelia", 501, sidebar="none")
    cv.builder()
    cv.y -= 28  # builder fills the canvas exactly
    save(cv, "wp", "builder"); n += 1
    return n
