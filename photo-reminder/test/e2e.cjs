/* End-to-end smoke test: real UI, fake clock, fake GPS. Requires a static server on :8765 and Playwright. */
const path = require('node:path');
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

const BASE = process.env.BASE || 'http://127.0.0.1:8765/';
const HOME = { latitude: 37.7749, longitude: -122.4194 };
const PNG_1x1 = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==', 'base64');

function assert(cond, msg) { if (!cond) throw new Error('ASSERT: ' + msg); console.log('  ✓', msg); }

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: 400, height: 800 }, isMobile: true, hasTouch: true,
    permissions: ['geolocation', 'notifications'], geolocation: { ...HOME, accuracy: 20 },
  });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

  await page.clock.install();
  await page.goto(BASE);
  await page.waitForFunction(() => window.DontForget);
  assert(await page.isVisible('#empty-state'), 'empty state shown on first load');

  // ---- 1. timer reminder ----
  await page.click('#btn-new');
  await page.setInputFiles('#photo-input', { name: 'jacket.png', mimeType: 'image/png', buffer: PNG_1x1 });
  await page.waitForSelector('#photo-preview-wrap:not([hidden])');
  await page.fill('#label-input', 'jacket');
  await page.click('.preset[data-id="hi"]');           // 30 min
  assert(!(await page.isDisabled('#btn-save')), 'save enabled after photo');
  await page.click('#btn-save');
  await page.waitForSelector('.rem');
  assert((await page.textContent('.rem-title')).includes('jacket'), 'reminder card shows label');
  assert((await page.textContent('.countdown')).includes('in 30 min'), 'countdown starts at 30 min');

  await page.clock.fastForward('20:00');
  await page.clock.runFor(6000);
  assert((await page.textContent('.countdown')).includes('in 10 min'), 'countdown updates after 20 min');
  assert(await page.isHidden('#alert'), 'no alert before due time');

  await page.clock.fastForward('11:00');
  await page.clock.runFor(6000);
  await page.waitForSelector('#alert:not([hidden])');
  assert((await page.textContent('#alert-title')).includes("Don't forget your jacket"), 'alert fires after 31 min with label');
  assert((await page.getAttribute('#alert-photo', 'src')).startsWith('blob:'), 'alert shows the photo');
  assert((await page.textContent('#alert-kicker')).includes("Time's up"), 'alert reason is timer');

  await page.click('#btn-snooze-5');
  await page.waitForSelector('#alert', { state: 'hidden' });
  assert((await page.textContent('.countdown')).includes('in 5 min'), 'snooze 5 resets countdown');
  await page.clock.fastForward('06:00');
  await page.clock.runFor(6000);
  await page.waitForSelector('#alert:not([hidden])');
  await page.click('#btn-alert-done');
  await page.waitForSelector('#alert', { state: 'hidden' });
  assert((await page.$$('#list-active .rem')).length === 0, 'done removes from active list');
  assert((await page.textContent('#past-count')) === '1', 'done reminder moves to past');

  // ---- 2. geofence reminder ----
  await page.click('#btn-new');
  await page.setInputFiles('#photo-input', { name: 'umbrella.png', mimeType: 'image/png', buffer: PNG_1x1 });
  await page.waitForSelector('#photo-preview-wrap:not([hidden])');
  await page.fill('#label-input', 'umbrella');
  await page.click('.preset[data-id="show"]');         // 2.5 h – far away, so only the geofence can fire
  await page.check('#geo-toggle');
  await page.waitForFunction(() => document.getElementById('geo-pin-status').textContent.includes('Pinned'));
  assert(true, 'location pinned');
  await page.click('#btn-save');
  await page.waitForSelector('#geo-status:not([hidden])');
  assert(true, 'geo watch active');

  // Still nearby (30 m): must not fire.
  await ctx.setGeolocation({ latitude: HOME.latitude + 0.00027, longitude: HOME.longitude, accuracy: 20 });
  await page.clock.runFor(2000);
  await ctx.setGeolocation({ latitude: HOME.latitude + 0.00028, longitude: HOME.longitude, accuracy: 20 });
  await page.clock.runFor(2000);
  assert(await page.isHidden('#alert'), 'no alert while within 100 m');

  // One far fix only: must not fire (GPS jump filter).
  await ctx.setGeolocation({ latitude: HOME.latitude + 0.0045, longitude: HOME.longitude, accuracy: 20 });
  await page.clock.runFor(2000);
  assert(await page.isHidden('#alert'), 'single far GPS fix is ignored');

  // Second consecutive far fix: fire.
  await ctx.setGeolocation({ latitude: HOME.latitude + 0.0046, longitude: HOME.longitude, accuracy: 20 });
  await page.waitForSelector('#alert:not([hidden])', { timeout: 5000 });
  assert((await page.textContent('#alert-kicker')).includes('leaving'), 'geofence alert fires after leaving');
  assert((await page.textContent('#alert-title')).includes('umbrella'), 'geofence alert names the item');
  await page.click('#btn-alert-done');
  await page.waitForSelector('#alert', { state: 'hidden' });
  await page.waitForFunction(() => document.getElementById('past-count').textContent === '2');
  assert(await page.isHidden('#geo-status'), 'geo watch stops when nothing needs it');

  // ---- 3. persistence across reload ----
  await page.reload();
  await page.waitForFunction(() => window.DontForget);
  const list = await page.evaluate(() => window.DontForget.list().map((r) => ({ label: r.label, status: r.status })));
  assert(list.length === 2 && list.every((r) => r.status === 'done'), 'reminders persist in IndexedDB across reload: ' + JSON.stringify(list));

  assert(errors.length === 0, 'no console/page errors: ' + JSON.stringify(errors));
  await page.screenshot({ path: path.join(process.env.SHOT_DIR || '.', 'e2e-final.png') });
  await browser.close();
  console.log('ALL PASSED');
})().catch((e) => { console.error(e); process.exit(1); });
