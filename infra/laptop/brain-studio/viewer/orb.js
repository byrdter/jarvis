// The JARVIS orb: a living entity drawn on a 2D canvas.
//
// Core is always JARVIS gold; the aura takes the color of the brain doing the thinking (palette from
// reference_brain_color_palettes: Claude #d97757, local models green). How it moves tells you who is
// talking:
//   idle       slow breathing
//   listening  the edge ripples with the REAL microphone level (setLevel, from an AnalyserNode)
//   thinking   inner arcs spin up and one satellite orbits per note being read
//   speaking   a pulse on every spoken word (kick, from SpeechSynthesis boundary events)
//   error      a red flicker
// No dependencies. One requestAnimationFrame loop; it sleeps when the tab is hidden.

export const ENGINES = {
  claude: { name: 'Claude', color: '#d97757' },
  local:  { name: 'Local',  color: '#4ade80' },
};
const GOLD = '#ffd700';

export function createOrb(canvas) {
  const ctx = canvas.getContext('2d');
  const st = { state: 'idle', engine: 'claude', level: 0, energy: 0, spin: 0, sats: 0, t0: performance.now() };
  let dpr = 1, size = 0;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    size = canvas.clientWidth;
    canvas.width = size * dpr; canvas.height = size * dpr;
  }
  resize();
  new ResizeObserver(resize).observe(canvas);

  const rgba = (hex, a) => {
    const n = parseInt(hex.slice(1), 16);
    return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`;
  };

  function frame(now) {
    const t = (now - st.t0) / 1000;
    const c = ENGINES[st.engine]?.color || ENGINES.claude.color;
    const err = st.state === 'error';
    const aura = err ? '#f87171' : c;

    // Energy: what drives the wobble. Listening follows the mic; speaking decays between word kicks.
    const target = st.state === 'listening' ? 0.15 + st.level * 1.6
                 : st.state === 'thinking' ? 0.35
                 : st.state === 'speaking' ? 0.2
                 : err ? 0.3 + 0.3 * (Math.sin(t * 30) > 0.6 ? 1 : 0)
                 : 0.08;
    st.energy += (target - st.energy) * (st.state === 'speaking' ? 0.08 : 0.15);
    st.spin += (st.state === 'thinking' ? 2.6 : st.state === 'speaking' ? 0.9 : 0.25) / 60;

    const W = size * dpr, cx = W / 2, cy = W / 2;
    const breathe = 1 + Math.sin(t * 1.3) * 0.025;
    const R = W * 0.25 * breathe * (1 + st.energy * 0.12);
    ctx.clearRect(0, 0, W, W);

    // Outer halo.
    const halo = ctx.createRadialGradient(cx, cy, R * 0.6, cx, cy, W * 0.5);
    halo.addColorStop(0, rgba(aura, 0.30 + st.energy * 0.25));
    halo.addColorStop(0.5, rgba(aura, 0.08 + st.energy * 0.08));
    halo.addColorStop(1, rgba(aura, 0));
    ctx.fillStyle = halo;
    ctx.fillRect(0, 0, W, W);

    // Living edge: a blob whose ripples grow with energy.
    const amp = 0.025 + st.energy * 0.11;
    ctx.beginPath();
    for (let i = 0; i <= 96; i++) {
      const a = (i / 96) * Math.PI * 2;
      const r = R * (1
        + amp * Math.sin(3 * a + t * 1.7)
        + amp * 0.6 * Math.sin(5 * a - t * 2.3 + 1.1)
        + amp * 0.35 * Math.sin(8 * a + t * 3.9 + 2.0));
      const x = cx + r * Math.cos(a), y = cy + r * Math.sin(a);
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.closePath();
    const body = ctx.createRadialGradient(cx - R * 0.25, cy - R * 0.3, R * 0.05, cx, cy, R * 1.1);
    body.addColorStop(0, '#fff8d6');
    body.addColorStop(0.28, GOLD);
    body.addColorStop(0.75, aura);
    body.addColorStop(1, rgba(aura, 0.55));
    ctx.save();
    ctx.shadowColor = aura; ctx.shadowBlur = 18 * dpr + st.energy * 30 * dpr;
    ctx.fillStyle = body;
    ctx.fill();
    ctx.restore();

    // Inner arcs: the "mind" turning over.
    ctx.save();
    ctx.translate(cx, cy);
    ctx.globalCompositeOperation = 'lighter';
    for (let k = 0; k < 3; k++) {
      ctx.rotate(st.spin * (k % 2 ? -1 : 1) * (1 + k * 0.4));
      ctx.beginPath();
      ctx.arc(0, 0, R * (0.45 + k * 0.17), 0, Math.PI * (0.55 + 0.25 * Math.sin(t + k)));
      ctx.strokeStyle = rgba('#ffffff', 0.18 + st.energy * 0.35);
      ctx.lineWidth = dpr * (1.2 + k * 0.3);
      ctx.lineCap = 'round';
      ctx.stroke();
    }
    ctx.restore();

    // Listening ring: a thin mint circle that swells with the voice.
    if (st.state === 'listening') {
      ctx.beginPath();
      ctx.arc(cx, cy, R * (1.28 + st.level * 0.5), 0, Math.PI * 2);
      ctx.strokeStyle = rgba('#e6fff4', 0.35 + st.level * 0.5);
      ctx.lineWidth = 1.5 * dpr;
      ctx.stroke();
    }

    // Satellites: one per note being read while thinking.
    const n = st.state === 'thinking' ? Math.max(st.sats, 3) : 0;
    for (let i = 0; i < n; i++) {
      const a = st.spin * 1.6 + (i / n) * Math.PI * 2;
      const rr = R * (1.45 + 0.08 * Math.sin(t * 2 + i));
      ctx.beginPath();
      ctx.arc(cx + rr * Math.cos(a), cy + rr * Math.sin(a) * 0.55, 2.2 * dpr, 0, Math.PI * 2);
      ctx.fillStyle = rgba(GOLD, 0.9);
      ctx.shadowColor = GOLD; ctx.shadowBlur = 8 * dpr;
      ctx.fill();
      ctx.shadowBlur = 0;
    }

    if (!document.hidden) requestAnimationFrame(frame);
  }
  document.addEventListener('visibilitychange', () => { if (!document.hidden) requestAnimationFrame(frame); });
  requestAnimationFrame(frame);

  return {
    setState(s) { st.state = s; if (s !== 'listening') st.level = 0; },
    setEngine(e) { if (ENGINES[e]) st.engine = e; },
    get engine() { return st.engine; },
    setLevel(v) { st.level = Math.max(0, Math.min(1, v)); },
    setSatellites(k) { st.sats = k; },
    kick(v = 0.6) { st.energy = Math.min(1.4, st.energy + v); },   // one spoken word
  };
}
