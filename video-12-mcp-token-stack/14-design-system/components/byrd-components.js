window.ByrdComponents = (() => {
  function trafficLights() {
    return '<div class="traffic"><span class="r"></span><span class="y"></span><span class="g"></span></div>';
  }

  function sourceBadge({ code, label }) {
    return `
      <div class="source-badge" data-animate="source-badge">
        <div class="source-badge-dot">${code}</div>
        <div class="source-badge-label">${label}</div>
      </div>
    `;
  }

  function browserMock({ url, meta, title, body, quote }) {
    return `
      <div class="browser" data-animate="browser">
        <div class="browser-chrome">
          ${trafficLights()}
          <div class="url-bar">
            <span class="url-lock">●</span>
            ${url}
          </div>
        </div>
        <div class="browser-body">
          <div class="post-meta">${meta}</div>
          <div class="post-title">${title}</div>
          <div class="post-body">${body}</div>
          <div class="post-quote">${quote}</div>
          <div class="evidence-highlight" data-animate="highlight"></div>
        </div>
      </div>
    `;
  }

  function metricCounter({ from, to, label, sub }) {
    return `
      <div class="metric" data-animate="metric">
        <div class="metric-label-top">CONTEXT COST</div>
        <div class="metric-from" data-counter-from>${from}</div>
        <div class="metric-arrow">↓</div>
        <div class="metric-to" data-counter-to>${to}</div>
        <div class="metric-label-bottom">${label}</div>
        <div class="metric-sub">${sub}</div>
      </div>
    `;
  }

  function eventCard(items) {
    return `
      <div class="event-card" data-animate="event-card">
        ${items.map((item) => `
          <div class="event-item">
            <div class="event-kicker">${item.kicker}</div>
            <div class="event-text">${item.text}</div>
          </div>
        `).join("")}
      </div>
    `;
  }

  function thesisBar({ label, text }) {
    return `
      <div class="thesis" data-animate="thesis">
        <div class="thesis-label">${label}</div>
        <div class="thesis-text">${text}</div>
      </div>
    `;
  }

  function slate(text) {
    return `<div class="slate">${text}</div>`;
  }

  function terminalMock({ title = "~/jarvis — zsh", lines = [] }) {
    return `
      <div class="terminal-mock" data-component="terminal-mock">
        <div class="terminal-titlebar">
          ${trafficLights()}
          <div class="terminal-title">${title}</div>
        </div>
        <div class="terminal-body">
          ${lines.map((line) => `<div class="terminal-line">${line}</div>`).join("")}
        </div>
      </div>
    `;
  }

  function vscodeMock({ title = "JARVIS / MCP-STACK", files = [], activeFile = "", codeLines = [], terminalLines = [] }) {
    return `
      <div class="vscode-mock" data-component="vscode-mock">
        <div class="vscode-titlebar">
          ${trafficLights()}
          <div class="vscode-title">${title}</div>
        </div>
        <div class="vscode-activity"><span>⌘</span><span>⌕</span><span>⑂</span></div>
        <div class="vscode-sidebar">
          <div class="vscode-side-title">Explorer</div>
          ${files.map((file) => `<div class="vscode-file ${file === activeFile ? "active" : ""}">${file}</div>`).join("")}
        </div>
        <div class="vscode-editor">
          ${codeLines.map((line) => `<span class="vscode-code-line">${line}</span>`).join("")}
        </div>
        <div class="vscode-terminal">
          ${terminalLines.map((line) => `<div class="terminal-line">${line}</div>`).join("")}
        </div>
      </div>
    `;
  }

  function comparisonSplit({ leftTitle, rightTitle, left, right, caption = "" }) {
    return `
      <div class="comparison-split" data-component="comparison-split">
        <div class="comparison-pane good">
          <div class="comparison-label">${leftTitle}</div>
          ${left}
        </div>
        <div class="comparison-pane bad">
          <div class="comparison-label">${rightTitle}</div>
          ${right}
        </div>
        ${caption ? `<div class="comparison-caption">${caption}</div>` : ""}
      </div>
    `;
  }

  function sideAvatarFrame({ side = "left", avatarSrc = "", label = "Avatar", content = "" }) {
    const avatar = avatarSrc
      ? `<video src="${avatarSrc}" muted playsinline></video>`
      : `<div class="avatar-placeholder">${label}</div>`;
    return `
      <div class="side-avatar-frame ${side === "right" ? "right" : "left"}" data-component="side-avatar-frame">
        <div class="avatar-slot">${avatar}</div>
        <div class="avatar-content">${content}</div>
      </div>
    `;
  }

  function phoneMock({ title, items = [] }) {
    return `
      <div class="phone-mock" data-component="phone-mock">
        <div class="phone-notch"></div>
        <div class="phone-screen">
          <div class="phone-title">${title}</div>
          ${items.map((item) => `<div class="phone-item">${item}</div>`).join("")}
        </div>
      </div>
    `;
  }

  function dashboardPanel({ title, metrics = [], bars = [] }) {
    return `
      <div class="dashboard-panel" data-component="dashboard-panel">
        <div class="dashboard-title">${title}</div>
        <div class="dashboard-metrics">
          ${metrics.map((metric) => `
            <div class="dashboard-metric">
              <div class="dashboard-metric-label">${metric.label}</div>
              <div class="dashboard-metric-value">${metric.value}</div>
            </div>
          `).join("")}
        </div>
        <div class="dashboard-chart">
          ${bars.map((bar) => `<div class="dashboard-bar" style="height:${bar}%"></div>`).join("")}
        </div>
      </div>
    `;
  }

  function lowerThird({ eyebrow, title, subtitle = "" }) {
    return `
      <div class="lower-third" data-component="lower-third">
        <div class="lower-third-eyebrow">${eyebrow}</div>
        <div class="lower-third-title">${title}</div>
        ${subtitle ? `<div class="lower-third-subtitle">${subtitle}</div>` : ""}
      </div>
    `;
  }

  function ctaControls(items = []) {
    return `
      <div class="cta-controls" data-component="cta-controls">
        ${items.map((item) => `
          <div class="cta-item">
            <div class="cta-icon">${item.icon}</div>
            <div class="cta-title">${item.title}</div>
            <div class="cta-copy">${item.copy}</div>
          </div>
        `).join("")}
      </div>
    `;
  }

  function decisionTable({ columns = [], rows = [] }) {
    return `
      <div class="decision-table" data-component="decision-table">
        <div class="decision-row header">
          ${columns.map((column) => `<div>${column}</div>`).join("")}
        </div>
        ${rows.map((row) => `
          <div class="decision-row">
            ${row.map((cell, index) => `<div>${index === 0 ? `<strong>${cell}</strong>` : cell}</div>`).join("")}
          </div>
        `).join("")}
      </div>
    `;
  }

  function architectureLayers({ layers = [], ports = [] }) {
    return `
      <div class="architecture-map" data-component="architecture-layers">
        <div class="architecture-layers">
          ${layers.map((layer) => `
            <div class="architecture-layer">
              <div class="architecture-layer-title">${layer.title}</div>
              <div class="architecture-layer-copy">${layer.copy}</div>
            </div>
          `).join("")}
        </div>
        <div class="architecture-ports">
          ${ports.map((port) => `<div class="architecture-port">${port}</div>`).join("")}
        </div>
      </div>
    `;
  }

  function evidenceMosaic(tiles = []) {
    return `
      <div class="evidence-mosaic" data-component="evidence-mosaic">
        ${tiles.map((tile) => `
          <div class="evidence-tile">
            <div class="evidence-thumb">${tile.src ? `<img src="${tile.src}" alt="">` : ""}</div>
            <div class="evidence-label">${tile.label}</div>
          </div>
        `).join("")}
      </div>
    `;
  }

  function buildComponentGalleryContent() {
    return `
      <div class="gallery-title">
        <h1>Byrddynasty Video Components</h1>
        <p>Reusable HyperFrames building blocks for Video 12 and future technical explainers.</p>
      </div>
      <div class="component-gallery-grid">
        <div class="component-demo">
          <div class="component-demo-title">TerminalMock</div>
          ${terminalMock({
            lines: [
              `<span class="prompt">$</span> jarvis-price stage QQQ --json`,
              `{ <span class="code-blue">"stage"</span>: <span class="code-amber">"markup"</span>, <span class="code-blue">"score"</span>: <span class="code-green">87</span> }`,
              `<span class="code-green">✓</span> done in 142ms`
            ]
          })}
        </div>
        <div class="component-demo">
          <div class="component-demo-title">VSCodeMock</div>
          ${vscodeMock({
            files: ["mcp-config.json", "SKILL.md", "token-audit.ts"],
            activeFile: "SKILL.md",
            codeLines: [
              `<span class="code-green"># MCP Token Stack Skill</span>`,
              `Use MCP for permissioned systems.`,
              `Use skills for procedural knowledge.`,
              `Use CLI scripts for deterministic local work.`
            ],
            terminalLines: [
              `<span class="prompt">$</span> hyperframes render`,
              `<span class="code-green">✓</span> render complete`
            ]
          })}
        </div>
        <div class="component-demo">
          <div class="component-demo-title">ComparisonSplit</div>
          ${comparisonSplit({
            leftTitle: "CLI",
            rightTitle: "MCP",
            left: `<p>1,365 tokens<br><span class="code-green">local deterministic work</span></p>`,
            right: `<p>44,026 tokens<br><span class="code-red">schema load overhead</span></p>`,
            caption: "Same task, different route."
          })}
        </div>
        <div class="component-demo">
          <div class="component-demo-title">PhoneMock</div>
          ${phoneMock({
            title: "JARVIS Alert",
            items: ["Digest ready", "MACD changed", "Review source evidence"]
          })}
        </div>
        <div class="component-demo">
          <div class="component-demo-title">DashboardPanel</div>
          ${dashboardPanel({
            title: "Token Budget",
            metrics: [{ label: "MCP", value: "77K" }, { label: "Search", value: "8.7K" }, { label: "Code", value: "1K" }],
            bars: [90, 42, 18, 64, 30, 74]
          })}
        </div>
        <div class="component-demo">
          <div class="component-demo-title">DecisionTable</div>
          ${decisionTable({
            columns: ["Layer", "Problem", "Better Output", "Use When"],
            rows: [
              ["MCP", "External access", "Permission boundary", "Products"],
              ["Skill", "Procedure", "Reusable instructions", "Workflows"],
              ["CLI", "Local task", "Deterministic result", "Your machine"]
            ]
          })}
        </div>
        <div class="component-demo">
          <div class="component-demo-title">ArchitectureLayers</div>
          ${architectureLayers({
            layers: [
              { title: "Wiki memory", copy: "Persistent knowledge" },
              { title: "Skills + scripts", copy: "Procedures and local actions" },
              { title: "Agent orchestration", copy: "Reasoning and routing" }
            ],
            ports: ["MCP services", "Scheduled jobs"]
          })}
        </div>
        <div class="component-demo">
          <div class="component-demo-title">EvidenceMosaic + CTA</div>
          ${evidenceMosaic([
            { label: "Cloudflare" },
            { label: "Anthropic" },
            { label: "Scalekit" }
          ])}
        </div>
      </div>
    `;
  }

  function segmentShell({ id, children }) {
    return `
      <div data-composition-id="${id}" data-width="1920" data-height="1080">
        <div class="byrd-scene">
          ${children}
        </div>
      </div>
    `;
  }

  function buildSegment07Content() {
    const body = `
      Instead of injecting every tool's schema into the model context, expose two primitives —
      <span class="code-pill">search()</span> and <span class="code-pill">execute()</span> —
      then let the agent discover what it needs.
    `;

    return `
        ${sourceBadge({ code: "CF", label: "CLOUDFLARE · CODE MODE" })}
        ${browserMock({
          url: "blog.cloudflare.com/code-mode",
          meta: "CLOUDFLARE WORKERS · ENGINEERING",
          title: "Code Mode: give Claude code, not tools.",
          body,
          quote: `"Discover, inspect, execute, return." The agent reads its own code, not 1.17 million tokens of someone else's documentation.`
        })}
        ${metricCounter({
          from: "1,170,000",
          to: "1,000",
          label: "input tokens with Code Mode",
          sub: "99.91% reduction · source: Cloudflare Workers"
        })}
        ${eventCard([
          { kicker: "Step 1", text: "Search the API surface" },
          { kicker: "Step 2", text: "Inspect only what matters" },
          { kicker: "Step 3", text: "Execute in a sandbox" },
          { kicker: "Step 4", text: "Return the result" }
        ])}
        ${thesisBar({
          label: "THE LAYER QUESTION",
          text: "The context window should carry reasoning, not every possible instruction manual."
        })}
        ${slate("SEG 07 · 172.50 → 199.10 · CLOUDFLARE SOURCE")}
      `;
  }

  function buildSegment07() {
    return segmentShell({
      id: "segment-07-cloudflare-proof",
      children: buildSegment07Content()
    });
  }

  function buildComponentGallery() {
    return segmentShell({
      id: "component-gallery",
      children: buildComponentGalleryContent()
    });
  }

  function animateComponentGallery() {
    const tl = gsap.timeline({ paused: true });
    tl.from(".gallery-title", { y: 24, opacity: 0, duration: 0.55, ease: "power3.out" }, 0.1);
    tl.from(".component-demo", { y: 24, opacity: 0, duration: 0.45, stagger: 0.08, ease: "power3.out" }, 0.45);
    return tl;
  }

  function animateSegment07() {
    const tl = gsap.timeline({ paused: true });

    tl.from("[data-animate='source-badge']", { y: -20, opacity: 0, duration: 0.55, ease: "power3.out" }, 0.15);
    tl.from("[data-animate='browser']", { y: 48, scale: 0.975, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.55);
    tl.from(".post-meta, .post-title, .post-body, .post-quote", {
      y: 24,
      opacity: 0,
      duration: 0.52,
      stagger: 0.18,
      ease: "power3.out"
    }, 1.2);

    tl.from("[data-animate='metric']", { x: 52, opacity: 0, duration: 0.7, ease: "power3.out" }, 5.0);
    tl.from("[data-counter-from]", { scale: 1.12, opacity: 0, duration: 0.45, ease: "back.out(1.5)" }, 5.65);
    tl.from("[data-counter-to]", { scale: 0.76, opacity: 0, duration: 0.7, ease: "back.out(1.6)" }, 7.0);
    tl.to("[data-counter-to]", { scale: 1.035, duration: 0.18, yoyo: true, repeat: 1, ease: "power1.inOut" }, 8.1);

    tl.to("[data-animate='highlight']", { opacity: 1, duration: 0.25, ease: "power2.out" }, 9.0);
    tl.to("[data-animate='highlight']", { x: 138, duration: 1.1, ease: "power2.inOut" }, 10.35);
    tl.to("[data-animate='highlight']", { opacity: 0, duration: 0.25, ease: "power2.in" }, 12.2);

    tl.from(".event-item", {
      y: 24,
      opacity: 0,
      duration: 0.44,
      stagger: 0.28,
      ease: "power3.out"
    }, 13.4);

    tl.from("[data-animate='thesis']", { y: 34, opacity: 0, duration: 0.65, ease: "power3.out" }, 18.2);
    tl.from(".thesis-text", { y: 18, opacity: 0, duration: 0.45, ease: "power3.out" }, 18.75);

    tl.to(".browser, .metric, .event-card, .thesis, .source-badge", {
      opacity: 0,
      y: -18,
      duration: 0.45,
      stagger: 0.035,
      ease: "power2.in"
    }, 25.85);

    return tl;
  }

  return {
    buildSegment07,
    buildSegment07Content,
    buildComponentGallery,
    buildComponentGalleryContent,
    animateSegment07,
    animateComponentGallery,
    architectureLayers,
    browserMock,
    comparisonSplit,
    ctaControls,
    dashboardPanel,
    decisionTable,
    evidenceMosaic,
    eventCard,
    lowerThird,
    metricCounter,
    phoneMock,
    sourceBadge,
    sideAvatarFrame,
    terminalMock,
    vscodeMock,
    thesisBar
  };
})();
