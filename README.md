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
