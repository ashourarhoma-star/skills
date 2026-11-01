// Renders scene.html frame-by-frame with Playwright/Chromium.
// Usage:
//   node render.mjs frames <outDir> [fps=30] [scale=2] [worker=0] [workers=1]
//        -> JPEG sequence f0000.jpg… (scale 2 = 2160x3840 / 4K). Frames are split
//           round-robin across workers so several processes can run in parallel.
//   node render.mjs stills <outDir> t1,t2,...  -> PNG preview stills at 1080x1920
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  ({ chromium } = createRequire('/opt/node-tools/')('playwright'));
}

const here = dirname(fileURLToPath(import.meta.url));
const [mode = 'frames', outDir = 'frames', a3, a4, a5, a6] = process.argv.slice(2);
const DURATION = Number(process.env.DURATION ?? 20);
mkdirSync(outDir, { recursive: true });

const scale = mode === 'frames' ? Number(a4 ?? 2) : 1;
const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
await page.goto(pathToFileURL(join(here, 'scene.html')).href);
await page.evaluate(() => window.__ready);

const draw = (t, frame) => page.evaluate(([tt, f]) => window.renderFrame(tt, f), [t, frame]);

if (mode === 'stills') {
  const times = (a3 ?? '1,3,6,8.5,10.3,12.5,14.5').split(',').map(Number);
  for (const t of times) {
    await draw(t, 0);
    await page.screenshot({ path: join(outDir, `t${t.toFixed(2)}.png`), type: 'png' });
  }
} else {
  const fps = Number(a3 ?? 30);
  const worker = Number(a5 ?? 0);
  const workers = Number(a6 ?? 1);
  const total = Math.round(DURATION * fps);
  const t0 = Date.now();
  for (let i = worker; i < total; i += workers) {
    await draw(i / fps, i);
    await page.screenshot({ path: join(outDir, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 95 });
    if ((i - worker) % (30 * workers) === 0) console.log(`[w${worker}] frame ${i}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
}
await browser.close();
