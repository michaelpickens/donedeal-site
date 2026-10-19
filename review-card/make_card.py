#!/usr/bin/env python3
"""Build the Done Deal review request card (front + back) as a print-ready PDF.

Usage:
    python3 make_card.py "https://g.page/r/XXXXXXXX/review"

Output: review-card.pdf (two pages, 3.5 x 2 in trim with 0.125 in bleed on
every side, so the page is 3.75 x 2.25 in). Upload to any business-card
printer (Vistaprint, MOO, local shop) and choose "I have my own bleed".

Fonts: Anton + Barlow TTFs in ./fonts (converted from @fontsource).
Requires: reportlab, qrcode, pillow  (pip install reportlab qrcode pillow)
"""
import sys, os, io
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(os.path.abspath(__file__))
REVIEW_URL = sys.argv[1] if len(sys.argv) > 1 else "https://g.page/r/REPLACE_WITH_REAL_LINK/review"
OUT = os.path.join(HERE, "review-card.pdf")

NAVY, NAVY_DEEP, YELLOW, RED, PAPER, INK, STEEL = (
    "#16305E", "#0F2347", "#F2C200", "#B02A30", "#F7F4EE", "#161B26", "#5B6474")

for name, file in [("Anton", "anton-latin-400-normal.ttf"),
                   ("Barlow", "barlow-latin-400-normal.ttf"),
                   ("Barlow-Bold", "barlow-latin-700-normal.ttf"),
                   ("Barlow-XBold", "barlow-latin-800-normal.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(HERE, "fonts", file)))

BLEED = 0.125 * inch
TRIM_W, TRIM_H = 3.5 * inch, 2.0 * inch
PAGE_W, PAGE_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
SAFE = BLEED + 0.125 * inch  # keep text inside this margin


def qr_image(url, fill, back):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0, box_size=20)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color=fill, back_color=back).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def check_mark(c, x, y, size, color):
    """Same check mark as the site favicon, scaled to `size`."""
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


def wordmark(c, x, y, main_size, sub_color, main_color):
    c.setFillColor(main_color)
    c.setFont("Anton", main_size)
    c.drawString(x, y, "DONE DEAL")
    c.setFillColor(sub_color)
    c.setFont("Barlow-Bold", main_size * 0.42)
    c.drawString(x, y - main_size * 0.5, "PAINTING & FLOORS")


def front(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # yellow rule along the bottom, like the site header border
    c.setFillColor(YELLOW)
    c.rect(0, 0, PAGE_W, BLEED + 0.06 * inch, stroke=0, fill=1)

    # QR block on the right
    qr_box = 1.3 * inch
    qx = PAGE_W - SAFE - qr_box
    qy = (PAGE_H - qr_box) / 2 + 0.04 * inch
    c.setFillColor("white")
    c.roundRect(qx, qy, qr_box, qr_box, 6, stroke=0, fill=1)
    pad = 0.1 * inch
    c.drawImage(qr_image(REVIEW_URL, NAVY_DEEP, "white"), qx + pad, qy + pad,
                qr_box - 2 * pad, qr_box - 2 * pad)

    # left column
    left_w = qx - SAFE - 0.18 * inch
    wordmark(c, SAFE, PAGE_H - SAFE - 0.2 * inch, 15, "white", YELLOW)

    c.setFillColor("white")
    c.setFont("Anton", 24)
    c.drawString(SAFE, PAGE_H / 2 + 0.1 * inch, "HAPPY WITH")
    c.drawString(SAFE, PAGE_H / 2 - 0.26 * inch, "THE WORK?")

    c.setFillColor(YELLOW)
    c.setFont("Barlow-XBold", 8.5)
    c.drawString(SAFE, SAFE + 0.26 * inch, "SCAN TO LEAVE A GOOGLE REVIEW")
    c.setFillColor("#C9D3E6")
    c.setFont("Barlow", 7.5)
    c.drawString(SAFE, SAFE + 0.1 * inch, "60 seconds. It's how a one-man shop grows.")


def back(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # check mark badge
    badge = 0.5 * inch
    bx, by = SAFE, PAGE_H - SAFE - badge
    c.setFillColor(NAVY)
    c.roundRect(bx, by, badge, badge, 7, stroke=0, fill=1)
    check_mark(c, bx, by, badge, YELLOW)

    c.setFillColor(NAVY)
    c.setFont("Anton", 17)
    c.drawString(bx + badge + 0.12 * inch, by + badge - 0.2 * inch, "THANK YOU")
    c.setFillColor(STEEL)
    c.setFont("Barlow", 8)
    c.drawString(bx + badge + 0.12 * inch, by + 0.08 * inch, "for trusting Diego with your home.")

    y = PAGE_H / 2 + 0.02 * inch
    c.setFillColor(INK)
    c.setFont("Barlow", 8)
    lines = [
        "A quick Google review helps the next homeowner",
        "find a painter who shows up and finishes the job.",
        "If anything isn't right, call first. Diego will fix it.",
    ]
    for i, line in enumerate(lines):
        c.drawString(SAFE, y - i * 0.15 * inch, line)

    c.setFillColor(RED)
    c.setFont("Anton", 14)
    c.drawString(SAFE, SAFE + 0.22 * inch, "(720) 295-5617")
    c.setFillColor(STEEL)
    c.setFont("Barlow-Bold", 7)
    c.drawString(SAFE, SAFE + 0.07 * inch, "Call or text  ·  donedealhandyman@outlook.com  ·  Veteran-owned  ·  Denver, CO")


c = canvas.Canvas(OUT, pagesize=(PAGE_W, PAGE_H))
c.setTitle("Done Deal review card")
front(c)
c.showPage()
back(c)
c.showPage()
c.save()
print("wrote", OUT, "for", REVIEW_URL)
