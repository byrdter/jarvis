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
  "characters/expressions",
  "props/science",
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

  const poses = [
    ["neutral", "neutral", "rest", null],
    ["happy", "happy", "rest", null],
    ["thinking", "thinking", "hold", "book"],
    ["worried", "worried", "rest", null],
    ["shocked", "shocked", "rest", null],
    ["point-left", "neutral", "point-left", "pointer"],
    ["point-right", "neutral", "point-right", "pointer"],
    ["explaining-card", "happy", "hold", "card"],
  ];

  for (const [name, expression, arm, prop] of poses) {
    await saveAsset(`characters/host-a/poses/${name}.svg`, "character-pose", ["host-a", expression, arm].filter(Boolean), poseSvg({
      name,
      host: "host-a",
      skin: palette.skinC,
      hair: palette.hairA,
      shirt: palette.blue,
      pants: palette.purple,
      expression,
      arm,
      prop,
    }));
    await saveAsset(`characters/host-b/poses/${name}.svg`, "character-pose", ["host-b", expression, arm].filter(Boolean), poseSvg({
      name,
      host: "host-b",
      skin: palette.skinB,
      hair: palette.hairB,
      shirt: palette.green,
      pants: palette.slate,
      expression,
      arm,
      prop,
      mirror: name === "point-left",
    }));
  }

  const expressions = [
    ["host-a-neutral", palette.skinC, palette.hairA, "neutral"],
    ["host-a-happy", palette.skinC, palette.hairA, "happy"],
    ["host-a-thinking", palette.skinC, palette.hairA, "thinking"],
    ["host-a-worried", palette.skinC, palette.hairA, "worried"],
    ["host-a-shocked", palette.skinC, palette.hairA, "shocked"],
    ["host-a-skeptical", palette.skinC, palette.hairA, "skeptical"],
    ["host-a-angry", palette.skinC, palette.hairA, "angry"],
    ["host-a-confused", palette.skinC, palette.hairA, "confused"],
    ["host-a-tired", palette.skinC, palette.hairA, "tired"],
    ["host-a-excited", palette.skinC, palette.hairA, "excited"],
    ["host-b-neutral", palette.skinB, palette.hairB, "neutral"],
    ["host-b-happy", palette.skinB, palette.hairB, "happy"],
    ["host-b-thinking", palette.skinB, palette.hairB, "thinking"],
    ["host-b-worried", palette.skinB, palette.hairB, "worried"],
    ["host-b-shocked", palette.skinB, palette.hairB, "shocked"],
    ["host-b-skeptical", palette.skinB, palette.hairB, "skeptical"],
    ["host-b-angry", palette.skinB, palette.hairB, "angry"],
    ["host-b-confused", palette.skinB, palette.hairB, "confused"],
    ["host-b-tired", palette.skinB, palette.hairB, "tired"],
    ["host-b-excited", palette.skinB, palette.hairB, "excited"],
  ];
  for (const [name, skin, hair, expression] of expressions) {
    await saveAsset(`characters/expressions/${name}.svg`, "expression", [name.split("-").slice(0, 2).join("-"), expression], expressionSvg({ name, skin, hair, expression }));
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
