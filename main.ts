// news-image-20261122 v2 entry point.
//
// The front page is rendered ahead of time by draw.py into entry.png
// next to this file. This program only delivers that image to the
// grader's output directory.
//
// Usage (local check):
//   python3 draw.py
//   cd /tmp && MAKEFUN_OUTPUT_DIR=/tmp/check-out node \
//     ~/workspace/makefun/news-image-20261122-entry/main.ts
// The image path is resolved from this file's own directory, never
// from the process working directory, so the grader may invoke it
// from anywhere.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(scriptDir, "entry.png");

if (!existsSync(sourceImage)) {
  throw new Error(`entry.png not found beside main.ts: ${sourceImage}`);
}

const targetDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
mkdirSync(targetDir, { recursive: true });
copyFileSync(sourceImage, join(targetDir, "entry.png"));
console.log(`entry.png -> ${join(targetDir, "entry.png")}`);
