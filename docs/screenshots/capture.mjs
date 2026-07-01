// Portfolio-screenshot capture. Uses puppeteer-core against the
// locally-installed Chrome so we don't need to bundle a ~200MB
// chromium download.
//
// Prereqs:
//   • Chrome installed at the standard macOS path
//   • Preview or dev server running at the URL below
//   • `npm i --no-save puppeteer-core` (from anywhere)
//
// Run:  node docs/screenshots/capture.mjs

import puppeteer from 'puppeteer-core';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const URL = process.env.SITE_URL ?? 'http://localhost:5199/';
const OUT = new URL('.', import.meta.url).pathname;

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

// Small helper: nudge a slider via bind:value by dispatching an input event
const setSliderScript = () => {
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  window.__setSlider = (id, value) => {
    const el = document.getElementById(id);
    if (!el) return;
    setter.call(el, value);
    el.dispatchEvent(new Event('input', { bubbles: true }));
  };
};

try {
  // ── 01. Hero ────────────────────────────────────────────
  {
    const page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
    await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.screenshot({ path: `${OUT}/01-hero.png` });
    await page.close();
    console.log('01-hero.png');
  }

  // ── 02. MapMoves — Georgia drilled in ──────────────────
  {
    const page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 1500, deviceScaleFactor: 2 });
    await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.evaluate(() => {
      document.getElementById('map-moves-h')?.scrollIntoView({ behavior: 'instant', block: 'start' });
      window.scrollBy(0, -60);
    });
    await new Promise(r => setTimeout(r, 500));
    await page.evaluate(() => {
      const heads = [...document.querySelectorAll('.state-head')];
      heads.find(h => h.textContent.includes('Georgia'))?.click();
    });
    await new Promise(r => setTimeout(r, 1500));  // let topojson + county paths render
    await page.evaluate(() => {
      const expanded = document.querySelector('.state-row.expanded');
      if (expanded) {
        expanded.scrollIntoView({ behavior: 'instant', block: 'start' });
        window.scrollBy(0, -140);
      }
    });
    await new Promise(r => setTimeout(r, 500));
    await page.screenshot({ path: `${OUT}/02-mapmoves.png` });
    await page.close();
    console.log('02-mapmoves.png');
  }

  // ── 03. MoversBudget — NC flipped, choropleth coloured ─
  {
    const page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 1400, deviceScaleFactor: 2 });
    await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.evaluate(() => {
      document.getElementById('mb-title')?.scrollIntoView({ behavior: 'instant', block: 'start' });
      window.scrollBy(0, -60);
    });
    await new Promise(r => setTimeout(r, 500));
    await page.evaluate(setSliderScript);
    await page.evaluate(() => {
      __setSlider('alloc-NC', 100000);   // flips NC from R to D
      __setSlider('alloc-GA', 25000);
      __setSlider('alloc-AZ', 20000);
      __setSlider('alloc-PA', 40000);
      __setSlider('alloc-MI', 30000);
    });
    await new Promise(r => setTimeout(r, 1200));
    await page.evaluate(() => {
      document.querySelector('.impact-title')?.scrollIntoView({ behavior: 'instant', block: 'start' });
      window.scrollBy(0, -80);
    });
    await new Promise(r => setTimeout(r, 800));
    await page.screenshot({ path: `${OUT}/03-moversbudget.png` });
    await page.close();
    console.log('03-moversbudget.png');
  }
} finally {
  await browser.close();
}
