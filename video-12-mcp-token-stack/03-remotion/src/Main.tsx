import React from 'react';
import {
  AbsoluteFill,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const FPS = 25;
const DURATION_SECONDS = 730.007;
export const VIDEO_DURATION_FRAMES = Math.ceil(DURATION_SECONDS * FPS);

type SegmentKind =
  | 'avatar-full'
  | 'avatar-side'
  | 'source'
  | 'warning'
  | 'metric'
  | 'flow'
  | 'code'
  | 'table'
  | 'cta'
  | 'evidence';

type Segment = {
  seg: number;
  start: number;
  end: number;
  title: string;
  kind: SegmentKind;
  source?: string;
  eyebrow?: string;
  bullets?: string[];
  metrics?: Array<{label: string; value: string; tone?: 'good' | 'bad' | 'warn'}>;
};

const segments: Segment[] = [
  {seg: 1, start: 0, end: 35.04, title: 'The 2026 Agent Token Stack', kind: 'avatar-full', eyebrow: 'JARVIS'},
  {
    seg: 2,
    start: 35.04,
    end: 85.98,
    title: 'Old MCP: Context Before Work',
    kind: 'source',
    source: 'anthropic.com/engineering/advanced-tool-use',
    eyebrow: 'SOURCE PROOF',
    bullets: ['Tool definitions arrive before the task', 'The model carries overhead, not work', 'Tool Search changes the baseline'],
    metrics: [
      {label: 'Traditional setup', value: '~77K tokens', tone: 'bad'},
      {label: 'Tool Search', value: '~8.7K tokens', tone: 'good'},
      {label: 'Reduction', value: '85%+', tone: 'good'},
    ],
  },
  {
    seg: 4,
    start: 85.98,
    end: 107.54,
    title: 'The Trap',
    kind: 'warning',
    bullets: ['Schema load is not output load', 'Search is not perfect retrieval', 'Workflow data can still flood context'],
  },
  {
    seg: 5,
    start: 107.54,
    end: 139.22,
    title: 'Accuracy Is Better, Not Magical',
    kind: 'metric',
    source: 'Anthropic MCP eval + Arcade 4,027-tool stress test',
    metrics: [
      {label: 'Opus 4 MCP eval', value: '49% -> 74%', tone: 'good'},
      {label: 'Opus 4.5 MCP eval', value: '79.5% -> 88.1%', tone: 'good'},
      {label: 'Arcade stress test', value: '~60%', tone: 'warn'},
    ],
  },
  {
    seg: 6,
    start: 139.22,
    end: 172.52,
    title: 'One Layer Cannot Do Every Job',
    kind: 'avatar-side',
    bullets: ['MCP: external systems', 'Skills: procedure', 'CLI: deterministic local work', 'Code execution: data movement'],
  },
  {
    seg: 7,
    start: 172.52,
    end: 198.06,
    title: 'Cloudflare Code Mode',
    kind: 'source',
    source: 'blog.cloudflare.com/code-mode-mcp',
    bullets: ['Expose an API through search() and execute()', 'Agent writes code against a typed surface', 'Code runs inside a controlled sandbox'],
    metrics: [{label: 'Traditional MCP', value: '1.17M tokens', tone: 'bad'}, {label: 'Code Mode', value: '~1K tokens', tone: 'good'}],
  },
  {
    seg: 8,
    start: 198.06,
    end: 221.4,
    title: 'Context Should Carry Reasoning',
    kind: 'metric',
    metrics: [
      {label: 'API manual in context', value: '1,170,000', tone: 'bad'},
      {label: 'Discovery + execution', value: '1,000', tone: 'good'},
      {label: 'Reported reduction', value: '99.9%', tone: 'good'},
    ],
  },
  {
    seg: 9,
    start: 221.4,
    end: 241.68,
    title: 'Anthropic: Google Drive to Salesforce',
    kind: 'flow',
    source: 'anthropic.com/engineering/code-execution-with-mcp',
    bullets: ['Download transcript', 'Attach to Salesforce lead', 'Avoid copying intermediate data through the model'],
  },
  {
    seg: 10,
    start: 241.68,
    end: 265.56,
    title: 'The Waste Is Transport',
    kind: 'flow',
    bullets: ['Naive path: transcript enters context twice', 'Code path: transcript stays as a sandbox variable', 'Only final status returns to the model'],
  },
  {
    seg: 11,
    start: 265.56,
    end: 285.48,
    title: '150K Tokens Down to 2K',
    kind: 'metric',
    metrics: [{label: 'Direct tool calls', value: '150,000', tone: 'bad'}, {label: 'Code execution', value: '2,000', tone: 'good'}, {label: 'Reduction', value: '98.7%', tone: 'good'}],
  },
  {
    seg: 12,
    start: 285.48,
    end: 315.48,
    title: 'Important Limitation',
    kind: 'source',
    source: 'platform.claude.com/docs/.../programmatic-tool-calling',
    eyebrow: 'DOCS CALLOUT',
    bullets: ['MCP connector tools cannot be called programmatically', 'Programmatic calling is not the same as MCP Code Mode', 'MCP-heavy workflows need a wrapper or server-side execution layer'],
  },
  {
    seg: 13,
    start: 315.48,
    end: 345.48,
    title: 'No Real Sandbox, No Free Win',
    kind: 'avatar-side',
    bullets: ['No filesystem', 'No environment variables', 'External fetch disabled by default', 'Resource limits and monitoring'],
  },
  {
    seg: 17,
    start: 345.48,
    end: 373.16,
    title: 'CLI Still Wins Local Work',
    kind: 'metric',
    source: 'scalekit.com/blog/mcp-vs-cli-use',
    metrics: [{label: 'CLI agent', value: '1,365 tokens', tone: 'good'}, {label: 'MCP agent', value: '44,026 tokens', tone: 'bad'}, {label: 'Failure rate', value: '28%', tone: 'warn'}],
  },
  {
    seg: 18,
    start: 373.16,
    end: 399.66,
    title: 'But MCP Has a Real Job',
    kind: 'flow',
    bullets: ['Local CLI: agent acts as us', 'MCP product: agent acts for many customers', 'Permission and audit boundaries matter'],
  },
  {
    seg: 19,
    start: 399.66,
    end: 425.38,
    title: 'Filter Tool Outputs',
    kind: 'code',
    bullets: ['Return only the fields the agent needs', 'Strip navigation, ads, and formatting', 'Do not ship full objects because they are easy'],
  },
  {
    seg: 20,
    start: 425.38,
    end: 449.3,
    title: 'TOON: Useful, Narrow',
    kind: 'table',
    bullets: ['Best: flat tabular rows', 'Risk: nested objects and very wide rows', 'Prompt overhead can eat the savings'],
  },
  {
    seg: 21,
    start: 449.3,
    end: 476.52,
    title: 'The Stack',
    kind: 'table',
    bullets: ['Direct MCP', 'Tool Search', 'Scoped MCP', 'Skills', 'CLI/scripts', 'Code execution', 'Output compression'],
  },
  {
    seg: 22,
    start: 476.52,
    end: 503.44,
    title: 'The Rule We Use',
    kind: 'avatar-side',
    bullets: ['Permissioned external system -> MCP', 'Procedure -> Skill', 'Local deterministic operation -> CLI', 'Large intermediate data -> Code execution'],
  },
  {
    seg: 23,
    start: 503.44,
    end: 527.06,
    title: 'JARVIS Layer Map',
    kind: 'flow',
    bullets: ['Wiki memory', 'Skills as operating procedures', 'Local scripts as reliable actions', 'Scheduled jobs as heartbeat'],
  },
  {
    seg: 24,
    start: 527.06,
    end: 552.46,
    title: 'Measurement Plan',
    kind: 'table',
    bullets: ['Naive MCP', 'Tool Search', 'JARVIS stack', 'Code execution'],
  },
  {
    seg: 25,
    start: 552.46,
    end: 573.04,
    title: 'Phase 1: Free Wins',
    kind: 'code',
    bullets: ['Check MCP token load', 'Disconnect unused servers', 'Enable Tool Search', 'Scope big MCP servers'],
  },
  {
    seg: 26,
    start: 573.04,
    end: 596.14,
    title: 'Phase 2: Move Knowledge',
    kind: 'code',
    bullets: ['CLAUDE.md -> Skills', 'Local work -> Scripts', 'Full output -> Filtered output'],
  },
  {
    seg: 27,
    start: 596.14,
    end: 619.9,
    title: 'Phase 3: Heavy Patterns',
    kind: 'flow',
    bullets: ['Programmatic tool calling where it fits', 'MCP wrappers where connectors block it', 'Sandboxing is the product'],
  },
  {
    seg: 28,
    start: 619.9,
    end: 642.18,
    title: 'Three Bad Takes',
    kind: 'warning',
    bullets: ['MCP is dead', 'MCP is fixed', 'TOON is magic'],
  },
  {
    seg: 29,
    start: 642.18,
    end: 669.24,
    title: 'Evidence Beats Opinion',
    kind: 'evidence',
    bullets: ['Cloudflare', 'Anthropic', 'Arcade', 'Scalekit', 'JARVIS'],
  },
  {
    seg: 30,
    start: 669.24,
    end: 689.64,
    title: 'Subscribe for the Next Build',
    kind: 'cta',
    bullets: ['Subscribe', 'Like', 'Ring the bell'],
  },
  {seg: 31, start: 689.64, end: 714.16, title: 'Right Layer. Right Scope.', kind: 'avatar-full'},
  {seg: 32, start: 714.16, end: 729.693, title: 'New Videos Every Week', kind: 'avatar-full'},
];

const palette = {
  bg: '#111318',
  panel: '#F7F2E8',
  ink: '#1C1D20',
  cyan: '#1CA7A8',
  blue: '#2952A3',
  green: '#2E8B57',
  red: '#B23A48',
  amber: '#D99A2B',
  white: '#FFFFFF',
};

const ease = (frame: number, input: number[], output: number[]) =>
  interpolate(frame, input, output, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

const stillSrc = (seg: number) => staticFile(`stills/${String(seg).padStart(3, '0')}.png`);

const Bg: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill
    style={{
      background: `linear-gradient(135deg, ${palette.bg}, #23262D 48%, #D6E9E7 48%, #ECE7DA)`,
      fontFamily: 'Inter, Arial, sans-serif',
      color: palette.ink,
    }}
  >
    <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(circle at 12% 18%, rgba(28,167,168,0.18), transparent 30%)'}} />
    {children}
  </AbsoluteFill>
);

const SourceBadge: React.FC<{source?: string; eyebrow?: string}> = ({source, eyebrow}) => (
  <div style={{display: 'flex', alignItems: 'center', gap: 18, fontSize: 34, fontWeight: 800, color: palette.ink}}>
    <div style={{background: palette.ink, color: palette.white, padding: '12px 20px', borderRadius: 8, letterSpacing: 1}}>
      {eyebrow ?? 'SOURCE'}
    </div>
    {source ? <div style={{fontSize: 30, color: '#565B63'}}>{source}</div> : null}
  </div>
);

const BrowserPanel: React.FC<{seg: Segment; frame: number}> = ({seg, frame}) => {
  const y = ease(frame, [0, 22], [42, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        left: 120,
        top: 100 + y,
        width: 1220,
        height: 790,
        background: palette.panel,
        border: `5px solid ${palette.ink}`,
        borderRadius: 8,
        boxShadow: '22px 22px 0 rgba(0,0,0,0.28)',
        overflow: 'hidden',
      }}
    >
      <div style={{height: 74, background: '#D8D0C3', display: 'flex', alignItems: 'center', gap: 14, padding: '0 24px'}}>
        <span style={{width: 24, height: 24, borderRadius: '50%', background: '#DC625B'}} />
        <span style={{width: 24, height: 24, borderRadius: '50%', background: '#E8B443'}} />
        <span style={{width: 24, height: 24, borderRadius: '50%', background: '#49A65B'}} />
        <div style={{marginLeft: 18, background: '#F8F5EE', borderRadius: 8, padding: '12px 18px', flex: 1, fontSize: 28, color: '#555'}}>
          https://{seg.source ?? 'source.local'}
        </div>
      </div>
      <div style={{padding: 44}}>
        <SourceBadge source={seg.source} eyebrow={seg.eyebrow} />
        <div style={{fontSize: 78, lineHeight: 1.02, marginTop: 34, fontWeight: 900, color: palette.ink}}>{seg.title}</div>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 22, marginTop: 44}}>
          {(seg.metrics ?? []).map((metric, i) => (
            <MetricCard key={metric.label} metric={metric} delay={i * 8} frame={frame} />
          ))}
        </div>
        <BulletList bullets={seg.bullets ?? []} frame={frame} />
      </div>
    </div>
  );
};

const MetricCard: React.FC<{metric: NonNullable<Segment['metrics']>[number]; frame: number; delay: number}> = ({
  metric,
  frame,
  delay,
}) => {
  const tone = metric.tone === 'good' ? palette.green : metric.tone === 'warn' ? palette.amber : palette.red;
  const scale = ease(frame - delay, [0, 14], [0.86, 1]);
  return (
    <div
      style={{
        transform: `scale(${scale})`,
        transformOrigin: 'center',
        border: `4px solid ${tone}`,
        background: '#FFFFFF',
        borderRadius: 8,
        padding: 24,
        minHeight: 150,
      }}
    >
      <div style={{fontSize: 28, color: '#5A5F66', fontWeight: 700}}>{metric.label}</div>
      <div style={{fontSize: 54, color: tone, fontWeight: 950, marginTop: 10}}>{metric.value}</div>
    </div>
  );
};

const BulletList: React.FC<{bullets: string[]; frame: number; color?: string}> = ({bullets, frame, color = palette.ink}) => (
  <div style={{display: 'grid', gap: 18, marginTop: 42}}>
    {bullets.map((bullet, i) => {
      const x = ease(frame - 10 - i * 7, [0, 16], [-40, 0]);
      const opacity = ease(frame - 10 - i * 7, [0, 16], [0, 1]);
      return (
        <div key={bullet} style={{display: 'flex', alignItems: 'center', gap: 18, transform: `translateX(${x}px)`, opacity}}>
          <div style={{width: 18, height: 18, background: palette.cyan, borderRadius: 2}} />
          <div style={{fontSize: 42, lineHeight: 1.13, fontWeight: 750, color}}>{bullet}</div>
        </div>
      );
    })}
  </div>
);

const WarningShot: React.FC<{seg: Segment; frame: number}> = ({seg, frame}) => (
  <Bg>
    <div style={{position: 'absolute', left: 120, top: 90, color: palette.white}}>
      <div style={{fontSize: 42, color: '#F3D27A', fontWeight: 900}}>AVOID THE EASY TAKE</div>
      <div style={{fontSize: 96, lineHeight: 1.02, fontWeight: 950, maxWidth: 1080}}>{seg.title}</div>
    </div>
    <div style={{position: 'absolute', left: 130, right: 130, top: 390, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 34}}>
      {(seg.bullets ?? []).map((b, i) => (
        <div
          key={b}
          style={{
            background: i === 0 ? palette.red : i === 1 ? palette.amber : palette.blue,
            color: palette.white,
            minHeight: 280,
            padding: 36,
            borderRadius: 8,
            border: '5px solid rgba(255,255,255,0.88)',
            transform: `translateY(${ease(frame - i * 7, [0, 18], [70, 0])}px) rotate(${i === 1 ? -1.5 : i === 2 ? 1.5 : 0}deg)`,
            opacity: ease(frame - i * 7, [0, 18], [0, 1]),
          }}
        >
          <div style={{fontSize: 100, fontWeight: 950}}>0{i + 1}</div>
          <div style={{fontSize: 48, lineHeight: 1.08, fontWeight: 900}}>{b}</div>
        </div>
      ))}
    </div>
  </Bg>
);

const MetricShot: React.FC<{seg: Segment; frame: number}> = ({seg, frame}) => (
  <Bg>
    <div style={{position: 'absolute', left: 100, top: 80, right: 100}}>
      <SourceBadge source={seg.source} eyebrow="NUMBERS" />
      <div style={{fontSize: 92, fontWeight: 950, color: palette.white, lineHeight: 1.02, marginTop: 32}}>{seg.title}</div>
      <div style={{display: 'grid', gridTemplateColumns: `repeat(${seg.metrics?.length ?? 3}, 1fr)`, gap: 34, marginTop: 80}}>
        {(seg.metrics ?? []).map((m, i) => <MetricCard key={m.label} metric={m} frame={frame} delay={i * 12} />)}
      </div>
    </div>
  </Bg>
);

const FlowShot: React.FC<{seg: Segment; frame: number}> = ({seg, frame}) => {
  const labels = seg.bullets ?? [];
  return (
    <Bg>
      <div style={{position: 'absolute', left: 110, top: 84}}>
        <SourceBadge source={seg.source} eyebrow="WORKFLOW" />
        <div style={{fontSize: 86, color: palette.white, fontWeight: 950, marginTop: 30}}>{seg.title}</div>
      </div>
      <div style={{position: 'absolute', left: 120, right: 120, top: 390, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
        {labels.map((label, i) => (
          <React.Fragment key={label}>
            <div
              style={{
                width: 360,
                minHeight: 210,
                background: i % 2 ? '#FFFFFF' : '#E8F3F0',
                border: `5px solid ${palette.ink}`,
                borderRadius: 8,
                padding: 28,
                boxShadow: '12px 12px 0 rgba(0,0,0,0.22)',
                transform: `translateY(${ease(frame - i * 10, [0, 18], [80, 0])}px)`,
                opacity: ease(frame - i * 10, [0, 18], [0, 1]),
              }}
            >
              <div style={{fontSize: 34, color: palette.cyan, fontWeight: 950}}>STEP {i + 1}</div>
              <div style={{fontSize: 44, lineHeight: 1.05, fontWeight: 900, marginTop: 14}}>{label}</div>
            </div>
            {i < labels.length - 1 ? (
              <div style={{fontSize: 76, color: palette.white, fontWeight: 950, opacity: ease(frame - i * 10 - 8, [0, 12], [0, 1])}}>{'->'}</div>
            ) : null}
          </React.Fragment>
        ))}
      </div>
    </Bg>
  );
};

const CodeShot: React.FC<{seg: Segment; frame: number}> = ({seg, frame}) => (
  <Bg>
    <div style={{position: 'absolute', left: 110, top: 80, color: palette.white}}>
      <div style={{fontSize: 86, fontWeight: 950}}>{seg.title}</div>
      <div style={{marginTop: 42, width: 1140, background: '#15191F', border: '4px solid #EEF0F2', borderRadius: 8, padding: 34}}>
        {(seg.bullets ?? []).map((line, i) => (
          <div key={line} style={{fontFamily: 'Menlo, monospace', fontSize: 42, color: i === 0 ? '#74D0C3' : '#F3EBD8', lineHeight: 1.45, opacity: ease(frame - i * 10, [0, 12], [0, 1])}}>
            <span style={{color: '#6F7882'}}>$ </span>{line}
          </div>
        ))}
      </div>
    </div>
  </Bg>
);

const TableShot: React.FC<{seg: Segment; frame: number}> = ({seg, frame}) => (
  <Bg>
    <div style={{position: 'absolute', left: 110, top: 70, right: 110}}>
      <div style={{fontSize: 84, color: palette.white, fontWeight: 950}}>{seg.title}</div>
      <div style={{marginTop: 48, background: palette.panel, border: `5px solid ${palette.ink}`, borderRadius: 8, overflow: 'hidden'}}>
        {(seg.bullets ?? []).map((row, i) => (
          <div
            key={row}
            style={{
              display: 'grid',
              gridTemplateColumns: '120px 1fr',
              alignItems: 'center',
              minHeight: 86,
              padding: '0 34px',
              borderBottom: i === (seg.bullets?.length ?? 0) - 1 ? 'none' : `3px solid rgba(28,29,32,0.2)`,
              background: i % 2 ? '#FFFFFF' : '#E7EFEA',
              opacity: ease(frame - i * 6, [0, 12], [0, 1]),
            }}
          >
            <div style={{fontSize: 38, fontWeight: 950, color: palette.cyan}}>{String(i + 1).padStart(2, '0')}</div>
            <div style={{fontSize: 44, fontWeight: 850}}>{row}</div>
          </div>
        ))}
      </div>
    </div>
  </Bg>
);

const CtaShot: React.FC<{frame: number}> = ({frame}) => (
  <Bg>
    <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column'}}>
      <div style={{fontSize: 92, color: palette.white, fontWeight: 950, marginBottom: 54}}>Before the closing summary</div>
      <div style={{display: 'flex', gap: 40}}>
        {['Subscribe', 'Like', 'Ring the bell'].map((label, i) => (
          <div
            key={label}
            style={{
              background: i === 0 ? palette.red : i === 1 ? palette.cyan : palette.amber,
              color: palette.white,
              borderRadius: 8,
              padding: '42px 54px',
              minWidth: 340,
              textAlign: 'center',
              border: '5px solid #fff',
              transform: `scale(${ease(frame - i * 10, [0, 14], [0.72, 1])})`,
            }}
          >
            <div style={{fontSize: 58, fontWeight: 950}}>{label}</div>
          </div>
        ))}
      </div>
    </div>
  </Bg>
);

const EvidenceShot: React.FC<{seg: Segment; frame: number}> = ({seg, frame}) => (
  <Bg>
    <div style={{position: 'absolute', left: 110, top: 74, color: palette.white, fontSize: 88, fontWeight: 950}}>{seg.title}</div>
    <div style={{position: 'absolute', left: 130, top: 250, right: 130, display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 24}}>
      {(seg.bullets ?? []).map((source, i) => (
        <div key={source} style={{background: palette.panel, border: `5px solid ${palette.ink}`, borderRadius: 8, padding: 26, height: 470, opacity: ease(frame - i * 8, [0, 14], [0, 1])}}>
          <div style={{height: 190, background: i % 2 ? '#CFE6DF' : '#EAD7B4', border: `4px solid ${palette.ink}`, borderRadius: 6}} />
          <div style={{fontSize: 42, fontWeight: 950, marginTop: 28}}>{source}</div>
          <div style={{fontSize: 30, lineHeight: 1.18, marginTop: 18, color: '#555'}}>source-backed signal</div>
        </div>
      ))}
    </div>
  </Bg>
);

const LightSweep: React.FC<{frame: number; delay?: number}> = ({frame, delay = 0}) => {
  const x = ease(frame - delay, [0, 90], [-780, 2350]);
  const opacity = ease(frame - delay, [0, 18, 75, 98], [0, 0.72, 0.62, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        top: -240,
        left: x,
        width: 320,
        height: 1560,
        transform: 'rotate(22deg)',
        background: 'linear-gradient(90deg, transparent, rgba(82,235,255,0.28), rgba(255,180,78,0.22), transparent)',
        filter: 'blur(16px)',
        opacity,
        mixBlendMode: 'screen',
      }}
    />
  );
};

const PulseRing: React.FC<{frame: number; left: number; top: number; size: number; delay?: number}> = ({frame, left, top, size, delay = 0}) => {
  const scale = ease((frame - delay) % 70, [0, 58], [0.88, 1.18]);
  const opacity = ease((frame - delay) % 70, [0, 14, 58, 70], [0, 0.8, 0.28, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        left,
        top,
        width: size,
        height: size,
        borderRadius: '50%',
        border: '5px solid rgba(94,236,255,0.9)',
        boxShadow: '0 0 36px rgba(94,236,255,0.78), inset 0 0 26px rgba(94,236,255,0.35)',
        transform: `scale(${scale})`,
        opacity,
        mixBlendMode: 'screen',
      }}
    />
  );
};

const ScanLines: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      inset: 0,
      opacity: 0.16,
      backgroundImage: 'linear-gradient(rgba(255,255,255,0.22) 1px, transparent 1px)',
      backgroundSize: '100% 5px',
      mixBlendMode: 'overlay',
    }}
  />
);

const AnimatedStill: React.FC<{seg: Segment; frame: number; sideAvatar?: boolean}> = ({seg, frame, sideAvatar = false}) => {
  const duration = Math.max(1, Math.round((seg.end - seg.start) * FPS));
  const push = ease(frame, [0, duration], [1.035, 1.105]);
  const driftX = ease(frame, [0, duration], [sideAvatar ? -14 : -24, sideAvatar ? 8 : 26]);
  const driftY = ease(frame, [0, duration], [-10, 10]);
  const titleOpacity = ease(frame, [8, 28], [0, 1]);
  return (
    <AbsoluteFill style={{background: '#05070B', overflow: 'hidden', fontFamily: 'Inter, Arial, sans-serif'}}>
      <Img
        src={stillSrc(seg.seg)}
        style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${push}) translate(${driftX}px, ${driftY}px)`,
          filter: sideAvatar ? 'brightness(0.62) saturate(1.14)' : 'brightness(0.82) saturate(1.18) contrast(1.05)',
        }}
      />
      <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(circle at 50% 44%, transparent 42%, rgba(0,0,0,0.5) 100%)'}} />
      <ScanLines />
      <LightSweep frame={frame} />
      <LightSweep frame={frame} delay={duration * 0.42} />
      <PulseRing frame={frame} left={sideAvatar ? 170 : 1440} top={sideAvatar ? 690 : 140} size={sideAvatar ? 210 : 250} />
      <PulseRing frame={frame} left={sideAvatar ? 760 : 160} top={sideAvatar ? 160 : 690} size={sideAvatar ? 170 : 190} delay={22} />
      {!sideAvatar ? (
        <div
          style={{
            position: 'absolute',
            left: 54,
            bottom: 42,
            maxWidth: 960,
            padding: '18px 24px',
            background: 'rgba(5,9,14,0.68)',
            borderLeft: '7px solid rgba(79,231,255,0.95)',
            color: '#fff',
            opacity: titleOpacity,
            boxShadow: '0 0 32px rgba(0,0,0,0.38)',
          }}
        >
          <div style={{fontSize: 30, letterSpacing: 1.6, fontWeight: 850, color: '#63EEFF'}}>SEGMENT {String(seg.seg).padStart(2, '0')}</div>
          <div style={{fontSize: 52, lineHeight: 1.02, fontWeight: 950, marginTop: 3}}>{seg.title}</div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const AvatarSide: React.FC<{seg: Segment; frame: number}> = ({seg, frame}) => (
  <AbsoluteFill style={{background: '#05070B'}}>
    <AnimatedStill seg={seg} frame={frame} sideAvatar />
    <div style={{position: 'absolute', left: 72, top: 70, width: 990, color: palette.white}}>
      <div style={{fontSize: 74, fontWeight: 950, lineHeight: 1.02, textShadow: '0 0 26px rgba(0,0,0,0.75)'}}>{seg.title}</div>
      <div style={{marginTop: 24}}>
        <BulletList bullets={seg.bullets ?? []} frame={frame} color={palette.white} />
      </div>
    </div>
  </AbsoluteFill>
);

const renderSegment = (seg: Segment) => {
  const SegmentRenderer: React.FC = () => {
    const frame = useCurrentFrame();
    if (seg.kind === 'avatar-side') return <AvatarSide seg={seg} frame={frame} />;
    return <AnimatedStill seg={seg} frame={frame} />;
  };
  return <SegmentRenderer />;
};

export const Main: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {segments.map((seg) => {
        const from = Math.round(seg.start * fps);
        const duration = Math.max(1, Math.round((seg.end - seg.start) * fps));
        return (
          <Sequence key={seg.seg} from={from} durationInFrames={duration} name={`Seg ${seg.seg}: ${seg.title}`}>
            {renderSegment(seg)}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
