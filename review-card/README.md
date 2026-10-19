# Done Deal review system

Two pieces: a text Diego sends after every job, and a card he leaves behind.
Both point at the same Google review link.

## 1. Get the review link (once)

In the Google Business Profile (business.google.com), open the profile,
click **Ask for reviews**, and copy the short link. It looks like
`https://g.page/r/XXXXXXXXXXXX/review`. Paste it into the text template
below and run the card script with it.

## 2. Review request text

Diego sends this from his phone the same day the job wraps, while it is still
fresh. One text, no follow-up chasing. Replace the two bracketed bits.

**Standard**

> Hey [first name], thanks again for having me out. Really happy with how the
> [room / floors / cabinets] turned out. If you've got 60 seconds, a quick
> Google review goes a long way for a one-man shop like mine:
> [review link]
> Diego, Done Deal Painting & Floors

**Shorter, for repeat or referral customers**

> [First name], thanks again. If you're happy with the work, a Google review
> would mean a lot: [review link]
> Diego

**If a few days go by and nothing posts (send once, then let it go)**

> Hey [first name], no pressure at all, just making sure the link came
> through: [review link]. Thanks for the work either way.

Tips that matter more than the wording:

- Send it the day the job finishes. Response rate drops by half after 48 hours.
- Say what the job was. A review that mentions "LVP in the basement" is worth
  more to search than "great guy".
- Never offer a discount for a review. Google removes them and can suspend the
  profile.
- If a customer is unhappy, do not send the link. Fix the job first.

## 3. Leave-behind card

`review-card.pdf` is a 3.5 x 2 in business card, two sides, with 0.125 in
bleed on every edge (page size 3.75 x 2.25 in). Upload it to any card printer
and choose the "I have my own bleed" or "full bleed" option. 250 cards from an
online printer runs about $20 to $40.

Front: "Happy with the work?" with the QR code. Back: thank-you, phone, email.

To regenerate with the real link (or after any copy change):

```
pip install reportlab qrcode pillow
python3 make_card.py "https://g.page/r/XXXXXXXXXXXX/review"
```

The file in this folder was built with a placeholder link. Do not print it
until it has been rebuilt with the real one.
