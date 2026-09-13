#!/usr/bin/env node
/*
 * Builds dist/standalone.html: one self-contained file with the CSS and JS inlined,
 * no service worker and no external references. Used for hosted previews where only
 * a single page can be served. Run: node build-standalone.js
 */
const fs = require('node:fs');
const path = require('node:path');

const dir = __dirname;
const read = (f) => fs.readFileSync(path.join(dir, f), 'utf8');

const html = read('index.html');
const css = read('styles.css');
const js = read('app.js');

const title = html.match(/<title>([\s\S]*?)<\/title>/)[1];
const body = html.match(/<body>([\s\S]*)<\/body>/)[1]
  .replace(/\s*<script src="app\.js"><\/script>/, '')
  .trimEnd();

const out = `<title>${title}</title>
<style>
${css.trim()}
</style>
${body}
<script>
// Single-file build: no service worker to register, so skip it and use the
// Notification constructor directly. Everything else is byte-identical to the app.
window.__NO_SW__ = true;
${js.trim()}
</script>
`;

fs.mkdirSync(path.join(dir, 'dist'), { recursive: true });
fs.writeFileSync(path.join(dir, 'dist', 'standalone.html'), out);
console.log(`dist/standalone.html  ${(Buffer.byteLength(out) / 1024).toFixed(1)} KB`);
