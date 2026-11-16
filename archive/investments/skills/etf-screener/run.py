#!/usr/bin/env python3
"""
ETF Screener - Screen 14 ETFs and identify Stage 2 opportunities

This script can run in two modes:
- light: Quick stage detection only (for daily morning checks)
- full: Complete analysis with scoring and recommendations (for weekly reviews)
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# JARVIS paths
JARVIS_ROOT = Path("/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis")
REPORTS_DIR = JARVIS_ROOT / "reports/etf-screening"
MARKET_DATA_CLI = JARVIS_ROOT / "cli-tools/jarvis-price"

# Ensure reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# The 14 ETFs we track
TRACKED_ETFS = [
    "SPY",   # S&P 500
    "QQQ",   # Nasdaq 100
    "IWM",   # Russell 2000
    "DIA",   # Dow Jones
    "EEM",   # Emerging Markets
    "EFA",   # EAFE (International Developed)
    "GLD",   # Gold
    "SLV",   # Silver
    "USO",   # Oil
    "TLT",   # 20+ Year Treasury
    "HYG",   # High Yield Corporate Bonds
    "LQD",   # Investment Grade Corporate Bonds
    "VNQ",   # Real Estate
    "XLE",   # Energy Sector
]


def get_stage_data(symbol: str) -> dict:
    """
    Get stage assessment for a symbol using market data CLI.

    Returns dict with stage, confidence, and key metrics.
    """
    try:
        result = subprocess.run(
            [str(MARKET_DATA_CLI), "stage", symbol, "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                'symbol': symbol,
                'stage': data.get('stage', 'Unknown'),
                'confidence': data.get('confidence', 'Low'),
                'price': data.get('price', 0),
                'sma_50': data.get('sma_50', 0),
                'sma_200': data.get('sma_200', 0),
                'volume_trend': data.get('volume_trend', 'neutral'),
                'error': None
            }
        else:
            return {
                'symbol': symbol,
                'stage': 'Error',
                'confidence': 'N/A',
                'error': result.stderr
            }

    except Exception as e:
        return {
            'symbol': symbol,
            'stage': 'Error',
            'confidence': 'N/A',
            'error': str(e)
        }


def light_mode_scan(check_stages: bool = False) -> dict:
    """
    Quick stage detection scan for morning checks.

    Args:
        check_stages: If True, flag any ETF that changed stages overnight

    Returns:
        Dict with scan results
    """
    print("🔍 Running light mode ETF scan...")
    print(f"Scanning {len(TRACKED_ETFS)} ETFs for stage detection\n")

    results = []
    stage_changes = []

    for symbol in TRACKED_ETFS:
        print(f"Checking {symbol}...", end=" ")
        stage_data = get_stage_data(symbol)
        results.append(stage_data)

        if stage_data['error']:
            print(f"❌ Error")
        else:
            print(f"Stage {stage_data['stage']} ({stage_data['confidence']} confidence)")

            # TODO: Compare to yesterday's stage to detect changes
            # For now, just flag Stage 2 as interesting
            if stage_data['stage'] == '2':
                stage_changes.append({
                    'symbol': symbol,
                    'stage': stage_data['stage'],
                    'note': 'Stage 2 (Markup) - Strong uptrend'
                })

    return {
        'mode': 'light',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'total_scanned': len(TRACKED_ETFS),
        'results': results,
        'stage_changes': stage_changes,
        'errors': [r for r in results if r['error']]
    }


def full_mode_scan() -> dict:
    """
    Complete analysis with scoring and recommendations for weekly reviews.

    Returns:
        Dict with full analysis
    """
    print("📊 Running full mode ETF screening...")
    print(f"Complete analysis of {len(TRACKED_ETFS)} ETFs\n")

    results = []

    for symbol in TRACKED_ETFS:
        print(f"\nAnalyzing {symbol}...")

        # Get stage data
        stage_data = get_stage_data(symbol)

        if stage_data['error']:
            print(f"  ❌ Error: {stage_data['error']}")
            results.append(stage_data)
            continue

        # Get full indicators
        try:
            indicators_result = subprocess.run(
                [str(MARKET_DATA_CLI), "indicators", symbol, "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if indicators_result.returncode == 0:
                indicators = json.loads(indicators_result.stdout)

                # Calculate composite score
                score = calculate_composite_score(stage_data, indicators)

                combined = {
                    **stage_data,
                    'indicators': indicators,
                    'composite_score': score['score'],
                    'grade': score['grade'],
                    'recommendation': score['recommendation']
                }

                results.append(combined)

                print(f"  Stage: {stage_data['stage']}")
                print(f"  Score: {score['score']}/100 (Grade {score['grade']})")
                print(f"  Action: {score['recommendation']}")
            else:
                results.append(stage_data)

        except Exception as e:
            print(f"  ⚠️  Could not fetch indicators: {e}")
            results.append(stage_data)

    # Rank results
    ranked = sorted(
        [r for r in results if not r.get('error')],
        key=lambda x: x.get('composite_score', 0),
        reverse=True
    )

    return {
        'mode': 'full',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'total_scanned': len(TRACKED_ETFS),
        'results': ranked,
        'errors': [r for r in results if r.get('error')]
    }


def calculate_composite_score(stage_data: dict, indicators: dict) -> dict:
    """
    Calculate composite score for an ETF.

    Scoring based on Asset Revesting 4-stage framework:
    - Stage 2 (Markup): Highest scores
    - Stage 1 (Accumulation): Medium scores if setting up
    - Stage 3/4: Low scores
    """
    score = 0

    # Stage weight (0-40 points)
    stage_scores = {
        '1': 20,  # Accumulation - waiting
        '2': 40,  # Markup - best
        '3': 10,  # Distribution - warning
        '4': 0    # Decline - avoid
    }
    score += stage_scores.get(str(stage_data['stage']), 0)

    # Trend alignment (0-30 points)
    price = stage_data.get('price', 0)
    sma_50 = stage_data.get('sma_50', 0)
    sma_200 = stage_data.get('sma_200', 0)

    if price > sma_50 > sma_200:
        score += 30  # Perfect alignment
    elif price > sma_50:
        score += 20  # Above short-term
    elif price > sma_200:
        score += 10  # Above long-term only

    # Momentum (0-30 points)
    rsi = indicators.get('rsi', 50)
    macd = indicators.get('macd', {})

    # RSI in sweet spot (40-70)
    if 40 <= rsi <= 70:
        score += 15
    elif 30 <= rsi <= 80:
        score += 10

    # MACD positive
    if macd.get('histogram', 0) > 0:
        score += 15

    # Grade assignment
    if score >= 80:
        grade = 'A'
        recommendation = 'BUY - Strong Stage 2 uptrend'
    elif score >= 65:
        grade = 'B'
        recommendation = 'WATCH - Potential setup'
    elif score >= 50:
        grade = 'C'
        recommendation = 'HOLD - Monitor for changes'
    else:
        grade = 'D'
        recommendation = 'AVOID - Weak or declining'

    return {
        'score': score,
        'grade': grade,
        'recommendation': recommendation
    }


def generate_report(scan_results: dict, output_file: Path):
    """Generate markdown report from scan results."""

    mode = scan_results['mode']
    date = scan_results['date']

    if mode == 'light':
        # Quick morning brief
        report = f"""# ETF Morning Scan - {date}

**Mode:** Light (Stage Detection Only)
**ETFs Scanned:** {scan_results['total_scanned']}

## Stage Changes

"""
        if scan_results['stage_changes']:
            for change in scan_results['stage_changes']:
                report += f"⚠️  **{change['symbol']}**: {change['note']}\n"
        else:
            report += "✅ No significant stage changes detected\n"

        report += "\n## Quick Summary\n\n"

        # Group by stage
        by_stage = {}
        for r in scan_results['results']:
            if not r['error']:
                stage = r['stage']
                by_stage.setdefault(stage, []).append(r['symbol'])

        for stage in sorted(by_stage.keys()):
            symbols = ', '.join(by_stage[stage])
            report += f"**Stage {stage}:** {symbols}\n"

        if scan_results['errors']:
            report += f"\n⚠️  **Errors:** {len(scan_results['errors'])} ETFs failed to scan\n"

    else:
        # Full weekly report
        report = f"""# ETF Screening Report - {date}

**Mode:** Full Analysis
**ETFs Screened:** {scan_results['total_scanned']}

## Top Opportunities

"""
        # Top 5
        for i, etf in enumerate(scan_results['results'][:5], 1):
            report += f"""### {i}. {etf['symbol']} - Grade {etf['grade']} ({etf['composite_score']}/100)

**Stage:** {etf['stage']} ({etf['confidence']} confidence)
**Recommendation:** {etf['recommendation']}
**Price:** ${etf['price']:.2f}
**SMA 50/200:** ${etf.get('sma_50', 0):.2f} / ${etf.get('sma_200', 0):.2f}

---

"""

        report += "\n## Complete Rankings\n\n"
        report += "| Rank | Symbol | Grade | Score | Stage | Recommendation |\n"
        report += "|------|--------|-------|-------|-------|----------------|\n"

        for i, etf in enumerate(scan_results['results'], 1):
            report += f"| {i} | {etf['symbol']} | {etf['grade']} | {etf['composite_score']} | {etf['stage']} | {etf['recommendation']} |\n"

    report += f"\n\n---\n*Generated by JARVIS ETF Screener*\n"

    with open(output_file, 'w') as f:
        f.write(report)

    print(f"\n📄 Report saved: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="JARVIS ETF Screener - Screen 14 ETFs for opportunities"
    )
    parser.add_argument(
        "--mode",
        choices=["light", "full"],
        default="light",
        help="Scan mode: light (quick stage detection) or full (complete analysis)"
    )
    parser.add_argument(
        "--check-stages",
        action="store_true",
        help="Flag any ETF that changed stages (light mode only)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of report"
    )

    args = parser.parse_args()

    # Run scan
    if args.mode == "light":
        results = light_mode_scan(check_stages=args.check_stages)
    else:
        results = full_mode_scan()

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Generate and save report
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"etf-scan-{args.mode}-{date_str}.md"
        output_file = REPORTS_DIR / filename

        generate_report(results, output_file)

        # Print summary to console
        print("\n" + "=" * 60)
        print(f"ETF SCREENING COMPLETE - {args.mode.upper()} MODE")
        print("=" * 60)
        print(f"Scanned: {results['total_scanned']} ETFs")

        if args.mode == "light":
            print(f"Stage changes: {len(results['stage_changes'])}")
            if results['stage_changes']:
                for change in results['stage_changes']:
                    print(f"  ⚠️  {change['symbol']}: {change['note']}")
        else:
            # Show top 3
            print("\nTop 3 Opportunities:")
            for i, etf in enumerate(results['results'][:3], 1):
                print(f"  {i}. {etf['symbol']}: Grade {etf['grade']} ({etf['composite_score']}/100)")

        print(f"\nFull report: {output_file}")
        print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
