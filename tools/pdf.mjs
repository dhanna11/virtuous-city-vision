// the PDF edition for now: every slide of the full deck, one per 1920x1080 page
import { chromium } from '../tests/node_modules/playwright/index.mjs';
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto(new URL('../preview-full.html', import.meta.url).href); await p.evaluate(() => document.fonts.ready);
await p.addStyleTag({ content: `html,body{height:auto!important;overflow:visible!important;display:block!important}
  .bar,.hint,.viewport>.note{display:none!important} .viewport{overflow:visible!important;display:block!important}
  .stage{position:relative!important;left:0!important;top:0!important;transform:none!important;visibility:visible!important;box-shadow:none!important;break-after:page;animation:none!important}
  .stage *{animation:none!important;opacity:1!important}` });
await p.pdf({ path: new URL('../virtuous-city-vision.pdf', import.meta.url).pathname, width: '1920px', height: '1080px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await b.close();
