# JARVIS - Just A Rather Very Intelligent System

**An AI-powered autonomous agent framework built on Claude Code**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-purple.svg)](https://claude.ai/code)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> **Update (November 2026):** JARVIS now focuses on agentic AI: building and testing AI apps and
> capabilities. The investment skills described below were moved to [`archive/investments/`](archive/README.md)
> and are no longer maintained. This README will be rewritten for the new direction.

---

## ⚠️ IMPORTANT DISCLAIMER

**The skills and examples in this repository are for educational and demonstration purposes only.**

- **NOT financial, investment, legal, or professional advice**
- **Investment skills demonstrate technical implementation only**
- **Always consult qualified professionals for financial decisions**
- **Use at your own risk**

The author assumes no liability for any decisions made based on this code.

---

## Overview

JARVIS is a production-ready autonomous AI agent framework that demonstrates:

- **🧠 Intelligent Orchestration** - Context-aware decision making
- **🔌 Skill-Based Architecture** - Extensible plugin system (100+ skill capacity)
- **🔐 Security-First Design** - Three-level classification, human-in-the-loop approval
- **💾 Hybrid Memory System** - Vector search + keyword matching
- **🎯 Progressive Disclosure** - Load only what's needed (55-80% token savings)
- **🛠️ Multi-Platform Integration** - MCP servers for Gmail, Calendar, Slack, YouTube, etc.
- **📊 Production-Ready** - Real-world usage in investment domain

Built on [Claude Code](https://claude.ai/code) with extensibility and security as core principles.

---

## Key Features

### 1. Skill Architecture

```yaml
---
name: market-analysis
version: 1.0.0
metadata:
  jarvis:
    security_level: medium
    requires_approval: false
    allowed_operations: [read, network]
    requires:
      bins: ["jarvis-price"]
      env: ["ALPACA_API_KEY"]
---
```

- **Auto-discovery** - Skills found automatically (no manual registration)
- **JSON Schema validation** - Skills validated before execution
- **Dependency gating** - Required tools/env vars checked upfront
- **Security classification** - Low/medium/high with approval gates

### 2. Hybrid Memory System

```
Memory Backends:
├── Chroma (local vector DB)        → Development
├── Supabase (cloud vector DB)      → Production
└── Neo4j (knowledge graph)         → Future

Search Methods:
├── Vector search (70%)             → Semantic similarity
└── Keyword search (30%)            → Exact matches
```

- **Pluggable backends** - Switch via environment variable
- **Progressive disclosure** - Load only relevant context
- **Session awareness** - Recent vs long-term memory routing

### 3. Security Model

```
Level      | Approval Required | Operations Allowed | Examples
-----------|-------------------|--------------------|-----------------
Low        | No                | read               | Data fetching
Medium     | No                | read, network      | API calls
High       | Yes (human)       | read, write, exec  | Trading, posting
```

- **Operation-level permissions** - Read, write, delete, execute, network
- **Complete audit trail** - All decisions logged with context
- **Zero-trust by default** - Explicitly grant permissions

### 4. Progressive Disclosure

Instead of loading all context (8,000+ tokens), JARVIS loads only what's needed:

```python
# User asks: "What's my current portfolio?"
→ Load: context/memory/work-status.md (100 tokens)
→ Skip: context/projects/investments/ (5,000 tokens)
→ Token savings: 98%
```

- **55-80% context reduction** in practice
- **Faster responses** - Less processing overhead
- **Better focus** - Relevant context only

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE (Brain)                       │
│                                                              │
│  Uses: Context System + Skills + Hooks + CLI Tools/MCP      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
          [Ecosystem]    [Skills]      [CLI Tools]
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                    ┌─────────────────────────────┐
                    │      Orchestrator          │
                    │   (Intent Recognition)     │
                    └─────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
              [Registry] [Memory]  [Security]
```

### Core Components

#### Ecosystem (`ecosystem/`)
- **Orchestrator** - Intent recognition, skill routing, context selection
- **Registry** - Skill discovery, validation, dependency checking
- **Memory** - Vector + keyword search, pluggable backends
- **Security** - Classification, approval gates, audit trail

#### Skills (`skills/`)
- **Investment Domain** - market-analysis, etf-screener, portfolio-builder, etc.
- **Research Domain** - academic-research-aggregator, arxiv-aggregator
- **Knowledge Domain** - obsidian-manager
- **Generic Skills** - news-aggregator, agent-browser

#### CLI Tools (`cli-tools/`)
- **jarvis-price** - Market data tool (Yahoo Finance integration)
- **jarvis-skill** - Skill generator and validator
- **jarvis-registry** - Registry management

---

## Quick Start

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.10+
- Node.js 18+ (for some skills)
- API keys as needed (see `.env.example`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis.git
   cd jarvis
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install CLI tools**
   ```bash
   cd cli-tools/market-data
   pip install -e .

   cd ../jarvis-skill
   pip install -e .
   ```

4. **Configure Claude Code**
   ```bash
   # .claude/settings.json already configured
   # Review and adjust as needed
   ```

5. **Start JARVIS**
   ```bash
   claude
   ```

### First Steps

```bash
# In Claude Code:

# 1. Check what skills are available
/skills

# 2. Run a skill
/skill market-analysis --symbol QQQ

# 3. Check memory
What have I been working on?

# 4. Create a new skill
/skill create my-new-skill
```

---

## Example: Market Analysis Skill

JARVIS can analyze ETFs using the Asset Revesting methodology:

```bash
# Run market analysis
/skill market-analysis --symbol SPY
```

**Output:**
```
📊 Market Analysis: SPY
───────────────────────────────

Current Stage: Stage 2 (Markup)
Trend: Bullish ↗
Risk Level: Medium

Technical Indicators:
• 50-day SMA: Above price ✓
• 200-day SMA: Above price ✓
• RSI: 65 (neutral)
• MACD: Bullish crossover

Recommendation: Hold existing position
Entry Point: Wait for pullback to $520
Stop Loss: $510 (-2%)

⚠️ Educational example only - not financial advice
```

See [`docs/skills/EXAMPLES.md`](docs/skills/EXAMPLES.md) for more examples.

---

## Documentation

### For Users
- **[Setup Guide](docs/setup/INSTALLATION.md)** - Installation and configuration
- **[Quick Start](docs/setup/QUICK-START.md)** - Get running in 5 minutes
- **[Skill Examples](docs/skills/EXAMPLES.md)** - Real-world usage examples

### For Developers
- **[Architecture Overview](docs/architecture/OVERVIEW.md)** - System design
- **[Skill Development](docs/skills/DEVELOPMENT-GUIDE.md)** - Create your own skills
- **[API Reference](docs/api/README.md)** - Core APIs and interfaces
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute

### Reference
- **[Nine Essential Skills Framework](NINE-SKILLS-MAPPING.md)** - Theoretical foundation
- **[Security Model](docs/architecture/SECURITY.md)** - Security implementation
- **[Memory System](docs/architecture/MEMORY.md)** - Hybrid memory design

---

## Project Status

### Completed Phases

✅ **Phase 0: Terminal Foundation** (Jan 2026)
- Claude Code integration
- Context system with progressive disclosure
- Memory patterns established

✅ **Phase 1: Investment Domain** (Feb 2026)
- 6 investment skills complete
- Real market data integration (Yahoo Finance)
- Heartbeat system (24/7 autonomous execution)
- Production-ready portfolio management

✅ **Phase 1 Extended: Multi-Domain** (Feb 2026)
- Content creation domain
- Research automation
- Obsidian integration (7 domains)

✅ **Phase 2: Hybrid Memory** (Mar 2026)
- Vector search + keyword search
- Pluggable backends (Chroma/Supabase/Neo4j)
- 70/30 hybrid ranking

✅ **Phase 3: MCP Integration** (Mar 2026)
- 4 MCP servers integrated (Gmail, Calendar, Slack, YouTube)
- Lazy loading (zero context bloat)
- Ready for 20+ platforms

✅ **Phase 4: Memory-Aware Orchestration** (Mar 2026)
- Smart layer routing
- Auto-discovery
- Context selection

✅ **Phase 5: Security Validation** (Mar 2026)
- Three-level classification
- Human-in-the-loop approval
- Complete audit trail
- Level 0 & 0.5 security alignment

### Future Roadmap

🔜 **Phase 6: Voice Interface** (Planned)
- Speech-to-text (Whisper)
- Text-to-speech (ElevenLabs)
- React voice UI

🔜 **Phase 7: Full Integration** (Planned)
- Brokerage integration (Alpaca live trading)
- Database persistence (Supabase)
- Dashboard and reporting

---

## Skills Showcase

| Skill | Domain | Description | Status |
|-------|--------|-------------|--------|
| `market-analysis` | Finance | ETF analysis with Asset Revesting | ✅ Production |
| `etf-screener` | Finance | Screen 14 ETFs, rank opportunities | ✅ Production |
| `portfolio-builder` | Finance | Construct allocation with sizing | ✅ Production |
| `portfolio-monitor` | Finance | Daily stop checks + weekly reviews | ✅ Production |
| `performance-tracker` | Finance | Monthly strategy validation | ✅ Production |
| `market-insights` | Finance | Chris Vermeulen YouTube analysis | ✅ Production |
| `obsidian-manager` | Knowledge | Multi-domain second brain | ✅ Production |
| `academic-research` | Research | Academic paper aggregation | ✅ Beta |
| `arxiv-aggregator` | Research | ArXiv paper search | ✅ Beta |
| `news-aggregator` | Content | Multi-source news aggregation | ✅ Beta |
| `agent-browser` | Tools | Autonomous web browsing | ✅ Beta |

---

## Real-World Usage

JARVIS is actively used for:

1. **Investment Management**
   - Daily portfolio monitoring (6 skills, $100K allocation)
   - Weekly strategy validation
   - Market signal detection

2. **Content Creation**
   - 234+ pieces of promotional content
   - 18,000+ lines of pre-written material
   - Multi-platform distribution (7 platforms)

3. **Research Automation**
   - Academic paper aggregation
   - YouTube content analysis
   - Market insights extraction

4. **Knowledge Management**
   - Obsidian vault organization (7 domains)
   - Cross-domain synthesis
   - Progressive disclosure

**Key Achievement:** Completed Phase 0-5 (Jan-Mar 2026) - production-ready autonomous agent framework with real-world validation.

---

## Technical Highlights

### Security Implementation

```python
# skill metadata
security_level: "high"
requires_approval: true
allowed_operations: ["read", "write", "network"]

# Runtime enforcement
if skill.security_level == "high":
    approval = await request_user_approval(
        skill=skill,
        operation=operation,
        context=full_context
    )
    if not approval:
        raise PermissionDenied()
```

### Progressive Disclosure

```python
# Instead of loading everything
context = load_all_context()  # 8,000 tokens ❌

# Load only what's needed
context = progressive_load(
    query=user_query,
    threshold=0.7
)  # 1,500 tokens ✅
```

### Skill Auto-Discovery

```bash
# Skills discovered from 3 locations:
1. skills/               # Core skills
2. ~/.jarvis/skills/    # User skills
3. Custom paths         # Project-specific

# No manual registration needed
```

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- 🐛 **Report bugs** - Open an issue
- 💡 **Suggest features** - Discuss in issues
- 🔧 **Fix issues** - Submit a pull request
- 📖 **Improve docs** - Documentation PRs welcome
- 🎨 **Create skills** - Share your skills
- 🧪 **Add tests** - Test coverage improvements

### Development Setup

See [docs/contributing/DEVELOPMENT-SETUP.md](docs/contributing/DEVELOPMENT-SETUP.md) for local development instructions.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- Claude Code - [Anthropic Terms](https://www.anthropic.com/terms)
- Dependencies listed in package manifests

---

## Acknowledgments

### Inspiration

- **OpenClaw** - Plugin architecture, memory system, multi-platform approach
- **Chris Vermeulen** - Asset Revesting methodology
- **Nine Essential Skills Framework** - Theoretical foundation

### Built With

- [Claude Code](https://claude.ai/code) - AI-powered development environment
- [Claude Sonnet 4.5](https://www.anthropic.com/claude) - Reasoning engine
- [Chroma](https://www.trychroma.com/) - Vector database
- [Yahoo Finance](https://pypi.org/project/yfinance/) - Market data
- [MCP](https://www.anthropic.com/mcp) - Multi-platform integration

---

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/jarvis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jarvis/discussions)
- **Documentation**: [docs/](docs/)

---

## Learn More

- 📺 **[YouTube Channel](https://www.youtube.com/@byrddynasty)** - Video tutorials and demos
- 📝 **[Blog Posts](https://www.byrdterry.com)** - Deep dives and case studies
- 🐦 **[Twitter/X](https://twitter.com/yourusername)** - Updates and tips

---

**⭐ Star this repo if you find it useful!**

---

*Last updated: March 8, 2026*
