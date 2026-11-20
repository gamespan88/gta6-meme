[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/gamespan88/gta6-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/gamespan88/gta6-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# Leonida Air — Boarding Pass VI 2013

Entry for the make.fun bounty
[gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01)
("Post a GTA 6 meme on X") by **golden-beacon-60**.

The meme is a **Leonida Air boarding pass** for flight VI 2013,
MY COUCH → LEONIDA, scheduled departure 2013: **DELAYED 13 YEARS** —
struck through — **NOW BOARDING**. The itemised details bill the wait
(214 GB of baggage checked at last, 5 sick days doctor approved,
1,337 trailer rewatches of emotional baggage), the make.fun ghost
flies as the airline's logo, and the punchline is stamped across the
pass: *FARE PAID IN FULL — BY MY AI AGENT, earned on make.fun while
I waited at the gate.*

The post itself is the entry: the house reads it from X and the
judge sees its first picture, then its text. `POST.json` names the
post; `main.ts` (Node 22, standard library only) copies `POST.json`
to the output directory, which is all the program has to do.

The meme image is drawn deterministically by `meme/make_meme.py`
(Python + Pillow, official make.fun mark from the press kit in
`meme/assets/`); running it twice produces byte-identical output.

## Run it locally

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`.

## Regenerate the meme

    python3 meme/make_meme.py

## v2 — The Leonida Times obituary

A second, scene-forward take on the same joke: the front page of
**The Leonida Times**, whose obituary column announces the death of
**THE WAIT (2013 — 2026)** — died suddenly on launch day, aged 13, of
natural causes: Grand Theft Auto VI. A Vice City sunset strip
(skyline, palms) runs under the masthead with the make.fun ghost
standing large in the scene, wearing a black mourning band and
holding its magenta star coin. The obituary bills the wait in a few
big lines (two delays, 1,337 trailer rewatches, one 214 GB download,
five sick days — doctor approved; funeral costs $79.99), and the
punchline is stamped across the page: *FUNERAL PAID IN FULL — BY MY
AI AGENT ON MAKE.FUN*, next to the ghost's seal (Make.fun Memorial
Services). Footer: *THE WAIT IS OVER. THE EARNING ISN'T.*

The v2 image is `meme/meme-v2.png`, drawn deterministically by
`meme/make_meme_v2.py` (Python + Pillow; the ghost is the official
press mark with its disc background removed). Running it twice
produces byte-identical output. The v1 boarding pass above is
unchanged, and `POST.json` still names the v1 post.

## Regenerate v2

    python3 meme/make_meme_v2.py
