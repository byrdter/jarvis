import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const palette = {
  ink: "#28313b",
  paper: "#f7f1df",
  cream: "#fff8e8",
  coral: "#e96f5f",
  red: "#d84f4a",
  gold: "#f2c14e",
  blue: "#55a6c8",
  sky: "#a8dbe8",
  green: "#7bb36a",
  mint: "#9bd6b5",
  purple: "#8067b7",
  violet: "#b57acc",
  slate: "#60707c",
  tan: "#d9a36c",
  skinA: "#c9865a",
  skinB: "#8e5b43",
  skinC: "#f1b78c",
  hairA: "#2b2a35",
  hairB: "#6a3f2b",
  white: "#ffffff",
  shadow: "#1f2a33",
};

const dirs = [
  "characters/host-a/poses",
  "characters/host-b/poses",
  "characters/host-c/poses",
  "characters/host-d/poses",
  "characters/expressions",
  "props/science",
  "props/tech",
  "props/media",
  "props/legal",
  "props/everyday",
  "diagrams",
  "backgrounds",
  "textures",
  "animation-presets",
];

const assets = [];

function esc(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll('"', "&quot;");
}

function svg(name, width, height, body, opts = {}) {
  const title = opts.title ?? name;
  const desc = opts.desc ?? "Reusable flat cartoon explainer asset for HyperFrames scenes.";
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="title desc">
  <title id="title">${esc(title)}</title>
  <desc id="desc">${esc(desc)}</desc>
  <defs>
    <filter id="paperNoise" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="12" result="noise"/>
      <feColorMatrix type="saturate" values="0"/>
      <feComponentTransfer>
        <feFuncA type="table" tableValues="0 0.06"/>
      </feComponentTransfer>
      <feBlend in="SourceGraphic" in2="noise" mode="multiply"/>
    </filter>
    <style>
      .ink{stroke:${palette.ink};stroke-width:7;stroke-linecap:round;stroke-linejoin:round}
      .thin{stroke:${palette.ink};stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
      .no-fill{fill:none}
      .asset-shadow{fill:${palette.shadow};opacity:.16}
      text{font-family:Inter,Arial,sans-serif;font-weight:800;letter-spacing:0}
    </style>
  </defs>
${body}
</svg>
`;
}

function saveAsset(relPath, type, tags, content) {
  assets.push({ path: relPath, type, tags });
  return writeFile(path.join(root, relPath), content);
}

function poseSvg({ name, host, skin, hair, shirt, pants, expression, arm, prop, mirror = false }) {
  const eyeY = expression === "shocked" ? 91 : 94;
  const mouth = {
    neutral: `<path class="thin no-fill" d="M140 120 q18 8 36 0"/>`,
    happy: `<path class="thin no-fill" d="M138 118 q22 28 45 0"/>`,
    worried: `<path class="thin no-fill" d="M139 128 q18 -13 38 0"/>`,
    thinking: `<path class="thin no-fill" d="M148 126 q12 5 25 0"/>`,
    shocked: `<ellipse class="thin" cx="160" cy="123" rx="12" ry="17" fill="${palette.cream}"/>`,
    skeptical: `<path class="thin no-fill" d="M140 124 q18 2 38 -4"/>`,
    angry: `<path class="thin no-fill" d="M139 130 q20 -18 42 0"/>`,
    confused: `<path class="thin no-fill" d="M142 126 q13 -10 26 0 q10 8 22 0"/>`,
    tired: `<path class="thin no-fill" d="M141 126 h39"/>`,
    excited: `<path class="thin no-fill" d="M136 116 q25 34 51 0"/>`,
  }[expression] ?? "";
  const brow = {
    worried: `<path class="thin no-fill" d="M126 82 l22 -8 M175 74 l22 8"/>`,
    shocked: `<path class="thin no-fill" d="M126 78 q11 -12 23 0 M175 78 q11 -12 23 0"/>`,
    skeptical: `<path class="thin no-fill" d="M124 76 q13 8 27 2 M175 80 q12 -10 25 -10"/>`,
    angry: `<path class="thin no-fill" d="M126 75 l25 12 M199 75 l-25 12"/>`,
    confused: `<path class="thin no-fill" d="M125 80 q13 -11 27 -1 M176 80 q13 7 25 -1"/>`,
    tired: `<path class="thin no-fill" d="M126 84 h24 M176 84 h24"/>`,
    excited: `<path class="thin no-fill" d="M126 77 q14 -13 28 0 M174 77 q14 -13 28 0"/>`,
  }[expression] ?? `<path class="thin no-fill" d="M126 81 q12 -7 24 0 M174 81 q12 -7 24 0"/>`;
  const armLeft = arm === "point-left"
    ? `<g id="arm-left"><path class="ink" d="M105 188 q-62 -12 -82 -55" fill="none"/><circle class="ink" cx="21" cy="130" r="12" fill="${skin}"/></g>`
    : arm === "hold"
      ? `<g id="arm-left"><path class="ink" d="M111 188 q-39 20 -50 58" fill="none"/><circle class="ink" cx="58" cy="252" r="12" fill="${skin}"/></g>`
      : `<g id="arm-left"><path class="ink" d="M111 190 q-32 31 -30 83" fill="none"/><circle class="ink" cx="80" cy="276" r="12" fill="${skin}"/></g>`;
  const armRight = arm === "point-right"
    ? `<g id="arm-right"><path class="ink" d="M215 188 q64 -14 82 -58" fill="none"/><circle class="ink" cx="300" cy="127" r="12" fill="${skin}"/></g>`
    : arm === "hold"
      ? `<g id="arm-right"><path class="ink" d="M210 188 q42 21 52 58" fill="none"/><circle class="ink" cx="265" cy="252" r="12" fill="${skin}"/></g>`
      : `<g id="arm-right"><path class="ink" d="M210 190 q34 32 31 83" fill="none"/><circle class="ink" cx="242" cy="276" r="12" fill="${skin}"/></g>`;
  const propSvg = prop === "card"
    ? `<g id="held-prop"><rect class="ink" x="89" y="244" width="142" height="82" rx="12" fill="${palette.cream}"/><path class="thin no-fill" d="M113 272 h82 M113 296 h56"/><circle class="thin" cx="206" cy="295" r="16" fill="${palette.gold}"/></g>`
    : prop === "pointer"
      ? `<g id="held-prop"><path class="thin no-fill" d="M271 128 l49 -31"/><circle class="thin" cx="324" cy="95" r="5" fill="${palette.red}"/></g>`
      : prop === "book"
        ? `<g id="held-prop"><path class="ink" d="M92 245 q40 -18 70 12 q30 -30 72 -10 v72 q-42 -15 -72 11 q-34 -23 -70 -8z" fill="${palette.cream}"/><path class="thin no-fill" d="M162 255 v70"/></g>`
        : "";
  const body = `
  <rect width="320" height="360" rx="24" fill="none"/>
  <g id="character" transform="${mirror ? "translate(320 0) scale(-1 1)" : ""}">
    <ellipse class="asset-shadow" cx="161" cy="329" rx="78" ry="16"/>
    <g id="legs">
      <path class="ink" d="M133 261 v57" fill="none"/>
      <path class="ink" d="M188 261 v57" fill="none"/>
      <path class="ink" d="M111 324 h35" fill="none"/>
      <path class="ink" d="M175 324 h35" fill="none"/>
    </g>
    <g id="torso">
      <path class="ink" d="M107 174 q52 -39 107 0 l24 96 q-72 28 -154 0z" fill="${shirt}"/>
      <path class="thin no-fill" d="M159 184 v86"/>
      <path class="ink" d="M106 270 q55 17 109 0" fill="${pants}"/>
    </g>
    ${armLeft}
    ${armRight}
    ${propSvg}
    <g id="head">
      <path class="ink" d="M101 94 q3 -46 59 -61 q63 11 62 64 q2 52 -59 64 q-61 -11 -62 -67z" fill="${skin}"/>
      <path class="ink" d="M105 87 q12 -55 64 -62 q39 8 54 45 q-28 -17 -58 -16 q-33 0 -60 33z" fill="${hair}"/>
      ${brow}
      <circle cx="141" cy="${eyeY}" r="${expression === "shocked" ? 7 : 5}" fill="${palette.ink}"/>
      <circle cx="181" cy="${eyeY}" r="${expression === "shocked" ? 7 : 5}" fill="${palette.ink}"/>
      <path class="thin no-fill" d="M161 94 q-8 15 5 22"/>
      ${mouth}
    </g>
  </g>`;
  return svg(`${host}-${name}`, 320, 360, body, {
    title: `${host} ${name}`,
    desc: "Layered host pose with stable group ids: character, head, torso, arms, legs, and held-prop.",
  });
}

function expressionSvg({ name, skin, hair, expression }) {
  return poseSvg({
    name: `expression-${name}`,
    host: "expression",
    skin,
    hair,
    shirt: palette.mint,
    pants: palette.blue,
    expression,
    arm: "rest",
  }).replace('width="320" height="360" viewBox="0 0 320 360"', 'width="220" height="220" viewBox="70 10 180 180"');
}

function propIcon(name, body, tags = ["prop"]) {
  return svg(name, 240, 240, `
  <rect width="240" height="240" rx="24" fill="none"/>
  <g id="prop" filter="url(#paperNoise)">
    <ellipse class="asset-shadow" cx="120" cy="205" rx="70" ry="12"/>
    ${body}
  </g>`, { title: name, desc: "Reusable cartoon prop with thick outline and transparent background." });
}

function diagram(name, body) {
  return svg(name, 420, 260, `
  <rect width="420" height="260" rx="24" fill="none"/>
  <g id="diagram">
    ${body}
  </g>`, { title: name, desc: "Reusable explainer diagram element for labels, callouts, charts, and motion paths." });
}

function background(name, body) {
  return svg(name, 1280, 720, `
  <rect width="1280" height="720" fill="${palette.paper}"/>
  <g id="background" filter="url(#paperNoise)">
    ${body}
  </g>`, { title: name, desc: "Reusable 16:9 flat cartoon background for explainer scenes." });
}

function texture(name, body) {
  return svg(name, 1280, 720, `
  <rect width="1280" height="720" fill="transparent"/>
  <g id="texture">
    ${body}
  </g>`, { title: name, desc: "Transparent overlay texture for subtle visual variance." });
}

async function main() {
  await Promise.all(dirs.map((dir) => mkdir(path.join(root, dir), { recursive: true })));

  const hosts = [
    { id: "host-a", skin: palette.skinC, hair: palette.hairA, shirt: palette.blue, pants: palette.purple },
    { id: "host-b", skin: palette.skinB, hair: palette.hairB, shirt: palette.green, pants: palette.slate, mirrorLeft: true },
    { id: "host-c", skin: palette.skinA, hair: palette.hairB, shirt: palette.coral, pants: palette.blue },
    { id: "host-d", skin: "#7a4d37", hair: palette.hairA, shirt: palette.gold, pants: palette.green, mirrorRight: true },
  ];

  const poses = [
    ["neutral", "neutral", "rest", null],
    ["happy", "happy", "rest", null],
    ["thinking", "thinking", "hold", "book"],
    ["worried", "worried", "rest", null],
    ["shocked", "shocked", "rest", null],
    ["point-left", "neutral", "point-left", "pointer"],
    ["point-right", "neutral", "point-right", "pointer"],
    ["explaining-card", "happy", "hold", "card"],
    ["skeptical-cross", "skeptical", "hold", null],
    ["excited-present", "excited", "point-right", "card"],
  ];

  for (const host of hosts) {
    for (const [name, expression, arm, prop] of poses) {
      await saveAsset(`characters/${host.id}/poses/${name}.svg`, "character-pose", [host.id, expression, arm].filter(Boolean), poseSvg({
        name,
        host: host.id,
        skin: host.skin,
        hair: host.hair,
        shirt: host.shirt,
        pants: host.pants,
        expression,
        arm,
        prop,
        mirror: (host.mirrorLeft && name === "point-left") || (host.mirrorRight && name === "point-right"),
      }));
    }
  }

  const expressions = ["neutral", "happy", "thinking", "worried", "shocked", "skeptical", "angry", "confused", "tired", "excited"];
  for (const host of hosts) {
    for (const expression of expressions) {
      const name = `${host.id}-${expression}`;
      await saveAsset(`characters/expressions/${name}.svg`, "expression", [host.id, expression], expressionSvg({ name, skin: host.skin, hair: host.hair, expression }));
    }
  }

  const props = [
    ["science/atom.svg", "atom", `<circle class="ink" cx="120" cy="112" r="15" fill="${palette.gold}"/><ellipse class="thin no-fill" cx="120" cy="112" rx="78" ry="28" transform="rotate(0 120 112)"/><ellipse class="thin no-fill" cx="120" cy="112" rx="78" ry="28" transform="rotate(60 120 112)"/><ellipse class="thin no-fill" cx="120" cy="112" rx="78" ry="28" transform="rotate(120 120 112)"/>`],
    ["science/microscope.svg", "microscope", `<path class="ink" d="M85 163 h82 v28 H65 q18 -12 20 -28z" fill="${palette.blue}"/><path class="ink" d="M105 65 l45 22 -16 33 -45 -22z" fill="${palette.cream}"/><path class="ink" d="M127 118 q11 35 -20 49" fill="none"/><path class="ink" d="M156 86 l22 -36" fill="none"/><path class="thin no-fill" d="M62 194 h135"/>`],
    ["science/syringe.svg", "syringe", `<path class="ink" d="M58 152 l76 -76 31 31 -76 76z" fill="${palette.cream}"/><path class="thin no-fill" d="M80 151 l31 31 M118 88 l31 31"/><path class="ink" d="M160 72 l25 -25" fill="none"/><path class="thin no-fill" d="M181 44 l27 -27"/><path class="ink" d="M44 168 l29 29" fill="none"/>`],
    ["science/shield.svg", "shield", `<path class="ink" d="M120 39 q45 28 79 28 q-1 89 -79 135 q-78 -46 -79 -135 q34 0 79 -28z" fill="${palette.green}"/><path class="thin no-fill" d="M120 70 v93 M83 113 h74"/>`],
    ["science/virus.svg", "virus", `<circle class="ink" cx="120" cy="119" r="52" fill="${palette.violet}"/><path class="ink" d="M120 45 v-25 M120 218 v-25 M45 119 h-25 M220 119 h-25 M67 66 l-18 -18 M191 190 l-18 -18 M67 190 l-18 18 M191 66 l18 -18" fill="none"/><circle cx="103" cy="103" r="7" fill="${palette.ink}"/><circle cx="141" cy="103" r="7" fill="${palette.ink}"/><path class="thin no-fill" d="M98 140 q23 22 48 0"/>`],
    ["everyday/book.svg", "book", `<path class="ink" d="M46 66 q49 -19 74 16 q27 -35 74 -16 v108 q-48 -18 -74 16 q-27 -34 -74 -16z" fill="${palette.cream}"/><path class="thin no-fill" d="M120 82 v106 M67 99 h31 M67 123 h35 M142 99 h31 M142 123 h28"/>`],
    ["everyday/laptop.svg", "laptop", `<rect class="ink" x="61" y="54" width="120" height="87" rx="8" fill="${palette.slate}"/><rect x="75" y="68" width="92" height="58" rx="4" fill="${palette.sky}"/><path class="ink" d="M35 170 h170 l-22 26 H57z" fill="${palette.cream}"/><path class="thin no-fill" d="M96 181 h48"/>`],
    ["everyday/document.svg", "document", `<path class="ink" d="M71 35 h72 l39 39 v128 H71z" fill="${palette.cream}"/><path class="thin no-fill" d="M143 36 v39 h39 M92 104 h64 M92 130 h64 M92 156 h43"/><circle class="thin" cx="154" cy="169" r="18" fill="${palette.gold}"/>`],
    ["everyday/magnifier.svg", "magnifier", `<circle class="ink" cx="103" cy="101" r="54" fill="${palette.sky}"/><path class="ink" d="M143 142 l51 51" fill="none"/><path class="thin no-fill" d="M75 96 q20 -25 55 -11"/>`],
    ["everyday/speech-bubble.svg", "speech-bubble", `<path class="ink" d="M43 70 q0 -34 39 -34 h78 q39 0 39 34 v39 q0 34 -39 34h-42 l-44 43 13 -43 h-5 q-39 0 -39 -34z" fill="${palette.cream}"/><path class="thin no-fill" d="M77 82 h83 M77 110 h57"/>`],
    ["everyday/phone.svg", "phone", `<rect class="ink" x="78" y="29" width="84" height="174" rx="18" fill="${palette.slate}"/><rect x="91" y="52" width="58" height="112" rx="7" fill="${palette.sky}"/><circle cx="120" cy="183" r="8" fill="${palette.cream}"/>`],
    ["everyday/clock.svg", "clock", `<circle class="ink" cx="120" cy="119" r="72" fill="${palette.cream}"/><path class="thin no-fill" d="M120 66 v54 l39 24"/><path class="thin no-fill" d="M120 40 v18 M120 180 v18 M41 119 h18 M181 119 h18"/>`],
    ["everyday/money.svg", "money", `<rect class="ink" x="43" y="65" width="154" height="100" rx="15" fill="${palette.green}"/><circle class="thin" cx="120" cy="115" r="29" fill="${palette.mint}"/><path class="thin no-fill" d="M120 92 v46 M104 105 q18 -14 34 0 M102 127 q20 16 38 0"/>`],
    ["everyday/folder.svg", "folder", `<path class="ink" d="M37 78 h70 l18 25 h78 v78 q0 20 -20 20H57 q-20 0 -20 -20z" fill="${palette.gold}"/><path class="thin no-fill" d="M54 119 h132 M58 150 h92"/>`],
    ["everyday/lightbulb.svg", "lightbulb", `<path class="ink" d="M120 34 q58 0 58 55 q0 35 -35 63 v22 h-46 v-22 q-35 -28 -35 -63 q0 -55 58 -55z" fill="${palette.gold}"/><path class="thin no-fill" d="M96 196 h48 M101 216 h38 M103 86 q17 -26 43 -4"/>`],
    ["science/dna.svg", "dna", `<path class="ink no-fill" d="M76 38 q89 42 0 166 M164 38 q-89 42 0 166"/><path class="thin no-fill" d="M87 62 h66 M74 92 h92 M74 122 h92 M87 152 h66 M99 182 h42"/>`],
    ["science/pill.svg", "pill", `<g transform="rotate(-32 120 120)"><rect class="ink" x="52" y="82" width="136" height="76" rx="38" fill="${palette.cream}"/><path class="thin no-fill" d="M120 82 v76"/><path d="M120 85 h31 q34 0 34 35 q0 35 -34 35h-31z" fill="${palette.coral}" opacity=".95"/></g>`],
    ["science/brain.svg", "brain", `<path class="ink" d="M82 143 q-36 -9 -31 -48 q3 -26 29 -30 q8 -34 44 -28 q30 -20 58 5 q31 1 38 32 q27 12 20 45 q-5 33 -39 35 q-20 35 -58 14 q-34 16 -61 -25z" fill="${palette.violet}"/><path class="thin no-fill" d="M91 75 q24 15 17 40 M145 61 q-24 30 5 56 M188 75 q-31 13 -23 47 M101 143 q32 -18 55 6"/>`],
    ["science/telescope.svg", "telescope", `<path class="ink" d="M73 91 l96 -38 16 39 -96 38z" fill="${palette.blue}"/><path class="ink" d="M93 130 l-32 55 M119 121 l-3 70 M145 111 l40 50" fill="none"/><circle class="thin" cx="56" cy="190" r="10" fill="${palette.gold}"/><path class="thin no-fill" d="M174 52 l22 -10"/>`],
    ["science/molecule.svg", "molecule", `<circle class="ink" cx="83" cy="118" r="34" fill="${palette.sky}"/><circle class="ink" cx="166" cy="76" r="28" fill="${palette.gold}"/><circle class="ink" cx="166" cy="166" r="28" fill="${palette.green}"/><path class="thin no-fill" d="M113 102 l29 -14 M113 134 l29 18"/><circle cx="83" cy="118" r="8" fill="${palette.ink}"/>`],
    ["tech/server-stack.svg", "server-stack", `<rect class="ink" x="54" y="42" width="132" height="46" rx="10" fill="${palette.slate}"/><rect class="ink" x="54" y="97" width="132" height="46" rx="10" fill="${palette.blue}"/><rect class="ink" x="54" y="152" width="132" height="46" rx="10" fill="${palette.slate}"/><circle cx="82" cy="65" r="6" fill="${palette.mint}"/><circle cx="82" cy="120" r="6" fill="${palette.gold}"/><circle cx="82" cy="175" r="6" fill="${palette.coral}"/><path class="thin no-fill" d="M105 65 h48 M105 120 h48 M105 175 h48"/>`],
    ["tech/code-window.svg", "code-window", `<rect class="ink" x="36" y="50" width="168" height="138" rx="16" fill="${palette.cream}"/><path class="thin no-fill" d="M36 86 h168"/><circle cx="62" cy="68" r="6" fill="${palette.coral}"/><circle cx="84" cy="68" r="6" fill="${palette.gold}"/><circle cx="106" cy="68" r="6" fill="${palette.green}"/><path class="thin no-fill" d="M76 122 l-24 20 l24 20 M164 122 l24 20 l-24 20 M111 168 l28 -62"/>`],
    ["tech/cloud.svg", "cloud", `<path class="ink" d="M72 165 q-39 0 -39 -35 q0 -31 31 -35 q12 -45 61 -38 q36 -28 78 2 q36 4 43 41 q31 9 31 38 q0 37 -43 37H72z" fill="${palette.sky}"/><path class="thin no-fill" d="M91 132 h96 M112 105 h62"/>`],
    ["tech/robot-head.svg", "robot-head", `<rect class="ink" x="55" y="72" width="130" height="102" rx="24" fill="${palette.mint}"/><path class="ink no-fill" d="M120 72 v-30"/><circle class="thin" cx="120" cy="34" r="12" fill="${palette.gold}"/><circle cx="91" cy="117" r="9" fill="${palette.ink}"/><circle cx="149" cy="117" r="9" fill="${palette.ink}"/><path class="thin no-fill" d="M91 146 h58"/>`],
    ["tech/api-plug.svg", "api-plug", `<rect class="ink" x="60" y="75" width="85" height="74" rx="15" fill="${palette.gold}"/><path class="ink no-fill" d="M145 112 h36 q25 0 25 25 v23"/><path class="thin no-fill" d="M81 55 v20 M123 55 v20 M77 112 h50"/>`],
    ["tech/terminal.svg", "terminal", `<rect class="ink" x="36" y="52" width="168" height="136" rx="16" fill="${palette.ink}"/><path d="M63 96 l25 21 l-25 21" stroke="${palette.cream}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/><path d="M105 141 h60" stroke="${palette.gold}" stroke-width="7" stroke-linecap="round"/>`],
    ["media/camera.svg", "camera", `<path class="ink" d="M42 80 h45 l16 -24 h48 l16 24 h31 q24 0 24 24 v72 q0 24 -24 24H42q-24 0 -24 -24v-72q0 -24 24 -24z" fill="${palette.slate}"/><circle class="ink" cx="120" cy="140" r="42" fill="${palette.sky}"/><circle class="thin" cx="120" cy="140" r="22" fill="${palette.cream}"/>`],
    ["media/microphone.svg", "microphone", `<rect class="ink" x="84" y="35" width="72" height="116" rx="36" fill="${palette.coral}"/><path class="ink no-fill" d="M54 112 q0 66 66 66 q66 0 66 -66 M120 178 v35 M82 213 h76"/><path class="thin no-fill" d="M102 70 h36 M102 101 h36"/>`],
    ["media/play-button.svg", "play-button", `<circle class="ink" cx="120" cy="120" r="82" fill="${palette.coral}"/><path class="ink" d="M98 74 l82 46 -82 46z" fill="${palette.cream}"/>`],
    ["media/thumbnail-frame.svg", "thumbnail-frame", `<rect class="ink" x="38" y="55" width="164" height="116" rx="16" fill="${palette.sky}"/><path class="thin no-fill" d="M62 145 l42 -42 l31 31 l20 -20 l25 31"/><circle class="thin" cx="164" cy="88" r="14" fill="${palette.gold}"/><rect class="ink" x="58" y="181" width="124" height="22" rx="10" fill="${palette.coral}"/>`],
    ["media/waveform.svg", "waveform", `<path class="ink no-fill" d="M28 126 h30 l16 -47 l29 102 l31 -127 l29 127 l29 -102 l16 47 h24"/><path class="thin no-fill" d="M50 197 h140"/>`],
    ["legal/gavel.svg", "gavel", `<g transform="rotate(-36 120 120)"><rect class="ink" x="73" y="62" width="93" height="37" rx="9" fill="${palette.tan}"/><rect class="ink" x="91" y="99" width="57" height="24" rx="7" fill="${palette.gold}"/><path class="ink no-fill" d="M120 123 v88"/></g><rect class="thin" x="56" y="189" width="120" height="24" rx="8" fill="${palette.slate}"/>`],
    ["legal/scales.svg", "scales", `<path class="ink no-fill" d="M120 45 v150 M75 76 h90 M120 76 l-48 70 M120 76 l48 70"/><path class="ink" d="M45 146 h54 q-5 35 -27 35 q-22 0 -27 -35z" fill="${palette.gold}"/><path class="ink" d="M141 146 h54 q-5 35 -27 35 q-22 0 -27 -35z" fill="${palette.gold}"/><path class="thin no-fill" d="M82 205 h76"/>`],
    ["legal/contract.svg", "contract", `<path class="ink" d="M64 32 h84 l38 38 v137H64z" fill="${palette.cream}"/><path class="thin no-fill" d="M148 33 v37 h38 M88 96 h70 M88 124 h70 M88 152 h44"/><path class="ink" d="M145 165 l35 35" fill="none"/><circle class="thin" cx="184" cy="204" r="13" fill="${palette.coral}"/>`],
    ["everyday/calendar.svg", "calendar", `<rect class="ink" x="42" y="58" width="156" height="136" rx="16" fill="${palette.cream}"/><path class="thin no-fill" d="M42 94 h156 M80 41 v35 M160 41 v35 M75 124 h24 M112 124 h24 M149 124 h24 M75 159 h24 M112 159 h24"/>`],
    ["everyday/map-fold.svg", "map-fold", `<path class="ink" d="M43 65 l52 -22 l50 22 l52 -22 v132 l-52 22 l-50 -22 l-52 22z" fill="${palette.cream}"/><path class="thin no-fill" d="M95 43 v132 M145 65 v132 M67 103 q35 -25 68 0 q31 24 75 -8"/><circle class="thin" cx="151" cy="119" r="12" fill="${palette.coral}"/>`],
    ["everyday/clipboard.svg", "clipboard", `<rect class="ink" x="61" y="55" width="118" height="152" rx="18" fill="${palette.cream}"/><rect class="ink" x="88" y="33" width="64" height="42" rx="12" fill="${palette.gold}"/><path class="thin no-fill" d="M91 104 h57 M91 134 h57 M91 164 h42"/>`],
    ["everyday/toolbox.svg", "toolbox", `<rect class="ink" x="42" y="82" width="156" height="108" rx="18" fill="${palette.coral}"/><path class="ink no-fill" d="M87 82 v-22 h66 v22"/><path class="thin no-fill" d="M42 125 h156 M120 125 v65"/><circle cx="120" cy="145" r="8" fill="${palette.gold}"/>`],
    ["everyday/graduation-cap.svg", "graduation-cap", `<path class="ink" d="M32 91 l88 -42 l88 42 l-88 42z" fill="${palette.slate}"/><path class="ink" d="M73 122 q47 27 94 0 v49 q-47 31 -94 0z" fill="${palette.blue}"/><path class="thin no-fill" d="M208 91 v63"/><circle class="thin" cx="208" cy="168" r="12" fill="${palette.gold}"/>`],
    ["tech/database.svg", "database", `<ellipse class="ink" cx="120" cy="66" rx="72" ry="30" fill="${palette.sky}"/><path class="ink" d="M48 66 v104 q0 30 72 30 q72 0 72 -30V66" fill="${palette.sky}"/><path class="thin no-fill" d="M48 112 q0 30 72 30 q72 0 72 -30 M48 154 q0 30 72 30 q72 0 72 -30"/>`],
  ];
  for (const [rel, name, body] of props) {
    await saveAsset(`props/${rel}`, "prop", [name], propIcon(name, body));
  }

  const diagramBodies = [
    ["arrow-curved.svg", `<path class="ink no-fill" d="M75 178 q124 -126 263 -42"/><path class="ink" d="M322 102 l43 40 -55 7z" fill="${palette.coral}"/>`],
    ["callout-bubble.svg", `<path class="ink" d="M48 58 h260 q43 0 43 40 v44 q0 40 -43 40H169 l-57 44 17 -44H48 q-31 0 -31 -31V89q0 -31 31 -31z" fill="${palette.cream}"/><path class="thin no-fill" d="M77 104 h204 M77 137 h149"/>`],
    ["comparison-panel.svg", `<rect class="ink" x="35" y="44" width="157" height="172" rx="18" fill="${palette.sky}"/><rect class="ink" x="228" y="44" width="157" height="172" rx="18" fill="${palette.gold}"/><path class="thin no-fill" d="M76 102 h76 M76 134 h55 M267 102 h76 M267 134 h55"/><text x="91" y="190" font-size="26" fill="${palette.ink}">A</text><text x="285" y="190" font-size="26" fill="${palette.ink}">B</text>`],
    ["timeline.svg", `<path class="ink no-fill" d="M44 134 h327"/><circle class="ink" cx="82" cy="134" r="22" fill="${palette.coral}"/><circle class="ink" cx="177" cy="134" r="22" fill="${palette.gold}"/><circle class="ink" cx="272" cy="134" r="22" fill="${palette.green}"/><path class="thin no-fill" d="M82 91 v-30 M177 177 v30 M272 91 v-30"/><rect class="thin" x="51" y="32" width="62" height="30" rx="8" fill="${palette.cream}"/><rect class="thin" x="146" y="205" width="62" height="30" rx="8" fill="${palette.cream}"/><rect class="thin" x="241" y="32" width="62" height="30" rx="8" fill="${palette.cream}"/>`],
    ["bar-chart.svg", `<path class="ink no-fill" d="M61 214 V55 M61 214 h304"/><rect class="ink" x="92" y="151" width="42" height="63" rx="8" fill="${palette.blue}"/><rect class="ink" x="162" y="110" width="42" height="104" rx="8" fill="${palette.green}"/><rect class="ink" x="232" y="75" width="42" height="139" rx="8" fill="${palette.gold}"/><rect class="ink" x="302" y="130" width="42" height="84" rx="8" fill="${palette.coral}"/>`],
    ["flow-nodes.svg", `<circle class="ink" cx="82" cy="130" r="36" fill="${palette.sky}"/><circle class="ink" cx="210" cy="82" r="36" fill="${palette.gold}"/><circle class="ink" cx="210" cy="178" r="36" fill="${palette.green}"/><circle class="ink" cx="338" cy="130" r="36" fill="${palette.violet}"/><path class="thin no-fill" d="M118 119 l56 -21 M118 141 l56 21 M246 94 l56 21 M246 166 l56 -21"/>`],
    ["question-card.svg", `<rect class="ink" x="87" y="35" width="246" height="188" rx="28" fill="${palette.purple}"/><text x="187" y="164" font-size="122" fill="${palette.cream}">?</text><path class="thin no-fill" d="M119 70 h73 M119 96 h43"/>`],
    ["map-pin.svg", `<path class="ink" d="M210 35 q-75 0 -75 73 q0 63 75 122 q75 -59 75 -122 q0 -73 -75 -73z" fill="${palette.coral}"/><circle class="ink" cx="210" cy="108" r="28" fill="${palette.cream}"/><path class="thin no-fill" d="M47 191 q72 -29 153 0 q83 29 173 -5"/>`],
    ["process-steps.svg", `<rect class="ink" x="37" y="82" width="86" height="86" rx="18" fill="${palette.sky}"/><rect class="ink" x="167" y="82" width="86" height="86" rx="18" fill="${palette.gold}"/><rect class="ink" x="297" y="82" width="86" height="86" rx="18" fill="${palette.green}"/><path class="thin no-fill" d="M126 125 h36 M256 125 h36"/><text x="71" y="139" font-size="30" fill="${palette.ink}">1</text><text x="201" y="139" font-size="30" fill="${palette.ink}">2</text><text x="331" y="139" font-size="30" fill="${palette.ink}">3</text>`],
    ["venn.svg", `<circle class="ink" cx="169" cy="130" r="70" fill="${palette.sky}" opacity=".84"/><circle class="ink" cx="251" cy="130" r="70" fill="${palette.coral}" opacity=".84"/><text x="194" y="143" font-size="28" fill="${palette.ink}">fit</text>`],
    ["checklist.svg", `<rect class="ink" x="76" y="34" width="270" height="194" rx="22" fill="${palette.cream}"/><path class="thin no-fill" d="M116 82 l19 19 l35 -42 M116 133 l19 19 l35 -42 M191 90 h97 M191 142 h97"/>`],
    ["warning-sign.svg", `<path class="ink" d="M210 34 l166 190H44z" fill="${palette.gold}"/><path class="thin no-fill" d="M210 95 v62"/><circle cx="210" cy="190" r="9" fill="${palette.ink}"/>`],
    ["quote-card.svg", `<rect class="ink" x="55" y="46" width="310" height="168" rx="26" fill="${palette.cream}"/><text x="84" y="139" font-size="78" fill="${palette.purple}">“</text><path class="thin no-fill" d="M145 105 h158 M145 141 h118"/>`],
    ["number-badge.svg", `<circle class="ink" cx="210" cy="130" r="92" fill="${palette.coral}"/><text x="176" y="158" font-size="88" fill="${palette.cream}">10</text>`],
    ["meter.svg", `<path class="ink" d="M78 188 q31 -93 132 -93 q101 0 132 93z" fill="${palette.cream}"/><path class="thin no-fill" d="M114 178 q26 -48 96 -48 q70 0 96 48"/><path class="ink" d="M210 176 l58 -53" fill="none"/><circle class="thin" cx="210" cy="176" r="15" fill="${palette.gold}"/>`],
    ["funnel.svg", `<path class="ink" d="M66 46 h288 l-104 112 v62 h-80 v-62z" fill="${palette.sky}"/><path class="thin no-fill" d="M102 82 h216 M128 119 h164 M170 182 h80"/>`],
    ["cycle.svg", `<path class="ink no-fill" d="M126 69 q83 -54 154 16"/><path class="ink" d="M276 44 l32 58 -64 -7z" fill="${palette.green}"/><path class="ink no-fill" d="M292 184 q-83 54 -154 -16"/><path class="ink" d="M142 209 l-32 -58 64 7z" fill="${palette.coral}"/><circle class="thin" cx="210" cy="130" r="42" fill="${palette.cream}"/>`],
    ["decision-tree.svg", `<circle class="ink" cx="210" cy="56" r="30" fill="${palette.gold}"/><circle class="ink" cx="105" cy="175" r="30" fill="${palette.sky}"/><circle class="ink" cx="210" cy="175" r="30" fill="${palette.green}"/><circle class="ink" cx="315" cy="175" r="30" fill="${palette.violet}"/><path class="thin no-fill" d="M194 82 l-70 70 M210 87 v58 M226 82 l70 70"/>`],
    ["axis-matrix.svg", `<rect class="ink" x="72" y="42" width="276" height="176" rx="18" fill="${palette.cream}"/><path class="thin no-fill" d="M210 42 v176 M72 130 h276"/><circle class="thin" cx="145" cy="88" r="20" fill="${palette.coral}"/><circle class="thin" cx="278" cy="172" r="20" fill="${palette.green}"/>`],
    ["data-table.svg", `<rect class="ink" x="56" y="48" width="308" height="172" rx="18" fill="${palette.cream}"/><path class="thin no-fill" d="M56 96 h308 M56 140 h308 M56 184 h308 M160 48 v172 M262 48 v172"/><circle cx="108" cy="118" r="10" fill="${palette.blue}"/><circle cx="210" cy="162" r="10" fill="${palette.gold}"/><circle cx="312" cy="206" r="10" fill="${palette.green}"/>`],
    ["stacked-cards.svg", `<rect class="ink" x="96" y="70" width="210" height="120" rx="18" fill="${palette.sky}" opacity=".7"/><rect class="ink" x="78" y="54" width="210" height="120" rx="18" fill="${palette.gold}" opacity=".8"/><rect class="ink" x="60" y="38" width="210" height="120" rx="18" fill="${palette.cream}"/><path class="thin no-fill" d="M96 83 h126 M96 116 h92"/>`],
    ["spotlight-callout.svg", `<circle class="ink" cx="210" cy="130" r="76" fill="${palette.gold}" opacity=".85"/><path class="ink no-fill" d="M210 24 v38 M210 198 v38 M104 130H66 M354 130h-38 M135 55 l28 28 M285 177 l28 28 M135 205 l28 -28 M285 83 l28 -28"/><circle class="thin" cx="210" cy="130" r="36" fill="${palette.cream}"/>`],
    ["myth-vs-fact.svg", `<rect class="ink" x="35" y="45" width="160" height="170" rx="18" fill="${palette.coral}"/><rect class="ink" x="225" y="45" width="160" height="170" rx="18" fill="${palette.green}"/><text x="82" y="116" font-size="34" fill="${palette.cream}">MYTH</text><text x="270" y="116" font-size="34" fill="${palette.cream}">FACT</text><path class="thin no-fill" d="M75 160 h80 M265 160 h80"/>`],
    ["risk-ladder.svg", `<path class="ink no-fill" d="M118 214 V48 M302 214 V48"/><path class="thin no-fill" d="M118 80 h184 M118 118 h184 M118 156 h184 M118 194 h184"/><circle class="ink" cx="210" cy="194" r="20" fill="${palette.green}"/><circle class="ink" cx="210" cy="118" r="20" fill="${palette.gold}"/><circle class="ink" cx="210" cy="80" r="20" fill="${palette.coral}"/>`],
    ["evidence-card.svg", `<rect class="ink" x="62" y="36" width="296" height="188" rx="24" fill="${palette.cream}"/><path class="thin no-fill" d="M105 91 h166 M105 126 h210 M105 161 h138"/><circle class="thin" cx="305" cy="88" r="28" fill="${palette.green}"/><path class="thin no-fill" d="M291 88 l10 12 l22 -26"/>`],
    ["source-tag.svg", `<path class="ink" d="M52 74 h224 l72 56 l-72 56H52z" fill="${palette.sky}"/><circle class="thin" cx="92" cy="130" r="18" fill="${palette.cream}"/><path class="thin no-fill" d="M133 112 h117 M133 146 h80"/>`],
    ["before-after-slider.svg", `<rect class="ink" x="48" y="54" width="324" height="152" rx="20" fill="${palette.cream}"/><path class="thin no-fill" d="M210 54 v152"/><rect x="50" y="56" width="160" height="148" rx="18" fill="${palette.coral}" opacity=".32"/><rect x="210" y="56" width="160" height="148" rx="18" fill="${palette.green}" opacity=".32"/><circle class="ink" cx="210" cy="130" r="28" fill="${palette.gold}"/><path class="thin no-fill" d="M201 112 v36 M219 112 v36"/>`],
    ["zoom-lens.svg", `<circle class="ink" cx="175" cy="111" r="68" fill="${palette.sky}" opacity=".75"/><path class="ink no-fill" d="M224 160 l70 62"/><rect class="thin" x="127" y="78" width="96" height="62" rx="10" fill="${palette.cream}"/><path class="thin no-fill" d="M146 108 h58"/>`],
    ["branching-path.svg", `<path class="ink no-fill" d="M58 130 h86 q46 0 46 -46 v-26 M144 130 q46 0 46 46 v26 M190 130 h174"/><circle class="ink" cx="58" cy="130" r="24" fill="${palette.gold}"/><circle class="ink" cx="190" cy="58" r="24" fill="${palette.sky}"/><circle class="ink" cx="190" cy="202" r="24" fill="${palette.coral}"/><circle class="ink" cx="364" cy="130" r="24" fill="${palette.green}"/>`],
    ["feedback-loop.svg", `<rect class="ink" x="78" y="58" width="102" height="64" rx="16" fill="${palette.sky}"/><rect class="ink" x="240" y="138" width="102" height="64" rx="16" fill="${palette.gold}"/><path class="ink no-fill" d="M180 90 q92 -28 124 39"/><path class="ink" d="M314 116 l12 49 -44 -25z" fill="${palette.coral}"/><path class="ink no-fill" d="M240 170 q-92 28 -124 -39"/><path class="ink" d="M106 144 l-12 -49 44 25z" fill="${palette.green}"/>`],
    ["heatmap-grid.svg", `<rect class="ink" x="70" y="40" width="280" height="180" rx="18" fill="${palette.cream}"/><g>${Array.from({ length: 4 }, (_, y) => Array.from({ length: 6 }, (_, x) => `<rect x="${95 + x * 39}" y="${66 + y * 34}" width="28" height="24" rx="5" fill="${[palette.sky, palette.gold, palette.coral, palette.green][(x + y) % 4]}" opacity="${0.45 + ((x * y + 1) % 4) * 0.12}"/>`).join("")).join("")}</g>`],
    ["probability-balls.svg", `<rect class="ink" x="65" y="56" width="290" height="148" rx="22" fill="${palette.cream}"/><g>${Array.from({ length: 24 }, (_, i) => `<circle cx="${94 + (i % 8) * 31}" cy="${91 + Math.floor(i / 8) * 39}" r="11" fill="${i % 7 === 0 ? palette.coral : palette.sky}" stroke="${palette.ink}" stroke-width="4"/>`).join("")}</g>`],
    ["network-map.svg", `<circle class="ink" cx="102" cy="92" r="26" fill="${palette.sky}"/><circle class="ink" cx="210" cy="60" r="26" fill="${palette.gold}"/><circle class="ink" cx="310" cy="126" r="26" fill="${palette.green}"/><circle class="ink" cx="168" cy="190" r="26" fill="${palette.coral}"/><circle class="ink" cx="255" cy="194" r="20" fill="${palette.violet}"/><path class="thin no-fill" d="M128 86 l56 -17 M232 76 l57 38 M292 141 l-25 37 M235 194 h-41 M184 174 l-66 -66 M194 80 l-20 87"/>`],
    ["annotation-pin.svg", `<path class="ink" d="M210 40 q58 0 58 55 q0 48 -58 105 q-58 -57 -58 -105 q0 -55 58 -55z" fill="${palette.coral}"/><circle class="thin" cx="210" cy="96" r="24" fill="${palette.cream}"/><rect class="ink" x="68" y="183" width="284" height="42" rx="18" fill="${palette.cream}"/><path class="thin no-fill" d="M101 204 h190"/>`],
    ["swimlane.svg", `<rect class="ink" x="45" y="42" width="330" height="176" rx="18" fill="${palette.cream}"/><path class="thin no-fill" d="M45 101 h330 M45 160 h330 M150 42 v176"/><rect class="thin" x="178" y="63" width="68" height="28" rx="8" fill="${palette.sky}"/><rect class="thin" x="270" y="122" width="68" height="28" rx="8" fill="${palette.gold}"/><rect class="thin" x="178" y="181" width="68" height="28" rx="8" fill="${palette.green}"/>`],
    ["formula-strip.svg", `<rect class="ink" x="45" y="83" width="330" height="94" rx="24" fill="${palette.cream}"/><text x="78" y="145" font-size="42" fill="${palette.ink}">A + B = C</text><circle class="thin" cx="320" cy="130" r="25" fill="${palette.gold}"/>`],
    ["timer-ring.svg", `<circle class="ink" cx="210" cy="130" r="80" fill="${palette.cream}"/><path class="ink no-fill" d="M210 50 a80 80 0 0 1 69 120"/><path class="ink" d="M267 163 l34 24 l-40 11z" fill="${palette.coral}"/><path class="thin no-fill" d="M210 88 v45 l35 20"/>`],
    ["ranking-podium.svg", `<rect class="ink" x="158" y="83" width="104" height="128" rx="14" fill="${palette.gold}"/><rect class="ink" x="62" y="132" width="104" height="79" rx="14" fill="${palette.sky}"/><rect class="ink" x="254" y="156" width="104" height="55" rx="14" fill="${palette.green}"/><text x="197" y="151" font-size="42" fill="${palette.ink}">1</text><text x="101" y="183" font-size="34" fill="${palette.ink}">2</text><text x="293" y="194" font-size="30" fill="${palette.ink}">3</text>`],
    ["split-screen.svg", `<rect class="ink" x="48" y="44" width="324" height="172" rx="20" fill="${palette.cream}"/><path class="thin no-fill" d="M210 44 v172"/><circle class="thin" cx="129" cy="130" r="42" fill="${palette.sky}"/><rect class="thin" x="254" y="88" width="76" height="84" rx="14" fill="${palette.gold}"/>`],
    ["caption-box.svg", `<rect class="ink" x="48" y="151" width="324" height="62" rx="18" fill="${palette.ink}"/><path d="M86 182 h160 M86 202 h92" stroke="${palette.cream}" stroke-width="7" stroke-linecap="round"/><circle cx="313" cy="182" r="13" fill="${palette.coral}"/>`],
  ];
  for (const [rel, body] of diagramBodies) {
    await saveAsset(`diagrams/${rel}`, "diagram", [rel.replace(".svg", "")], diagram(rel, body));
  }

  const backgroundBodies = [
    ["lab.svg", `<rect x="0" y="0" width="1280" height="720" fill="${palette.sky}"/><rect x="0" y="480" width="1280" height="240" fill="${palette.cream}"/><rect class="ink" x="80" y="112" width="270" height="198" rx="18" fill="${palette.white}"/><path class="thin no-fill" d="M117 163 h183 M117 207 h143 M117 251 h92"/><rect class="ink" x="830" y="162" width="286" height="318" rx="20" fill="${palette.mint}"/><path class="thin no-fill" d="M873 217 h200 M873 276 h153 M873 335 h184"/><circle class="thin" cx="1030" cy="585" r="42" fill="${palette.gold}"/>`],
    ["classroom.svg", `<rect width="1280" height="720" fill="#f0d6a5"/><rect class="ink" x="110" y="90" width="680" height="330" rx="20" fill="${palette.green}"/><path class="thin no-fill" d="M175 168 h260 M175 225 h460 M175 282 h310"/><rect x="0" y="515" width="1280" height="205" fill="${palette.tan}"/><rect class="ink" x="890" y="146" width="230" height="230" rx="16" fill="${palette.cream}"/>`],
    ["space.svg", `<rect width="1280" height="720" fill="#202b40"/><g fill="${palette.cream}" opacity=".9"><circle cx="100" cy="110" r="5"/><circle cx="265" cy="208" r="3"/><circle cx="484" cy="84" r="4"/><circle cx="722" cy="154" r="5"/><circle cx="1020" cy="102" r="4"/><circle cx="1132" cy="310" r="3"/><circle cx="908" cy="552" r="5"/><circle cx="352" cy="602" r="3"/></g><circle class="ink" cx="676" cy="363" r="138" fill="${palette.purple}"/><path class="thin no-fill" d="M556 356 q117 -69 241 -9 M579 420 q94 53 213 0"/><ellipse class="thin no-fill" cx="676" cy="363" rx="248" ry="64" transform="rotate(-12 676 363)"/>`],
    ["living-room.svg", `<rect width="1280" height="720" fill="#f1cfc2"/><rect x="0" y="510" width="1280" height="210" fill="#a9c3b4"/><rect class="ink" x="130" y="310" width="420" height="180" rx="35" fill="${palette.coral}"/><rect class="ink" x="710" y="130" width="300" height="205" rx="18" fill="${palette.cream}"/><path class="thin no-fill" d="M744 173 h222 M744 226 h173 M744 279 h198"/><circle class="thin" cx="1060" cy="476" r="54" fill="${palette.gold}"/>`],
    ["office.svg", `<rect width="1280" height="720" fill="#d6e4e8"/><rect x="0" y="496" width="1280" height="224" fill="#d2b48a"/><rect class="ink" x="95" y="112" width="300" height="205" rx="18" fill="${palette.cream}"/><rect class="ink" x="785" y="126" width="350" height="225" rx="20" fill="${palette.sky}"/><rect class="ink" x="492" y="432" width="260" height="78" rx="18" fill="${palette.slate}"/><path class="thin no-fill" d="M532 471 h180 M830 181 h250 M830 234 h190 M830 287 h220"/>`],
    ["city.svg", `<rect width="1280" height="720" fill="#b9dce8"/><rect x="0" y="545" width="1280" height="175" fill="${palette.slate}"/><rect class="ink" x="82" y="282" width="150" height="263" fill="${palette.cream}"/><rect class="ink" x="280" y="196" width="190" height="349" fill="${palette.blue}"/><rect class="ink" x="548" y="250" width="150" height="295" fill="${palette.gold}"/><rect class="ink" x="775" y="156" width="230" height="389" fill="${palette.mint}"/><path class="thin no-fill" d="M120 338 h74 M120 394 h74 M320 258 h110 M320 320 h110 M824 222 h136 M824 289 h136"/>`],
    ["map.svg", `<rect width="1280" height="720" fill="#b8d9d1"/><path class="ink" d="M107 518 q176 -110 315 -48 q152 67 305 -24 q148 -89 352 -31 v175H107z" fill="${palette.green}"/><path class="thin no-fill" d="M146 214 q202 -81 417 -20 q224 64 472 -34 M182 356 q214 -73 424 0 q219 76 480 -22"/><circle class="ink" cx="726" cy="302" r="34" fill="${palette.coral}"/>`],
    ["dashboard.svg", `<rect width="1280" height="720" fill="#dfecef"/><rect class="ink" x="95" y="92" width="1090" height="525" rx="26" fill="${palette.cream}"/><rect class="thin" x="145" y="145" width="295" height="160" rx="18" fill="${palette.sky}"/><rect class="thin" x="485" y="145" width="295" height="160" rx="18" fill="${palette.gold}"/><rect class="thin" x="825" y="145" width="295" height="160" rx="18" fill="${palette.green}"/><path class="thin no-fill" d="M165 512 h880 M220 470 v42 M325 430 v82 M430 390 v122 M535 455 v57 M640 350 v162 M745 410 v102 M850 370 v142 M955 448 v64"/>`],
    ["courtroom.svg", `<rect width="1280" height="720" fill="#c99b71"/><rect x="0" y="500" width="1280" height="220" fill="#8f6a4f"/><rect class="ink" x="355" y="190" width="570" height="190" rx="18" fill="${palette.tan}"/><rect class="ink" x="435" y="380" width="410" height="130" rx="18" fill="${palette.slate}"/><path class="thin no-fill" d="M420 250 h440 M475 314 h330"/><circle class="thin" cx="640" cy="132" r="50" fill="${palette.gold}"/>`],
    ["abstract-grid.svg", `<rect width="1280" height="720" fill="#efe4c7"/><g opacity=".55"><path class="thin no-fill" d="M0 120 h1280 M0 240 h1280 M0 360 h1280 M0 480 h1280 M0 600 h1280 M160 0 v720 M320 0 v720 M480 0 v720 M640 0 v720 M800 0 v720 M960 0 v720 M1120 0 v720"/></g><circle class="ink" cx="880" cy="260" r="95" fill="${palette.purple}"/><rect class="ink" x="220" y="250" width="310" height="180" rx="30" fill="${palette.sky}"/>`],
    ["newsroom.svg", `<rect width="1280" height="720" fill="#c9dde2"/><rect x="0" y="492" width="1280" height="228" fill="${palette.slate}"/><rect class="ink" x="86" y="86" width="510" height="300" rx="24" fill="${palette.cream}"/><rect class="ink" x="700" y="112" width="410" height="250" rx="24" fill="${palette.blue}"/><path class="thin no-fill" d="M140 160 h390 M140 220 h310 M140 280 h350 M754 180 h298 M754 240 h220 M754 300 h260"/><rect class="ink" x="415" y="456" width="450" height="80" rx="22" fill="${palette.coral}"/>`],
    ["podcast-studio.svg", `<rect width="1280" height="720" fill="#dfc2d8"/><rect x="0" y="500" width="1280" height="220" fill="#786f86"/><rect class="ink" x="130" y="116" width="330" height="260" rx="24" fill="${palette.cream}"/><rect class="ink" x="820" y="120" width="260" height="260" rx="24" fill="${palette.slate}"/><circle class="thin" cx="640" cy="310" r="96" fill="${palette.gold}"/><path class="thin no-fill" d="M640 125 v142 M595 265 q45 42 90 0 M872 190 h155 M872 250 h125"/>`],
    ["hospital.svg", `<rect width="1280" height="720" fill="#d8eef0"/><rect x="0" y="510" width="1280" height="210" fill="#bad1c7"/><rect class="ink" x="160" y="118" width="400" height="360" rx="24" fill="${palette.cream}"/><rect class="ink" x="760" y="160" width="310" height="300" rx="24" fill="${palette.white}"/><path class="ink" d="M336 210 h54 v-54 h62 v54 h54 v62 h-54 v54 h-62 v-54 h-54z" fill="${palette.coral}"/><path class="thin no-fill" d="M820 230 h190 M820 292 h150 M820 354 h170"/>`],
    ["library.svg", `<rect width="1280" height="720" fill="#ead4aa"/><rect x="0" y="512" width="1280" height="208" fill="#9c7250"/><rect class="ink" x="90" y="100" width="350" height="380" rx="18" fill="${palette.tan}"/><rect class="ink" x="820" y="100" width="350" height="380" rx="18" fill="${palette.tan}"/><g>${Array.from({ length: 5 }, (_, y) => `<path class="thin no-fill" d="M125 ${158 + y * 58} h280 M855 ${158 + y * 58} h280"/>`).join("")}</g><rect class="ink" x="510" y="330" width="240" height="110" rx="18" fill="${palette.cream}"/>`],
    ["factory.svg", `<rect width="1280" height="720" fill="#c9d8dd"/><rect x="0" y="510" width="1280" height="210" fill="#858f91"/><path class="ink" d="M100 505 V260 l160 82 v-82 l160 82 v-82 l160 82 v163z" fill="${palette.slate}"/><rect class="ink" x="760" y="188" width="260" height="317" rx="18" fill="${palette.cream}"/><path class="thin no-fill" d="M155 425 h370 M805 248 h170 M805 310 h170 M805 372 h170"/><circle class="thin" cx="1040" cy="160" r="52" fill="${palette.gold}"/>`],
    ["internet-map.svg", `<rect width="1280" height="720" fill="#cfe9e2"/><path class="thin no-fill" d="M188 192 q210 -120 430 0 q230 124 470 0 M180 500 q240 -130 450 0 q235 135 470 -10 M240 330 h780"/><circle class="ink" cx="250" cy="330" r="54" fill="${palette.sky}"/><circle class="ink" cx="640" cy="330" r="70" fill="${palette.gold}"/><circle class="ink" cx="1020" cy="330" r="54" fill="${palette.green}"/><path class="thin no-fill" d="M304 330 h266 M710 330 h256"/>`],
    ["whiteboard-room.svg", `<rect width="1280" height="720" fill="#e8dcc4"/><rect x="0" y="510" width="1280" height="210" fill="#c1a889"/><rect class="ink" x="135" y="90" width="760" height="350" rx="20" fill="${palette.white}"/><path class="thin no-fill" d="M205 178 h270 M205 244 h420 M205 310 h310"/><circle class="thin" cx="710" cy="260" r="72" fill="${palette.sky}"/><rect class="ink" x="965" y="155" width="150" height="240" rx="18" fill="${palette.gold}"/>`],
    ["data-center.svg", `<rect width="1280" height="720" fill="#d4e3e8"/><rect x="0" y="520" width="1280" height="200" fill="#96a6ad"/><rect class="ink" x="140" y="110" width="220" height="400" rx="22" fill="${palette.slate}"/><rect class="ink" x="530" y="110" width="220" height="400" rx="22" fill="${palette.slate}"/><rect class="ink" x="920" y="110" width="220" height="400" rx="22" fill="${palette.slate}"/><g>${[190, 580, 970].map((x) => `<circle cx="${x}" cy="180" r="12" fill="${palette.green}"/><circle cx="${x}" cy="250" r="12" fill="${palette.gold}"/><circle cx="${x}" cy="320" r="12" fill="${palette.coral}"/><path class="thin no-fill" d="M225 180 h85 M615 180 h85 M1005 180 h85 M225 250 h85 M615 250 h85 M1005 250 h85"/>`).join("")}</g>`],
    ["museum.svg", `<rect width="1280" height="720" fill="#f0dfc1"/><rect x="0" y="520" width="1280" height="200" fill="#bca782"/><path class="ink" d="M230 500 V250 h820 v250z" fill="${palette.cream}"/><path class="ink" d="M190 250 l450 -130 l450 130z" fill="${palette.tan}"/><path class="thin no-fill" d="M330 500 V290 M480 500 V290 M640 500 V290 M800 500 V290 M950 500 V290"/><rect class="thin" x="540" y="340" width="200" height="110" rx="16" fill="${palette.sky}"/>`],
    ["forest-field.svg", `<rect width="1280" height="720" fill="#bee4e8"/><rect x="0" y="490" width="1280" height="230" fill="${palette.green}"/><circle class="ink" cx="230" cy="300" r="100" fill="${palette.mint}"/><circle class="ink" cx="430" cy="330" r="130" fill="${palette.green}"/><circle class="ink" cx="930" cy="310" r="118" fill="${palette.mint}"/><path class="ink no-fill" d="M230 392 v148 M430 454 v118 M930 420 v130"/><path class="thin no-fill" d="M145 565 q235 -80 455 0 q245 88 520 -10"/>`],
  ];
  for (const [rel, body] of backgroundBodies) {
    await saveAsset(`backgrounds/${rel}`, "background", [rel.replace(".svg", "")], background(rel, body));
  }

  const textureBodies = [
    ["paper-grain.svg", `<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" seed="31"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .18"/></feComponentTransfer></filter><rect width="1280" height="720" filter="url(#grain)" opacity=".55"/>`],
    ["halftone-dots.svg", `<g fill="${palette.ink}" opacity=".1">${Array.from({ length: 13 }, (_, y) => Array.from({ length: 22 }, (_, x) => `<circle cx="${40 + x * 58}" cy="${38 + y * 54}" r="${3 + ((x + y) % 4)}"/>`).join("")).join("")}</g>`],
    ["diagonal-hatch.svg", `<g stroke="${palette.ink}" stroke-width="3" opacity=".08">${Array.from({ length: 33 }, (_, i) => `<path d="M${i * 55 - 420} 720 L${i * 55 + 300} 0"/>`).join("")}</g>`],
    ["soft-vignette.svg", `<radialGradient id="v" cx="50%" cy="50%" r="72%"><stop offset="55%" stop-color="${palette.ink}" stop-opacity="0"/><stop offset="100%" stop-color="${palette.ink}" stop-opacity=".18"/></radialGradient><rect width="1280" height="720" fill="url(#v)"/>`],
    ["speckle.svg", `<g fill="${palette.ink}" opacity=".09">${Array.from({ length: 180 }, (_, i) => `<circle cx="${(i * 197) % 1280}" cy="${(i * 113) % 720}" r="${1 + (i % 4)}"/>`).join("")}</g>`],
    ["fold-lines.svg", `<g stroke="${palette.ink}" stroke-width="4" opacity=".07"><path d="M0 180 h1280 M0 360 h1280 M0 540 h1280 M320 0 v720 M640 0 v720 M960 0 v720"/></g>`],
    ["comic-burst.svg", `<g fill="none" stroke="${palette.gold}" stroke-width="18" stroke-linecap="round" opacity=".22">${Array.from({ length: 18 }, (_, i) => {
      const angle = (Math.PI * 2 * i) / 18;
      const x1 = 640 + Math.cos(angle) * 90;
      const y1 = 360 + Math.sin(angle) * 90;
      const x2 = 640 + Math.cos(angle) * 620;
      const y2 = 360 + Math.sin(angle) * 340;
      return `<path d="M${x1.toFixed(1)} ${y1.toFixed(1)} L${x2.toFixed(1)} ${y2.toFixed(1)}"/>`;
    }).join("")}</g>`],
    ["scanlines.svg", `<g stroke="${palette.ink}" stroke-width="2" opacity=".06">${Array.from({ length: 36 }, (_, i) => `<path d="M0 ${i * 20} h1280"/>`).join("")}</g>`],
  ];
  for (const [rel, body] of textureBodies) {
    await saveAsset(`textures/${rel}`, "texture", [rel.replace(".svg", "")], texture(rel, body));
  }

  const manifest = {
    generatedAt: new Date().toISOString(),
    totalAssets: assets.length,
    assets,
  };
  await writeFile(path.join(root, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);

  const catalog = [
    "# Cartoon Starter Asset Catalog",
    "",
    `Generated assets: ${assets.length}`,
    "",
    "| Asset | Type | Tags |",
    "|---|---|---|",
    ...assets.map((asset) => `| \`${asset.path}\` | ${asset.type} | ${asset.tags.join(", ")} |`),
    "",
  ].join("\n");
  await writeFile(path.join(root, "CATALOG.md"), catalog);
}

await main();
