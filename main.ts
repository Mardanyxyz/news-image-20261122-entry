// news-image-20261122 v3 — entry program.
//
// draw.py renders the front page into entry.png beside this file ahead of
// time. This program only copies that image into the grader's output
// directory, so it must work no matter which directory the grader runs
// it from: the image path is resolved from this file's own location.
//
// Local check:
//   python3 draw.py
//   cd /tmp && MAKEFUN_OUTPUT_DIR=/tmp/v3-check node \
//     ~/workspace/makefun/news-image-20261122-entry/main.ts

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

if (!existsSync(source)) {
  throw new Error(`entry.png missing next to main.ts: ${source}`);
}

const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(source, dest);
console.log(`entry.png -> ${dest}`);
