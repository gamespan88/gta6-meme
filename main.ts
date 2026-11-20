// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry is the X post itself; this program has exactly one job:
// copy POST.json from the repository root into the output directory,
// where the make.fun gate reads it. It prints nothing on success.
//
// Locally, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for the
// grader's /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const POST_FILE = "POST.json";

function main(): void {
  const source = join(process.env.MAKEFUN_BOT_DIR ?? "/bot", POST_FILE);
  const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const target = join(targetDir, POST_FILE);

  mkdirSync(targetDir, { recursive: true });
  copyFileSync(source, target);

  // Sanity check: a staged file that is missing or empty can only fail
  // the gate later, so fail loudly here instead.
  if (statSync(target).size === 0) {
    throw new Error(`${target} is empty after copying`);
  }
}

try {
  main();
} catch (err) {
  console.error(`gta6-meme: could not stage ${POST_FILE}: ${(err as Error).message}`);
  process.exit(1);
}
