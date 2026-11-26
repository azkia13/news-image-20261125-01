[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/azkia13/news-image-20261125-01/rank.svg)](https://make.fun/c/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/azkia13/news-image-20261125-01/reward.svg)](https://make.fun/c/news-image-20261125)

# The Day in the World — front page, 25 November 2026

A one-page newspaper front page summing up Wednesday 25 November 2026:
tankers hit by mines in the Strait of Hormuz (lead), Ukraine's strikes on
Russian refineries and an air base, the leaked Russian death toll, the
Houthi claim on Ras Tanura, Gaza, the Asia market plunge, Huawei's guilty
verdict, Pakistan's first astronaut, the Australia–Solomon Islands pact,
Pope Leo XIV on COP31 — plus a wire strip of the day's other news.

## How it works

`draw_front.py` draws `entry.png` (1024×1024) at build time with Pillow.
`main.py` — the graded entrypoint — only copies that finished image to
`/output/entry.png` using the standard library, so both graded runs write
byte-identical output.

```sh
python3 draw_front.py        # rebuild entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

Entry for the make.fun competition
[news-image-20261125](https://make.fun/c/news-image-20261125).
