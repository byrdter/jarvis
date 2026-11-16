# JARVIS Market Data CLI Tool

Real-time market data fetcher for JARVIS investment analysis.

## Features

- **Current Price**: Get real-time price and market data
- **Historical Data**: Fetch price history (up to 250 days)
- **Technical Indicators**: Calculate SMAs (20/50/150/200), RSI, MACD
- **Stage Detection**: Determine market stage (1-4) using Asset Revesting criteria

## Installation

```bash
cd cli-tools/market-data

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

This will install the `jarvis-price` command globally.

## Commands

### Current Price
```bash
jarvis-price current SPY
jarvis-price current QQQ --json  # JSON output
```

### Historical Data
```bash
jarvis-price history SPY                 # Last 200 days (default)
jarvis-price history QQQ --days 90      # Last 90 days
jarvis-price history SPY --json         # JSON output
```

### Technical Indicators
```bash
jarvis-price indicators SPY
jarvis-price indicators QQQ --json
```

### Stage Detection
```bash
jarvis-price stage SPY
jarvis-price stage QQQ --json
```

## Output Formats

### Human-Readable (Default)
Pretty tables and formatted output for terminal viewing.

### JSON Mode (`--json`)
Structured JSON for programmatic consumption (used by JARVIS).

## Data Source

Uses `yfinance` library to fetch data from Yahoo Finance:
- Real-time quotes (15-20 min delay for free tier)
- Historical OHLCV data
- Adjusted for splits and dividends

## Requirements

- Python 3.11+
- Internet connection for data fetching
- Dependencies: yfinance, typer, pandas, rich

## Usage from JARVIS

JARVIS calls this tool via bash commands with `--json` flag for structured data:

```bash
jarvis-price indicators SPY --json
```

See `context/tools/market-data-cli.md` for JARVIS integration documentation.

## Error Handling

- Invalid symbols return error code 1
- Network errors are reported with details
- Insufficient data warnings for new/illiquid symbols

## Development

```bash
# Run tests
uv run pytest

# Install in development mode
uv pip install -e .
```

## Version

0.1.0 - Initial release with core functionality
