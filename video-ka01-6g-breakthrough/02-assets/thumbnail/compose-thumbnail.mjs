import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const sharp = require("sharp");

const input = new URL("../generated-stills/ka01-network-sensing-hero-v1.png", import.meta.url);
const output = new URL("./ka01-thumbnail-it-can-see-v1.png", import.meta.url);

const type = Buffer.from(`
<svg width="1280" height="720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="7"/>
      <feOffset dx="5" dy="8" result="offsetblur"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.9"/></feComponentTransfer>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect x="0" y="0" width="590" height="720" fill="url(#fade)"/>
  <defs>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="#050912" stop-opacity="0.78"/>
      <stop offset="0.78" stop-color="#050912" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#050912" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <g font-family="Impact, Arial Black, sans-serif" font-weight="900" filter="url(#shadow)" text-anchor="start">
    <text x="62" y="292" font-size="115" letter-spacing="2" fill="#F5F7FA" stroke="#05070B" stroke-width="9" paint-order="stroke">IT CAN</text>
    <text x="62" y="457" font-size="170" letter-spacing="2" fill="#FFB12B" stroke="#05070B" stroke-width="11" paint-order="stroke">SEE</text>
  </g>
</svg>`);

await sharp(fileURLToPath(input))
  .resize(1280, 720, { fit: "cover", position: "centre" })
  .composite([{ input: type, top: 0, left: 0 }])
  .png({ compressionLevel: 9 })
  .toFile(fileURLToPath(output));

console.log(fileURLToPath(output));
