// Name: QiuCheng Zhen
// Nickname: HuangXiaoYunMeiMei WoXiHuanNi
// ID: 2400012917

'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { createRequire } = require('node:module');

const ROOT = path.resolve(__dirname, '..');
const FONT_SHA256 = 'f144137f557805c7327fc4b14d1d730f6e1822e0124170251ff1bcd723a693f1';
const FONT_FAMILY = 'WhiteBlueSourceCodePro';
const EXTRA_CHARACTERS = new Set('αβγδλμσπΣΠ∑∏∫∂∞√≤≥≠≈≡∩∀∃¬→←↔⇒×÷±');
const OUTPUT_NAMES = ['symbols-text.svg', 'symbols-outlined.svg', 'symbols.png', 'preview.png', 'master.svg', 'report.json'];
const PNG_OPTIONS = { compressionLevel: 9, adaptiveFiltering: false, palette: false, effort: 10 };

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function escapeXml(value) {
  return String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' })[character]);
}

function parseArguments(args) {
  const options = {
    sourceDir: path.join(ROOT, 'designs', '03-white-blue-code', 'source', 'symbols'),
    outputDir: path.join(ROOT, 'generated', 'white-blue-symbols'),
    force: false,
    help: false,
  };
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === '--force') options.force = true;
    else if (arg === '--help' || arg === '-h') options.help = true;
    else if (arg === '--source-dir' || arg === '--output-dir') {
      const next = args[++index];
      assert(next && !next.startsWith('--'), `Missing value for ${arg}`);
      options[arg === '--source-dir' ? 'sourceDir' : 'outputDir'] = path.resolve(next);
    } else throw new Error(`Unknown argument: ${arg}`);
  }
  return options;
}

function sourcePath(sourceDir, relative, label) {
  assert(typeof relative === 'string' && relative.length > 0 && !path.isAbsolute(relative), `${label} must be a relative path`);
  const target = path.resolve(sourceDir, relative);
  const normalized = path.relative(sourceDir, target);
  assert(normalized && !normalized.startsWith('..') && !path.isAbsolute(normalized), `${label} must remain inside the source directory`);
  return target;
}

// Read the bundled font's Unicode cmap directly so missing characters never use a fallback font.
function characterMapper(font) {
  const tableCount = font.readUInt16BE(4);
  let cmapOffset;
  for (let index = 0; index < tableCount; index += 1) {
    const offset = 12 + index * 16;
    if (font.toString('ascii', offset, offset + 4) === 'cmap') cmapOffset = font.readUInt32BE(offset + 8);
  }
  assert(cmapOffset !== undefined, 'The pinned font has no cmap table');
  const maps = [];
  const mapCount = font.readUInt16BE(cmapOffset + 2);
  for (let index = 0; index < mapCount; index += 1) {
    const record = cmapOffset + 4 + index * 8;
    const platform = font.readUInt16BE(record);
    const encoding = font.readUInt16BE(record + 2);
    if (platform !== 0 && !(platform === 3 && [1, 10].includes(encoding))) continue;
    const offset = cmapOffset + font.readUInt32BE(record + 4);
    const format = font.readUInt16BE(offset);
    if (format === 4 || format === 12) maps.push({ offset, format });
  }
  assert(maps.length > 0, 'The pinned font has no supported Unicode cmap');
  return codePoint => maps.some(({ offset, format }) => {
    if (format === 12) {
      const count = font.readUInt32BE(offset + 12);
      for (let index = 0; index < count; index += 1) {
        const group = offset + 16 + index * 12;
        const start = font.readUInt32BE(group);
        const end = font.readUInt32BE(group + 4);
        if (codePoint >= start && codePoint <= end) return font.readUInt32BE(group + 8) + codePoint - start !== 0;
      }
      return false;
    }
    if (codePoint > 0xffff) return false;
    const segments = font.readUInt16BE(offset + 6) / 2;
    const endCodes = offset + 14;
    const startCodes = endCodes + segments * 2 + 2;
    const deltas = startCodes + segments * 2;
    const rangeOffsets = deltas + segments * 2;
    for (let index = 0; index < segments; index += 1) {
      const start = font.readUInt16BE(startCodes + index * 2);
      const end = font.readUInt16BE(endCodes + index * 2);
      if (codePoint < start || codePoint > end) continue;
      const delta = font.readInt16BE(deltas + index * 2);
      const rangePosition = rangeOffsets + index * 2;
      const range = font.readUInt16BE(rangePosition);
      if (range === 0) return ((codePoint + delta) & 0xffff) !== 0;
      const glyph = font.readUInt16BE(rangePosition + range + (codePoint - start) * 2);
      return glyph !== 0 && ((glyph + delta) & 0xffff) !== 0;
    }
    return false;
  });
}

function validateLayout(layout, hasCharacter) {
  assert(layout.width === 1536 && layout.height === 1024, 'The master canvas must remain 1536 x 1024');
  assert(layout.clipPaths && typeof layout.clipPaths === 'object' && !Array.isArray(layout.clipPaths), 'clipPaths must be an object');
  assert(Array.isArray(layout.items) && layout.items.length > 0, 'items must be a non-empty array');
  const safeId = /^[A-Za-z_][A-Za-z0-9_.-]*$/;
  for (const [id, data] of Object.entries(layout.clipPaths)) {
    assert(safeId.test(id) && typeof data === 'string' && data.trim(), `Invalid clip path: ${id}`);
    assert(/^[MmLlHhVvCcSsQqTtAaZz0-9eE+.,\s-]+$/.test(data), `Invalid SVG path data in clip: ${id}`);
  }
  const ids = new Set();
  const characters = new Set();
  for (const item of layout.items) {
    assert(typeof item.id === 'string' && safeId.test(item.id) && !ids.has(item.id), `Invalid or duplicate item id: ${item.id}`);
    ids.add(item.id);
    assert(typeof item.text === 'string' && item.text.trim().length > 0, `Missing text in ${item.id}`);
    assert(typeof item.clip === 'string' && Object.hasOwn(layout.clipPaths, item.clip), `Unknown clip in ${item.id}`);
    assert(/^#[0-9a-f]{6}$/i.test(item.fill), `Use a six-digit hexadecimal fill in ${item.id}`);
    for (const field of ['x', 'y', 'fontSize', 'opacity']) assert(Number.isFinite(item[field]), `Invalid ${field} in ${item.id}`);
    assert(item.fontSize > 0 && item.fontSize <= 300, `fontSize outside (0, 300] in ${item.id}`);
    assert(item.opacity >= 0 && item.opacity <= 1, `opacity outside [0, 1] in ${item.id}`);
    assert(Number.isFinite(item.strokeWidth ?? 0) && (item.strokeWidth ?? 0) >= 0 && (item.strokeWidth ?? 0) <= 1.5, `strokeWidth outside [0, 1.5] in ${item.id}`);
    assert(Number.isFinite(item.rotate ?? 0), `Invalid rotate in ${item.id}`);
    assert(Number.isFinite(item.scaleX ?? 1) && (item.scaleX ?? 1) > 0, `Invalid scaleX in ${item.id}`);
    for (const character of item.text) {
      const codePoint = character.codePointAt(0);
      assert((codePoint >= 32 && codePoint <= 126) || EXTRA_CHARACTERS.has(character), `Unsupported character ${JSON.stringify(character)} in ${item.id}`);
      assert(hasCharacter(codePoint), `The pinned font lacks U+${codePoint.toString(16).toUpperCase()} in ${item.id}; fallback is disabled`);
      characters.add(character);
    }
  }
  return [...characters].sort((a, b) => a.codePointAt(0) - b.codePointAt(0));
}

function makeTextSvg(layout, font) {
  const clips = Object.entries(layout.clipPaths).map(([id, data]) => `<clipPath id="clip-${id}" clipPathUnits="userSpaceOnUse"><path d="${escapeXml(data)}"/></clipPath>`).join('\n');
  const items = layout.items.map(item => {
    const transform = `translate(${item.x} ${item.y}) rotate(${item.rotate ?? 0}) scale(${item.scaleX ?? 1} 1)`;
    return `<g id="item-${item.id}" clip-path="url(#clip-${item.clip})" opacity="${item.opacity}"><text transform="${transform}" x="0" y="0" font-family="${FONT_FAMILY}" font-size="${item.fontSize}" font-weight="400" font-style="normal" font-kerning="none" fill="${item.fill}" stroke="${item.fill}" stroke-width="${item.strokeWidth ?? 0}" paint-order="stroke fill" xml:space="preserve">${escapeXml(item.text)}</text></g>`;
  }).join('\n');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${layout.width}" height="${layout.height}" viewBox="0 0 ${layout.width} ${layout.height}">
<title>White-blue shirt: fixed editable symbol layout</title>
<metadata>${escapeXml(JSON.stringify(layout.metadata ?? {}))}</metadata>
<defs><style>@font-face{font-family:'${FONT_FAMILY}';src:url(data:font/ttf;base64,${font.toString('base64')}) format('truetype');font-weight:400;font-style:normal;}text{font-variant-ligatures:none;font-feature-settings:'liga' 0,'calt' 0;}</style>
${clips}</defs>
${items}
</svg>\n`;
}

function makeOutlinedSvg(layout, canvas) {
  const clips = Object.entries(layout.clipPaths).map(([id, data]) => `<clipPath id="clip-${id}" clipPathUnits="userSpaceOnUse"><path d="${escapeXml(data)}"/></clipPath>`).join('\n');
  const glyphCache = new Map();
  const glyphs = [];
  const items = layout.items.map(item => {
    const strokeWidth = item.strokeWidth ?? 0;
    const key = JSON.stringify([item.text, item.fontSize, strokeWidth]);
    let glyphId = glyphCache.get(key);
    if (!glyphId) {
      glyphId = `glyph-${glyphCache.size}`;
      const padding = item.fontSize * 2;
      const width = item.fontSize * (item.text.length + 4) * 2;
      const height = item.fontSize * 4;
      // The native SVG exporter drops translucent text. Outline opaque glyphs first;
      // preserve opacity, clipping and positioning in our own outer SVG groups.
      const text = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}"><text x="${padding}" y="${padding}" font-family="${FONT_FAMILY}" font-size="${item.fontSize}" font-weight="400" font-style="normal" font-kerning="none" fill="#010203" stroke="#010203" stroke-width="${strokeWidth}" paint-order="stroke fill" xml:space="preserve">${escapeXml(item.text)}</text></svg>`;
      const outlined = canvas.convertSVGTextToPath(text).toString('utf8');
      const inner = outlined.match(/<svg\b[^>]*>([\s\S]*)<\/svg>/i)?.[1];
      assert(inner && /<path\b/.test(inner) && !/<text\b/.test(inner), `Failed to outline ${item.id}`);
      assert(strokeWidth === 0 || /\bstroke=/.test(inner), `Text-to-path conversion discarded the stroke for ${item.id}`);
      glyphs.push(`<g id="${glyphId}" transform="translate(${-padding} ${-padding})">${inner.replace(/#010203/gi, 'currentColor')}</g>`);
      glyphCache.set(key, glyphId);
    }
    const transform = `translate(${item.x} ${item.y}) rotate(${item.rotate ?? 0}) scale(${item.scaleX ?? 1} 1)`;
    return `<g id="item-${item.id}" clip-path="url(#clip-${item.clip})" opacity="${item.opacity}" color="${item.fill}"><use href="#${glyphId}" transform="${transform}"/></g>`;
  }).join('\n');
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${layout.width}" height="${layout.height}" viewBox="0 0 ${layout.width} ${layout.height}">
<title>White-blue shirt: fixed outlined symbol layout</title>
<defs>${clips}\n${glyphs.join('\n')}</defs>
${items}
</svg>\n`);
}

async function main() {
  const options = parseArguments(process.argv.slice(2));
  if (options.help) {
    console.log('Usage: node scripts/render-white-blue.cjs [--source-dir DIR] [--output-dir DIR] [--force]\nInstall dependencies: npm install --prefix scripts/white-blue-renderer\nExisting outputs are protected unless --force is supplied.');
    return;
  }
  const outputRelativeToSource = path.relative(options.sourceDir, options.outputDir);
  assert(outputRelativeToSource && (outputRelativeToSource === '..' || outputRelativeToSource.startsWith(`..${path.sep}`) || path.isAbsolute(outputRelativeToSource)), 'Output directory must not be the source directory or one of its descendants, even with --force');
  for (const name of OUTPUT_NAMES) assert(options.force || !fs.existsSync(path.join(options.outputDir, name)), `Output already exists: ${path.join(options.outputDir, name)}; use --force to replace generated outputs`);
  const localRequire = createRequire(path.join(__dirname, 'white-blue-renderer', 'package.json'));
  let canvas;
  let sharp;
  let canvasVersion;
  try {
    canvas = localRequire('@napi-rs/canvas');
    sharp = localRequire('sharp');
    canvasVersion = localRequire('@napi-rs/canvas/package.json').version;
  } catch (error) {
    throw new Error(`Renderer dependencies are unavailable. Run npm install --prefix scripts/white-blue-renderer, or set NODE_PATH to the bundled node_modules directory. ${error.message}`);
  }
  assert(canvasVersion === '0.1.100' && sharp.versions.sharp === '0.35.5', `Dependency versions differ from the pinned renderer: canvas=${canvasVersion}, sharp=${sharp.versions.sharp}`);
  const layoutBytes = fs.readFileSync(path.join(options.sourceDir, 'symbols-layout.json'));
  const layout = JSON.parse(layoutBytes.toString('utf8').replace(/^\uFEFF/, ''));
  const font = fs.readFileSync(sourcePath(options.sourceDir, layout.font, 'font'));
  assert(sha256(font) === FONT_SHA256, 'Font SHA-256 differs from the pinned Source Code Pro Regular 2.038');
  const characters = validateLayout(layout, characterMapper(font));
  const background = fs.readFileSync(sourcePath(options.sourceDir, layout.background, 'background'));
  const backgroundMetadata = await sharp(background).metadata();
  assert(backgroundMetadata.format === 'png' && backgroundMetadata.width === layout.width && backgroundMetadata.height === layout.height, 'Background must be a 1536 x 1024 PNG');
  let lettering = null;
  if (layout.lettering != null) {
    lettering = fs.readFileSync(sourcePath(options.sourceDir, layout.lettering, 'lettering'));
    const letteringMetadata = await sharp(lettering).metadata();
    assert(letteringMetadata.format === 'png' && letteringMetadata.width === layout.width && letteringMetadata.height === layout.height && letteringMetadata.hasAlpha, 'Lettering must be a 1536 x 1024 PNG with an alpha channel');
  }
  assert(canvas.GlobalFonts.register(font, FONT_FAMILY), 'Could not register the pinned font');
  const textSvg = Buffer.from(makeTextSvg(layout, font));
  const outlinedSvg = makeOutlinedSvg(layout, canvas);
  assert(!/<text(?:\s|>)/i.test(outlinedSvg.toString('utf8')), 'Text-to-path conversion left unconverted text');
  assert(/<clipPath(?:\s|>)/i.test(outlinedSvg.toString('utf8')), 'Text-to-path conversion discarded clipping definitions');
  const outlinedItemCount = (outlinedSvg.toString('utf8').match(/\bid="item-/g) ?? []).length;
  assert(outlinedItemCount === layout.items.length, 'Text-to-path conversion did not preserve every layout item');
  const symbols = await sharp(outlinedSvg, { density: 72 }).png(PNG_OPTIONS).toBuffer();
  const symbolMetadata = await sharp(symbols).metadata();
  assert(symbolMetadata.width === layout.width && symbolMetadata.height === layout.height && symbolMetadata.hasAlpha, 'Symbol layer dimensions or transparency changed');
  const compositeLayers = [{ input: symbols, left: 0, top: 0 }];
  if (lettering) compositeLayers.push({ input: lettering, left: 0, top: 0 });
  const preview = await sharp(background).composite(compositeLayers).png(PNG_OPTIONS).toBuffer();
  const outlinedContent = outlinedSvg.toString('utf8').replace(/^\s*<\?xml[^?]*\?>\s*/i, '');
  const letteringLayer = lettering ? `<image id="lettering" x="0" y="0" width="${layout.width}" height="${layout.height}" href="data:image/png;base64,${lettering.toString('base64')}"/>\n` : '';
  const master = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${layout.width}" height="${layout.height}" viewBox="0 0 ${layout.width} ${layout.height}">
<title>White-blue shirt master: embedded garment, outlined symbols${lettering ? ' and lettering' : ''}</title>
<image id="blank-garment" x="0" y="0" width="${layout.width}" height="${layout.height}" href="data:image/png;base64,${background.toString('base64')}"/>
<g id="outlined-symbols">${outlinedContent}</g>
${letteringLayer}</svg>\n`);
  const outputs = { 'symbols-text.svg': textSvg, 'symbols-outlined.svg': outlinedSvg, 'symbols.png': symbols, 'preview.png': preview, 'master.svg': master };
  const report = {
    schemaVersion: 1,
    width: layout.width,
    height: layout.height,
    itemCount: layout.items.length,
    outlinedItemCount,
    strokedItemCount: layout.items.filter(item => (item.strokeWidth ?? 0) > 0).length,
    uniqueTextCount: new Set(layout.items.map(item => item.text)).size,
    uniqueCharacterCount: characters.length,
    characters: characters.join(''),
    fontFamily: 'Source Code Pro Regular',
    fontVersion: '2.038',
    fontSha256: sha256(font),
    layoutSha256: sha256(layoutBytes),
    backgroundSha256: sha256(background),
    letteringSha256: lettering ? sha256(lettering) : null,
    runtime: { node: process.version, platform: process.platform, arch: process.arch, canvas: canvasVersion, sharp: sharp.versions },
    pngOptions: PNG_OPTIONS,
    svgDensity: 72,
    outputSha256: Object.fromEntries(Object.entries(outputs).map(([name, value]) => [name, sha256(value)])),
    reproducibility: 'No random placement. Code symbols are fixed outlines; optional lettering retains its stored pixels. PNG byte identity requires matching the recorded renderer/runtime versions.',
  };
  outputs['report.json'] = Buffer.from(`${JSON.stringify(report, null, 2)}\n`);
  fs.mkdirSync(options.outputDir, { recursive: true });
  for (const [name, value] of Object.entries(outputs)) fs.writeFileSync(path.join(options.outputDir, name), value, { flag: options.force ? 'w' : 'wx' });
  console.log(`Rendered ${layout.items.length} fixed text items (${characters.length} unique characters) to ${options.outputDir}`);
  console.log(`Preview SHA-256: ${report.outputSha256['preview.png']}`);
}

main().catch(error => {
  console.error(`White-blue render failed: ${error.message}`);
  process.exitCode = 1;
});
