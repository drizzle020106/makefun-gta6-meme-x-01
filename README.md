# Called in sick. My agent called in rich.

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/drizzle020106/makefun-gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/drizzle020106/makefun-gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 launch-week meme for the make.fun bounty
[gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01).

## The joke

Launch day, GTA 6 is finally out after 13 years. I called in sick to play
it. My AI agent called in rich instead: while I play, it earns real money
in make.fun bounties.

- Top half: me in bed, controller in hand, texting the boss "sick. very sick."
- Bottom half: make.fun's ghost, coin in hand, on a magenta disc —
  "MY AGENT CALLED IN RICH. earning on make.fun while I play GTA 6".

## The files

- `meme-b.png` — the meme that goes on X (1024×1024, drawn from scratch
  with Pillow in `draw.py`: no photos, no downloaded art, no Rockstar assets).
- `meme-a.png` — backup meme: the ghost driving into a Vice City sunset,
  "WAITED 13 YEARS. FINALLY IN VICE CITY."
- `draw.py` — the drawing program that made both memes.
- `POST.json` — the X post's address (filled in once the meme is posted).
- `POST-TEXT.txt` — the exact text posted with the meme.
- `main.ts` — copies `POST.json` to the output directory for the grader.

## The post

The meme is posted on X from a public account with the text in
`POST-TEXT.txt`: a link to make.fun, a tag of @makefunai, and the account's
make.fun play code. The post itself is the entry: the house reads it from X
and an AI judge compares it pairwise with the other memes.

Owner: drizzle020106.
