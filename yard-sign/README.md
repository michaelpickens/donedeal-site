# Done Deal yard sign

Two-sided 24 x 18 in coroplast yard sign with H-stake. Face A goes up at every
active job site ("happening right here"); Face B is the roadside version. Both
carry the phone, the wordmark, and a QR to donedealhandyman.com.

`yard-sign.pdf` is two pages with 0.125 in bleed on every edge (page size
24.25 x 18.25 in). Order as double-sided, 4mm coroplast, "I have my own bleed",
page 1 = front, page 2 = back, H-stakes included. Rebuild after any copy change:

```
pip install reportlab qrcode pillow
python3 make_sign.py
```

Readability check: the phone number is about 3 in tall, which reads from
roughly 150 ft, or a car passing at neighborhood speed.
