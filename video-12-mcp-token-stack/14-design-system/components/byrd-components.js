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
    animateSegment07,
    browserMock,
    eventCard,
    metricCounter,
    sourceBadge,
    thesisBar
  };
})();
