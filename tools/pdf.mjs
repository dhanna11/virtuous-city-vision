// the PDF edition for now: every slide of the full deck, one per 1920x1080 page
import { chromium } from '../tests/node_modules/playwright/index.mjs';
import { execFileSync } from 'node:child_process';
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
// Google Fonts through curl: in a sandbox whose proxy the browser can't verify, the page would otherwise print in fallback
// fonts, and the Arabic and Hebrew as empty boxes
await p.route(/fonts\.(googleapis|gstatic)\.com/, r => {
  const u = r.request().url();
  const body = execFileSync('curl', ['-sS', '-A', 'Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36', u], { maxBuffer: 1 << 26 });
  r.fulfill({ body, contentType: u.includes('googleapis') ? 'text/css' : 'font/woff2', headers: { 'access-control-allow-origin': '*' } });
});
await p.goto(new URL('../preview-full.html', import.meta.url).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1000);
await p.addStyleTag({ content: `html,body{height:auto!important;overflow:visible!important;display:block!important}
  .bar,.hint,.viewport>.note{display:none!important} .viewport{overflow:visible!important;display:block!important}
  .stage{position:relative!important;left:0!important;top:0!important;transform:none!important;visibility:visible!important;box-shadow:none!important;break-after:page;animation:none!important}
  .stage *{animation:none!important;opacity:1!important}` });
await p.pdf({ path: new URL('../virtuous-city-vision.pdf', import.meta.url).pathname, width: '1920px', height: '1080px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await b.close();
