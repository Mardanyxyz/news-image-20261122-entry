[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Mardanyxyz/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Mardanyxyz/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122)

# THE WORLD — Sunday 22 November 2026

A newspaper front page summing up the world news of Sunday 22 November 2026, drawn from scratch with Python (PIL) — no external images, no network. The lead story is the collapse of the COP31 climate talks in Antalya after 18 days and 48 hours of overtime, the longest summit ever, ending with no agreement after some 90 countries rejected a final draft that left out fossil fuels. The page also covers Ukraine sinking the Russian corvette Merkury at Benghazi, Russia's 186-drone barrage on Ukraine and the apartment block collapse in Dymer, the Gulf flashpoint as Iran struck US bases in Bahrain and claimed tanker mines off Hormuz, drone strikes on homes and a UN building in Khartoum, Carlos Alcaraz winning his first ATP Finals title in Turin, and the Democrats securing at least 258 US House seats — their largest majority since 1992.

## Build

```sh
python3 draw.py        # renders entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `entry.png` to the output directory; it resolves the image against the script's own directory, so it works from any working directory.

## License

MIT — see [LICENSE](LICENSE).
