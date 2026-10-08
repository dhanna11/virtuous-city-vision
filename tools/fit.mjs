// measures every slide of preview.html and preview-full.html; prints JSON {id: overflowPx} for slides whose flow content
// leaves the safe box (top 100, bottom 940 so it clears the footer line, sides 120)
import { chromium } from '../tests/node_modules/playwright/index.mjs';
const b = await chromium.launch(); const out = {};
for (const f of ['preview.html', 'preview-full.html']) {
  const p = await b.newPage({ viewport: { width: 1920, height: 1200 } });
  await p.goto(new URL('../' + f, import.meta.url).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  Object.assign(out, await p.evaluate(() => { const r = {};
    for (const sec of document.querySelectorAll('.stage section')) {
      const box = sec.getBoundingClientRect(), k = box.width / 1920; let worst = 0;
      for (const el of sec.querySelectorAll('*')) {
        { let a = el, abs = false; while (a && a !== sec) { if (getComputedStyle(a).position === 'absolute') abs = true; a = a.parentElement; } if (abs) continue; }
        const q = el.getBoundingClientRect(); if (!q.width || !q.height) continue;
        const t = (q.top - box.top) / k, bt = (q.bottom - box.top) / k, l = (q.left - box.left) / k, rt = (q.right - box.left) / k;
        const w = Math.max(bt - 940, 100 - t, 120 - l, rt - 1800); if (w > worst) { worst = w; r[sec.id + ":el"] = el.tagName + " " + [t, bt, l, rt].map(Math.round).join(","); }
      }
      if (worst > 0) r[sec.id] = Math.round(worst);
    } return r; }));
}
console.log(JSON.stringify(out)); await b.close();
