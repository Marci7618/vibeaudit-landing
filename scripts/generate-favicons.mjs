/**
 * Generates landing favicon assets from vibeaudit-symbol-source.png (official symbol, no text).
 * Run from repo root: node scripts/generate-favicons.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const sharp = require(path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../vibeaudit/node_modules/sharp",
));

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const SOURCE = path.join(ROOT, "vibeaudit-symbol-source.png");

const SIZES = [
  ["favicon.png", 32],
  ["favicon-48.png", 48],
  ["favicon-96.png", 96],
  ["apple-touch-icon.png", 180],
  ["vibeaudit-symbol-512.png", 512],
];

async function symbolPipelineFromSource() {
  const { data, info } = await sharp(SOURCE)
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

  const { width, height, channels } = info;
  const px = channels;
  for (let i = 0; i < data.length; i += px) {
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];
    if (r <= 28 && g <= 28 && b <= 28) {
      data[i + 3] = 0;
    }
  }

  const trimmedBuf = await sharp(data, { raw: { width, height, channels } })
    .trim()
    .png()
    .toBuffer();

  const meta = await sharp(trimmedBuf).metadata();
  const w = meta.width ?? 1;
  const h = meta.height ?? 1;
  const maxSide = Math.max(w, h);
  const pad = Math.max(2, Math.round(maxSide * 0.03));

  const fitted = await sharp(trimmedBuf)
    .resize(maxSide, maxSide, {
      fit: "contain",
      background: { r: 0, g: 0, b: 0, alpha: 0 },
    })
    .extend({
      top: pad,
      bottom: pad,
      left: pad,
      right: pad,
      background: { r: 0, g: 0, b: 0, alpha: 0 },
    })
    .png()
    .toBuffer();

  return sharp(fitted);
}

async function writePng(pipeline, name, size) {
  const dest = path.join(ROOT, name);
  await pipeline
    .clone()
    .resize(size, size, {
      fit: "contain",
      background: { r: 0, g: 0, b: 0, alpha: 0 },
      kernel: sharp.kernel.lanczos3,
    })
    .png({ compressionLevel: 9, adaptiveFiltering: true })
    .toFile(dest);
  console.log("Wrote", name);
}

async function writeSvg(pipeline) {
  const buf = await pipeline
    .clone()
    .resize(32, 32, {
      fit: "contain",
      background: { r: 0, g: 0, b: 0, alpha: 0 },
      kernel: sharp.kernel.lanczos3,
    })
    .png()
    .toBuffer();
  const b64 = buf.toString("base64");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32" role="img" aria-label="VibeAudit">
  <image width="32" height="32" xlink:href="data:image/png;base64,${b64}"/>
</svg>
`;
  fs.writeFileSync(path.join(ROOT, "favicon.svg"), svg, "utf8");
  console.log("Wrote favicon.svg");
}

async function main() {
  if (!fs.existsSync(SOURCE)) {
    throw new Error(`Missing ${SOURCE} — place the official VibeAudit symbol PNG there first.`);
  }
  const pipeline = await symbolPipelineFromSource();
  for (const [name, size] of SIZES) {
    await writePng(pipeline, name, size);
  }
  await writeSvg(pipeline);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
