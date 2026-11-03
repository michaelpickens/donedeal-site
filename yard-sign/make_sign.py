#!/usr/bin/env python3
"""Build the Done Deal two-sided yard sign as a print-ready PDF.

Usage:
    python3 make_sign.py

Output: yard-sign.pdf, two pages (Face A: job site, Face B: roadside).
Trim 24 x 18 in (standard coroplast yard sign, H-stake), 0.125 in bleed on
every side, so each page is 24.25 x 18.25 in. Order as "double-sided, I have
my own bleed". Keep everything important inside the 0.5 in safe margin.

Fonts: Anton + Barlow TTFs in ../review-card/fonts.
Requires: reportlab, qrcode, pillow
"""
import os, io
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "review-card", "fonts")
OUT = os.path.join(HERE, "yard-sign.pdf")

SITE_URL = "https://www.donedealhandyman.com/"
PHONE = "(720) 295-5617"

NAVY, NAVY_DEEP, YELLOW, RED, PAPER, INK = (
    "#16305E", "#0F2347", "#F2C200", "#B02A30", "#F7F4EE", "#161B26")

for name, file in [("Anton", "anton-latin-400-normal.ttf"),
                   ("Barlow", "barlow-latin-400-normal.ttf"),
                   ("Barlow-Bold", "barlow-latin-700-normal.ttf"),
                   ("Barlow-XBold", "barlow-latin-800-normal.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, file)))

BLEED = 0.125 * inch
TRIM_W, TRIM_H = 24 * inch, 18 * inch
PAGE_W, PAGE_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
SAFE = BLEED + 0.5 * inch


def qr_image(url, fill, back):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0, box_size=40)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color=fill, back_color=back).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def check_mark(c, x, y, size, color):
    s = size / 64.0
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(9 * s)
    c.setLineCap(1)
    c.setLineJoin(1)
    p = c.beginPath()
    p.moveTo(x + 14 * s, y + size - 34 * s)
    p.lineTo(x + 26 * s, y + size - 46 * s)
    p.lineTo(x + 50 * s, y + size - 20 * s)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def fit_size(c, text, font, max_size, max_width):
    """Largest point size at or below max_size whose string fits max_width."""
    w = c.stringWidth(text, font, max_size)
    return max_size if w <= max_width else max_size * max_width / w


def centered(c, text, y, font, size, color, x=None):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(PAGE_W / 2 if x is None else x, y, text)


def face(c, headline_lines, sub_line, bottom_line):
    top = PAGE_H  # measure from the top edge of the page
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.rect(0, 0, PAGE_W, BLEED + 0.45 * inch, stroke=0, fill=1)

    # wordmark with check badge, top center
    badge = 1.3 * inch
    wm = 1.9 * inch
    gap = 0.28 * inch
    wm_w = c.stringWidth("DONE DEAL", "Anton", wm)
    x0 = (PAGE_W - (badge + gap + wm_w)) / 2
    by0 = top - SAFE - 0.05 * inch - badge
    c.setFillColor(YELLOW)
    c.roundRect(x0, by0, badge, badge, 0.16 * inch, stroke=0, fill=1)
    check_mark(c, x0, by0, badge, NAVY)
    c.setFillColor(YELLOW)
    c.setFont("Anton", wm)
    c.drawString(x0 + badge + gap, by0 + 0.1 * inch, "DONE DEAL")
    sub = "PAINTING & FLOORING"
    sub_sz = 0.62 * inch
    c.setFillColor("white")
    c.setFont("Barlow-XBold", sub_sz)
    sub_w = c.stringWidth(sub, "Barlow-XBold", sub_sz)
    c.drawString(x0 + badge + gap + (wm_w - sub_w) / 2, by0 - 0.62 * inch, sub)

    # headline, two lines, white Anton, fitted to width
    avail = PAGE_W - 2 * SAFE
    hl = min(fit_size(c, l, "Anton", 2.5 * inch, avail) for l in headline_lines)
    centered(c, headline_lines[0], top - 6.35 * inch, "Anton", hl, "white")
    centered(c, headline_lines[1], top - 6.35 * inch - hl * 0.98, "Anton", hl, "white")

    # yellow sub line
    ss = fit_size(c, sub_line, "Barlow-XBold", 0.9 * inch, avail)
    centered(c, sub_line, top - 10.0 * inch, "Barlow-XBold", ss, YELLOW)

    # phone block, yellow with navy number fitted to the block
    blk_w, blk_h = avail, 3.4 * inch
    bx, by = SAFE, top - 14.1 * inch
    c.setFillColor(YELLOW)
    c.roundRect(bx, by, blk_w, blk_h, 0.3 * inch, stroke=0, fill=1)
    ps = fit_size(c, PHONE, "Anton", 3.0 * inch, blk_w - 1.4 * inch)
    centered(c, PHONE, by + (blk_h - ps * 0.72) / 2, "Anton", ps, NAVY)

    # QR, bottom right, with a tiny label
    qr_box = 2.1 * inch
    qx = PAGE_W - SAFE - qr_box
    qy = BLEED + 0.45 * inch + 0.72 * inch
    c.setFillColor("white")
    c.roundRect(qx, qy, qr_box, qr_box, 0.14 * inch, stroke=0, fill=1)
    pad = 0.15 * inch
    c.drawImage(qr_image(SITE_URL, NAVY_DEEP, "white"), qx + pad, qy + pad,
                qr_box - 2 * pad, qr_box - 2 * pad)
    centered(c, "SCAN FOR A QUOTE", qy - 0.42 * inch, "Barlow-Bold", 0.26 * inch, "white",
             x=qx + qr_box / 2)

    # bottom line, centered in the space left of the QR
    bs = 0.85 * inch
    cx = SAFE + (qx - 0.4 * inch - SAFE) / 2
    centered(c, bottom_line, qy + 0.75 * inch, "Barlow-Bold", bs, "white", x=cx)


def face_a(c):
    face(c, ["FRESH PAINT.", "NEW FLOORS."],
         "HAPPENING RIGHT HERE",
         "FREE ESTIMATES  ·  VETERAN-OWNED")


def face_b(c):
    face(c, ["INTERIOR PAINTING", "& NEW FLOORS"],
         "LVP  ·  LAMINATE  ·  HARDWOOD  ·  CABINETS  ·  WALLS & TRIM",
         "FREE ESTIMATES  ·  VETERAN-OWNED")


c = canvas.Canvas(OUT, pagesize=(PAGE_W, PAGE_H))
c.setTitle("Done Deal yard sign, 24x18, two-sided")
face_a(c)
c.showPage()
face_b(c)
c.showPage()
c.save()
print("wrote", OUT)
