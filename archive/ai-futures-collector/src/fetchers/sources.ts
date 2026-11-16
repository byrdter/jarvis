/**
 * Byrddynasty "Understanding AI" — unified knowledge-source registry.
 *
 * Single machine-readable source of truth for ALL monitored sources, encoding
 * jarvis-private/ai-futures-wiki/Byrddynasty-Jarvis-Knowledge-Sources.md
 * (the Perplexity-cultivated registry) plus the sources already wired in
 * ai-futures.ts. The sweep engine (sweep.ts) iterates this list by cadence.
 *
 * Lenses (show bible):
 *   L1 = Power & Choices · L2 = Scenarios & Trade-offs · L3 = Strategic Navigation
 * These map to the 5 fine-grained thesis_lens tags used in the wiki via LENS_MAP.
 */

export type Cadence = 'daily' | 'weekly' | 'monthly' | 'annual' | 'quarterly';
export type Access = 'open' | 'paywall' | 'semi_open';
export type SweepMethod = 'rss' | 'html' | 'alert' | 'api';
export type Tier = '1' | '1.5' | '2' | '3' | '4' | '5';
export type ShowLens = 'L1' | 'L2' | 'L3';

export interface Source {
  id: string;                 // stable slug (dedupe key for config)
  name: string;
  tier: Tier;
  cadence: Cadence;
  access: Access;
  sweep: SweepMethod;
  lens: ShowLens[];
  url: string;                // durable landing page (anchor)
  feed?: string;              // RSS/Atom/API endpoint, if any
  category: string;           // wiki/<category>/ destination
  academic?: boolean;         // capture title+authors+abstract+DOI; alert for full-text
  note?: string;
}

// Coarse show-lens -> fine wiki thesis_lens (best-effort default; the sweep
// engine still keyword-refines per item).
export const LENS_MAP: Record<ShowLens, string[]> = {
  L1: ['power-control'],
  L2: ['economic-futures', 'social-consequences'],
  L3: ['strategic-choices'],
};

export const SOURCES: Source[] = [
  // ───────────────────────── TIER 1 — Data Anchors ─────────────────────────
  { id: 'hai-ai-index', name: 'Stanford HAI — AI Index Report', tier: '1', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L1','L2','L3'], url: 'https://hai.stanford.edu/ai-index', category: 'data-anchors', note: 'Flagship dataset; release ~April.' },
  { id: 'stanford-digital-economy', name: 'Stanford Digital Economy Lab — AI Economic Indicators', tier: '1', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://digitaleconomy.stanford.edu', category: 'data-anchors', note: 'Entry-level squeeze / canaries dashboard.' },
  { id: 'pew-ai', name: 'Pew Research Center — AI attitudes', tier: '1', cadence: 'monthly', access: 'open', sweep: 'rss', lens: ['L1','L2'], url: 'https://www.pewresearch.org/topic/internet-technology/artificial-intelligence/', feed: 'https://www.pewresearch.org/feed/', category: 'data-anchors' },
  { id: 'mgi', name: 'McKinsey Global Institute', tier: '1', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L2','L3'], url: 'https://www.mckinsey.com/mgi', category: 'data-anchors' },
  { id: 'oecd-future-of-work', name: 'OECD — Future of Work / Employment Outlook', tier: '1', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://www.oecd.org/en/topics/policy-issues/future-of-work.html', category: 'data-anchors' },
  { id: 'imf-ai-work', name: 'IMF — AI & Future of Work', tier: '1', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://www.imf.org', category: 'data-anchors' },
  { id: 'nber', name: 'NBER Working Papers', tier: '1', cadence: 'weekly', access: 'semi_open', sweep: 'rss', lens: ['L2'], url: 'https://www.nber.org/papers', feed: 'https://back.nber.org/rss/new.xml', category: 'academic', academic: true },
  { id: 'yale-budget-lab', name: 'Yale Budget Lab', tier: '1', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://budgetlab.yale.edu', category: 'data-anchors', note: 'Counter-evidence ("no discernible disruption").' },
  { id: 'fed-research', name: 'Federal Reserve research (working papers)', tier: '1', cadence: 'monthly', access: 'open', sweep: 'rss', lens: ['L2'], url: 'https://www.dallasfed.org', feed: 'https://www.federalreserve.gov/feeds/working_papers.xml', category: 'data-anchors' },
  { id: 'pwc-ai-jobs', name: 'PwC Global AI Jobs Barometer', tier: '1', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://www.pwc.com', category: 'data-anchors', note: 'Release ~June.' },
  { id: 'bcg-ai', name: 'Boston Consulting Group (BCG)', tier: '1', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://www.bcg.com', category: 'data-anchors' },
  { id: 'wef-future-jobs', name: 'WEF — Future of Jobs Report', tier: '1', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://www.weforum.org', category: 'data-anchors' },
  { id: 'lightcast', name: 'Lightcast', tier: '1', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://lightcast.io', category: 'data-anchors' },
  { id: 'anthropic-economic-index', name: 'Anthropic Economic Index', tier: '1', cadence: 'monthly', access: 'open', sweep: 'rss', lens: ['L1','L2'], url: 'https://www.anthropic.com/economic-index', feed: 'https://www.anthropic.com/rss.xml', category: 'data-anchors' },
  { id: 'openai-econ', name: 'OpenAI economic research', tier: '1', cadence: 'monthly', access: 'open', sweep: 'rss', lens: ['L1','L2'], url: 'https://openai.com/research', feed: 'https://openai.com/news/rss.xml', category: 'data-anchors' },

  // ──────────────── TIER 1.5 — Peer-Reviewed Academic Journals ────────────────
  { id: 'hbr', name: 'Harvard Business Review', tier: '1.5', cadence: 'weekly', access: 'paywall', sweep: 'rss', lens: ['L3'], url: 'https://hbr.org', feed: 'https://feeds.hbr.org/harvardbusiness', category: 'academic', academic: true },
  { id: 'mit-smr', name: 'MIT Sloan Management Review', tier: '1.5', cadence: 'weekly', access: 'paywall', sweep: 'rss', lens: ['L1','L2','L3'], url: 'https://sloanreview.mit.edu', feed: 'https://sloanreview.mit.edu/feed/', category: 'academic', academic: true },
  { id: 'misqe', name: 'MISQ Executive (MISQE)', tier: '1.5', cadence: 'monthly', access: 'semi_open', sweep: 'html', lens: ['L3'], url: 'https://www.misqe.org', category: 'academic', academic: true },
  { id: 'misq', name: 'MIS Quarterly (MISQ)', tier: '1.5', cadence: 'monthly', access: 'paywall', sweep: 'html', lens: ['L1'], url: 'https://misq.umn.edu', category: 'academic', academic: true },
  { id: 'isr', name: 'Information Systems Research (ISR)', tier: '1.5', cadence: 'monthly', access: 'paywall', sweep: 'rss', lens: ['L2'], url: 'https://pubsonline.informs.org/journal/isre', feed: 'https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=isre', category: 'academic', academic: true },
  { id: 'jmis', name: 'Journal of MIS (JMIS)', tier: '1.5', cadence: 'monthly', access: 'paywall', sweep: 'html', lens: ['L1'], url: 'https://www.jmis-web.org', category: 'academic', academic: true },
  { id: 'mnsc', name: 'Management Science (MnSc)', tier: '1.5', cadence: 'monthly', access: 'paywall', sweep: 'rss', lens: ['L1'], url: 'https://pubsonline.informs.org/journal/mnsc', feed: 'https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=mnsc', category: 'academic', academic: true },
  // Adjacent journals worth adding (monthly; eTOC RSS where INFORMS, else HTML)
  { id: 'orsc', name: 'Organization Science', tier: '1.5', cadence: 'monthly', access: 'paywall', sweep: 'rss', lens: ['L1','L3'], url: 'https://pubsonline.informs.org/journal/orsc', feed: 'https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=orsc', category: 'academic', academic: true, note: 'Adjacent (suggested).' },
  { id: 'jais', name: 'Journal of the AIS (JAIS)', tier: '1.5', cadence: 'monthly', access: 'semi_open', sweep: 'html', lens: ['L1'], url: 'https://aisel.aisnet.org/jais/', category: 'academic', academic: true, note: 'Adjacent (suggested).' },
  { id: 'nature-human-behaviour', name: 'Nature Human Behaviour', tier: '1.5', cadence: 'monthly', access: 'paywall', sweep: 'rss', lens: ['L2'], url: 'https://www.nature.com/nathumbehav/', feed: 'https://www.nature.com/nathumbehav.rss', category: 'academic', academic: true, note: 'Adjacent (suggested).' },
  { id: 'jep', name: 'Journal of Economic Perspectives', tier: '1.5', cadence: 'quarterly', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://www.aeaweb.org/journals/jep', category: 'academic', academic: true, note: 'Adjacent (suggested); open access.' },

  // Academic discovery feeds (find papers before journal print)
  { id: 'arxiv-cs-ai', name: 'arXiv cs.AI', tier: '1.5', cadence: 'daily', access: 'open', sweep: 'rss', lens: ['L2'], url: 'https://arxiv.org/list/cs.AI/recent', feed: 'https://rss.arxiv.org/rss/cs.AI', category: 'academic', academic: true, note: 'High volume; keyword-filter.' },
  { id: 'arxiv-cs-hc', name: 'arXiv cs.HC', tier: '1.5', cadence: 'daily', access: 'open', sweep: 'rss', lens: ['L2','L3'], url: 'https://arxiv.org/list/cs.HC/recent', feed: 'https://rss.arxiv.org/rss/cs.HC', category: 'academic', academic: true },
  { id: 'arxiv-cs-cy', name: 'arXiv cs.CY', tier: '1.5', cadence: 'daily', access: 'open', sweep: 'rss', lens: ['L1','L2'], url: 'https://arxiv.org/list/cs.CY/recent', feed: 'https://rss.arxiv.org/rss/cs.CY', category: 'academic', academic: true },
  { id: 'arxiv-econ-gn', name: 'arXiv econ.GN', tier: '1.5', cadence: 'daily', access: 'open', sweep: 'rss', lens: ['L2'], url: 'https://arxiv.org/list/econ.GN/recent', feed: 'https://rss.arxiv.org/rss/econ.GN', category: 'academic', academic: true },
  { id: 'ssrn', name: 'SSRN (keyword alert)', tier: '1.5', cadence: 'weekly', access: 'semi_open', sweep: 'alert', lens: ['L2'], url: 'https://www.ssrn.com', category: 'academic', academic: true, note: 'Account keyword alerts; no clean feed.' },
  { id: 'informs-mnsc-advance', name: 'INFORMS Articles in Advance (MnSc)', tier: '1.5', cadence: 'weekly', access: 'paywall', sweep: 'rss', lens: ['L1'], url: 'https://pubsonline.informs.org/toc/mnsc/0/0', feed: 'https://pubsonline.informs.org/action/showFeed?type=axatoc&feed=rss&jc=mnsc', category: 'academic', academic: true, note: 'Online-first, months before print.' },
  { id: 'google-scholar-alerts', name: 'Google Scholar Alerts', tier: '1.5', cadence: 'daily', access: 'open', sweep: 'alert', lens: ['L2'], url: 'https://scholar.google.com', category: 'academic', academic: true, note: 'Email alerts → forward to JARVIS inbox for ingest.' },
  { id: 'semantic-scholar', name: 'Semantic Scholar / Connected Papers', tier: '1.5', cadence: 'weekly', access: 'open', sweep: 'api', lens: ['L2'], url: 'https://www.semanticscholar.org', category: 'academic', academic: true, note: 'Citation-chaining API from a key paper.' },

  // ──────────────── TIER 2 — Power, Governance & Safety ────────────────
  { id: 'brookings-ai-gov', name: 'Brookings — AI Governance', tier: '2', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://www.brookings.edu/tags/ai-governance/', feed: 'https://www.brookings.edu/feed/', category: 'thinktanks', note: 'Feed often returns HTML — fallback to html sweep.' },
  { id: 'govai', name: 'Centre for the Governance of AI (GovAI)', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://www.governance.ai', category: 'thinktanks' },
  { id: 'iaps', name: 'Institute for AI Policy & Strategy (IAPS)', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://www.iaps.ai', category: 'thinktanks' },
  { id: 'data-society', name: 'Data & Society', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://datasociety.net', category: 'thinktanks' },
  { id: 'ai-now', name: 'AI Now Institute', tier: '2', cadence: 'monthly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://ainowinstitute.org', feed: 'https://ainowinstitute.org/feed', category: 'thinktanks' },
  { id: 'chatham-rand-carnegie', name: 'Chatham House / RAND / Carnegie', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1','L2'], url: 'https://www.rand.org', category: 'thinktanks', note: 'Per-site RSS where available; geopolitics/US-China.' },
  { id: 'hai-policy', name: 'Stanford HAI Policy', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://hai.stanford.edu/policy', category: 'thinktanks' },
  { id: 'oii', name: 'Oxford Internet Institute', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://www.oii.ox.ac.uk', category: 'thinktanks' },
  { id: 'intl-ai-safety-report', name: 'International AI Safety Report (Bengio et al.)', tier: '2', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://www.gov.uk/government/publications/international-ai-safety-report-2025', category: 'thinktanks', note: 'IPCC-style consensus doc (+ interim updates).' },
  { id: 'fli-safety-index', name: 'Future of Life Institute — AI Safety Index', tier: '2', cadence: 'monthly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://futureoflife.org', feed: 'https://futureoflife.org/feed/', category: 'thinktanks' },
  { id: 'itu-wef-gov', name: 'ITU AI Governance / WEF AI Governance Alliance', tier: '2', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://www.itu.int', category: 'thinktanks' },
  { id: 'fmti', name: 'Stanford Foundation Model Transparency Index', tier: '2', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://crfm.stanford.edu/fmti/', category: 'thinktanks', note: 'Power-asymmetry: how little labs disclose.' },
  { id: 'nist-ai-rmf', name: 'NIST AI Risk Management Framework', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1','L3'], url: 'https://www.nist.gov/itl/ai-risk-management-framework', category: 'thinktanks' },
  { id: 'eu-ai-act', name: 'EU AI Act portal', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://artificialintelligenceact.eu', category: 'thinktanks' },
  { id: 'oecd-ai', name: 'OECD AI Policy Observatory (OECD.AI)', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://oecd.ai', category: 'thinktanks' },
  { id: 'law-ai', name: 'Institute for Law & AI', tier: '2', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://law-ai.org', category: 'thinktanks' },
  { id: 'lawfare', name: 'Lawfare', tier: '2', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://www.lawfaremedia.org', feed: 'https://www.lawfaremedia.org/feeds/rss.xml', category: 'thinktanks' },
  { id: 'tech-policy-press', name: 'Tech Policy Press', tier: '2', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://www.techpolicy.press', feed: 'https://www.techpolicy.press/rss/', category: 'thinktanks' },

  // ──────────────── TIER 3 — Analysis, Synthesis & Story Ideas ────────────────
  { id: 'import-ai', name: 'Import AI (Jack Clark)', tier: '3', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1','L2'], url: 'https://importai.net', feed: 'https://importai.substack.com/feed', category: 'newsletters' },
  { id: 'stratechery', name: 'Stratechery (Ben Thompson)', tier: '3', cadence: 'weekly', access: 'paywall', sweep: 'rss', lens: ['L1'], url: 'https://stratechery.com', category: 'newsletters', note: 'Private member RSS token (secret) required.' },
  { id: 'exponential-view', name: 'Exponential View (Azeem Azhar)', tier: '3', cadence: 'weekly', access: 'semi_open', sweep: 'rss', lens: ['L2'], url: 'https://www.exponentialview.co', feed: 'https://www.exponentialview.co/feed', category: 'newsletters' },
  { id: 'one-useful-thing', name: 'One Useful Thing (Ethan Mollick)', tier: '3', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L2','L3'], url: 'https://www.oneusefulthing.org', feed: 'https://www.oneusefulthing.org/feed', category: 'newsletters' },
  { id: 'ai-snake-oil', name: 'AI Snake Oil (Narayanan & Kapoor)', tier: '3', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L2'], url: 'https://www.aisnakeoil.com', feed: 'https://www.aisnakeoil.com/feed', category: 'newsletters', note: 'Counter-evidence / hype-debunk flag.' },
  { id: 'pragmatic-engineer', name: 'Pragmatic Engineer (Gergely Orosz)', tier: '3', cadence: 'weekly', access: 'paywall', sweep: 'rss', lens: ['L2'], url: 'https://newsletter.pragmaticengineer.com', feed: 'https://newsletter.pragmaticengineer.com/feed', category: 'newsletters' },
  { id: 'ai-ethics-brief', name: 'The AI Ethics Brief (Montreal AI Ethics)', tier: '3', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://montrealethics.ai', feed: 'https://montrealethics.ai/feed/', category: 'thinktanks' },
  { id: 'zvi', name: 'Zvi Mowshowitz — Don\'t Worry About the Vase', tier: '3', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1','L2'], url: 'https://thezvi.substack.com', feed: 'https://thezvi.substack.com/feed', category: 'newsletters' },
  { id: 'the-information', name: 'The Information', tier: '3', cadence: 'daily', access: 'paywall', sweep: 'rss', lens: ['L1'], url: 'https://www.theinformation.com', feed: 'https://www.theinformation.com/feed', category: 'news' },
  { id: 'ft-tech', name: 'Financial Times — Technology', tier: '3', cadence: 'daily', access: 'paywall', sweep: 'rss', lens: ['L1','L2'], url: 'https://www.ft.com', feed: 'https://www.ft.com/technology?format=rss', category: 'news' },
  { id: 'economist-tech', name: 'The Economist — Science & Technology', tier: '3', cadence: 'weekly', access: 'paywall', sweep: 'rss', lens: ['L2'], url: 'https://www.economist.com', feed: 'https://www.economist.com/science-and-technology/rss.xml', category: 'news' },
  { id: 'wire-services-tech', name: 'Bloomberg / Reuters / WSJ (tech)', tier: '3', cadence: 'daily', access: 'paywall', sweep: 'rss', lens: ['L1','L2'], url: 'https://www.reuters.com/technology/', category: 'news', note: 'Per-site tech RSS.' },
  { id: 'mit-tech-review', name: 'MIT Technology Review', tier: '3', cadence: 'weekly', access: 'semi_open', sweep: 'rss', lens: ['L1','L2'], url: 'https://www.technologyreview.com', feed: 'https://www.technologyreview.com/feed/', category: 'news' },
  { id: 'wired-ai', name: 'Wired — AI', tier: '3', cadence: 'weekly', access: 'semi_open', sweep: 'rss', lens: ['L1','L2'], url: 'https://www.wired.com', feed: 'https://www.wired.com/feed/tag/ai/latest/rss', category: 'news' },
  { id: 'rest-of-world', name: 'Rest of World', tier: '3', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L2'], url: 'https://restofworld.org', feed: 'https://restofworld.org/feed/latest/', category: 'news', note: 'AI impact outside US/Europe.' },

  // ──────────────── TIER 4 — Historical Context & Frameworks (evergreen) ────────────────
  { id: 'prediction-machines', name: 'Power and Prediction / Prediction Machines (Agrawal et al.)', tier: '4', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L3'], url: 'https://www.predictionmachines.ai', category: 'frameworks' },
  { id: 'carlota-perez', name: 'Carlota Perez — Technological Revolutions & Financial Capital', tier: '4', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L2','L3'], url: 'https://www.carlotaperez.org', category: 'frameworks' },
  { id: 'brynjolfsson', name: 'Brynjolfsson & McAfee — Second Machine Age', tier: '4', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://mitsloan.mit.edu/faculty/directory/erik-brynjolfsson', category: 'frameworks' },
  { id: 'acemoglu-johnson', name: 'Acemoglu & Johnson — Power and Progress', tier: '4', cadence: 'annual', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://shapingwork.mit.edu', category: 'frameworks' },
  { id: 'our-world-in-data-ai', name: 'Our World in Data — AI', tier: '4', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L2'], url: 'https://ourworldindata.org/artificial-intelligence', category: 'frameworks' },
  { id: 'ieee-spectrum', name: 'IEEE Spectrum / Computer History Museum', tier: '4', cadence: 'monthly', access: 'open', sweep: 'rss', lens: ['L2'], url: 'https://spectrum.ieee.org', feed: 'https://spectrum.ieee.org/feeds/feed.rss', category: 'frameworks' },

  // ──────────────── TIER 5 — Primary & Company Sources ────────────────
  { id: 'openai-news', name: 'OpenAI blog/news', tier: '5', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://openai.com/news', feed: 'https://openai.com/news/rss.xml', category: 'companies' },
  { id: 'anthropic-news', name: 'Anthropic news', tier: '5', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://www.anthropic.com/news', feed: 'https://www.anthropic.com/rss.xml', category: 'companies' },
  { id: 'deepmind-blog', name: 'Google DeepMind blog', tier: '5', cadence: 'weekly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://deepmind.google/discover/blog/', category: 'companies' },
  { id: 'microsoft-ai-blog', name: 'Microsoft AI blog', tier: '5', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://blogs.microsoft.com/ai/', feed: 'https://news.microsoft.com/source/topics/ai/feed/', category: 'companies' },
  { id: 'meta-ai-blog', name: 'Meta AI blog', tier: '5', cadence: 'weekly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://ai.meta.com/blog/', category: 'companies' },
  { id: 'nvidia-blog', name: 'NVIDIA blog', tier: '5', cadence: 'weekly', access: 'open', sweep: 'rss', lens: ['L1'], url: 'https://blogs.nvidia.com', feed: 'https://blogs.nvidia.com/feed/', category: 'companies' },
  { id: 'sec-edgar', name: 'SEC filings / earnings / investor letters', tier: '5', cadence: 'quarterly', access: 'open', sweep: 'api', lens: ['L1'], url: 'https://www.sec.gov/cgi-bin/browse-edgar', category: 'companies', note: 'EDGAR full-text search API; earnings season.' },
  { id: 'gov-primary-docs', name: 'Government primary docs (White House EOs, EU Commission, UK AISI)', tier: '5', cadence: 'monthly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://www.whitehouse.gov', category: 'companies' },
  { id: 'earnings-transcripts', name: 'Earnings-call transcripts', tier: '5', cadence: 'quarterly', access: 'open', sweep: 'html', lens: ['L1'], url: 'https://www.fool.com/earnings-call-transcripts/', category: 'companies' },
];

// ───────────────────────────── helpers ─────────────────────────────
export const byCadence = (c: Cadence) => SOURCES.filter((s) => s.cadence === c);
export const academicSources = () => SOURCES.filter((s) => s.academic);
export const rssSources = (c?: Cadence) => SOURCES.filter((s) => s.sweep === 'rss' && (!c || s.cadence === c));
export const getSource = (id: string) => SOURCES.find((s) => s.id === id);
export const fineLenses = (s: Source): string[] => [...new Set(s.lens.flatMap((l) => LENS_MAP[l]))];

// Counts for sanity / reporting
export const REGISTRY_STATS = {
  total: SOURCES.length,
  byTier: SOURCES.reduce((a, s) => ((a[s.tier] = (a[s.tier] || 0) + 1), a), {} as Record<string, number>),
  byCadence: SOURCES.reduce((a, s) => ((a[s.cadence] = (a[s.cadence] || 0) + 1), a), {} as Record<string, number>),
  rss: SOURCES.filter((s) => s.sweep === 'rss').length,
  academic: SOURCES.filter((s) => s.academic).length,
  paywall: SOURCES.filter((s) => s.access === 'paywall').length,
};
