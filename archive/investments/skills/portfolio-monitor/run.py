#!/usr/bin/env python3
"""
Portfolio Monitor - Monitor active positions with stop loss checks

This script monitors the current portfolio and checks:
- Daily mode: Stop loss levels, risk exposure
- Weekly mode: Full portfolio health check, allocation vs target
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# JARVIS paths
JARVIS_ROOT = Path("/Users/terrybyrd/Library/CloudStorage/Dropbox/jarvis")
REPORTS_DIR = JARVIS_ROOT / "reports/portfolio-monitoring"
MARKET_DATA_CLI = JARVIS_ROOT / "cli-tools/jarvis-price/jarvis-price"

# Current portfolio (will eventually read from database/file)
# For now, hardcoded based on $100K allocation from Jan 25
CURRENT_POSITIONS = [
    {
        'symbol': 'QQQ',
        'shares': 0,  # Not entered yet
        'entry_price': 525.00,  # Target entry
        'stop_loss': 498.75,  # 5% stop
        'allocated': 25000,
        'status': 'pending'
    },
    {
        'symbol': 'USO',
        'shares': 0,  # Conditional position
        'entry_price': 67.00,  # If Stage 2
        'stop_loss': 63.65,  # 5% stop
        'allocated': 10000,
        'status': 'conditional'
    },
    {
        'symbol': 'BIL',
        'shares': 0,  # Cash equivalent
        'entry_price': 91.50,
        'stop_loss': None,  # No stop on cash
        'allocated': 65000,
        'status': 'pending'
    }
]

# Ensure reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def get_current_price(symbol: str) -> float:
    """Get current price for a symbol."""
    try:
        result = subprocess.run(
            [str(MARKET_DATA_CLI), "current", symbol, "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('price', 0)
        else:
            return 0

    except Exception:
        return 0


def daily_mode(check_stops: bool = False) -> dict:
    """
    Daily stop loss check.

    Args:
        check_stops: If True, check all positions against stop levels

    Returns:
        Dict with check results
    """
    print("🛡️  Running daily portfolio guard...")
    print("Checking stop losses on active positions\n")

    results = []
    warnings = []

    for position in CURRENT_POSITIONS:
        symbol = position['symbol']
        status = position['status']

        # Skip conditional/pending positions
        if status != 'active':
            print(f"{symbol}: {status.upper()} - not monitored")
            continue

        print(f"Checking {symbol}...", end=" ")

        current_price = get_current_price(symbol)

        if current_price == 0:
            print("❌ Could not fetch price")
            results.append({
                'symbol': symbol,
                'status': 'error',
                'error': 'Price fetch failed'
            })
            continue

        stop_loss = position['stop_loss']

        if stop_loss is None:
            print("✅ No stop (cash equivalent)")
            results.append({
                'symbol': symbol,
                'current_price': current_price,
                'stop_loss': None,
                'status': 'no_stop',
                'distance': None
            })
            continue

        # Calculate distance to stop
        distance_pct = ((current_price - stop_loss) / current_price) * 100

        if distance_pct <= 2:
            # Within 2% of stop - WARNING
            status_emoji = "⚠️"
            status_text = "WARNING"
            warnings.append({
                'symbol': symbol,
                'current_price': current_price,
                'stop_loss': stop_loss,
                'distance_pct': distance_pct
            })
        elif distance_pct <= 5:
            # Within 5% of stop - CAUTION
            status_emoji = "⚡"
            status_text = "CAUTION"
        else:
            # Safe distance
            status_emoji = "✅"
            status_text = "SAFE"

        print(f"{status_emoji} {status_text} (${current_price:.2f}, stop ${stop_loss:.2f}, {distance_pct:.1f}% away)")

        results.append({
            'symbol': symbol,
            'current_price': current_price,
            'stop_loss': stop_loss,
            'distance_pct': distance_pct,
            'status': status_text.lower()
        })

    return {
        'mode': 'daily',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'positions_checked': len([r for r in results if r.get('status') != 'error']),
        'results': results,
        'warnings': warnings
    }


def weekly_mode() -> dict:
    """
    Weekly portfolio health check.

    Returns:
        Dict with weekly analysis
    """
    print("💼 Running weekly portfolio review...")
    print("Full portfolio health check\n")

    results = []
    total_value = 0
    total_allocated = 0

    for position in CURRENT_POSITIONS:
        symbol = position['symbol']
        allocated = position['allocated']
        status = position['status']

        print(f"\n{symbol}:")
        print(f"  Allocated: ${allocated:,.0f}")
        print(f"  Status: {status.upper()}")

        if status == 'active':
            current_price = get_current_price(symbol)
            entry_price = position['entry_price']
            shares = position['shares']

            current_value = current_price * shares
            pnl = current_value - (entry_price * shares)
            pnl_pct = (pnl / (entry_price * shares)) * 100

            print(f"  Entry: ${entry_price:.2f}")
            print(f"  Current: ${current_price:.2f}")
            print(f"  P&L: ${pnl:,.2f} ({pnl_pct:.2f}%)")

            total_value += current_value

            results.append({
                'symbol': symbol,
                'allocated': allocated,
                'current_value': current_value,
                'pnl': pnl,
                'pnl_pct': pnl_pct,
                'status': 'active'
            })

        else:
            # Pending or conditional
            total_value += allocated  # Count as cash

            results.append({
                'symbol': symbol,
                'allocated': allocated,
                'current_value': allocated,
                'pnl': 0,
                'pnl_pct': 0,
                'status': status
            })

        total_allocated += allocated

    # Portfolio metrics
    total_pnl = total_value - total_allocated
    total_pnl_pct = (total_pnl / total_allocated) * 100

    print(f"\n{'='*60}")
    print("PORTFOLIO SUMMARY")
    print(f"{'='*60}")
    print(f"Total Allocated: ${total_allocated:,.0f}")
    print(f"Current Value: ${total_value:,.0f}")
    print(f"Total P&L: ${total_pnl:,.2f} ({total_pnl_pct:.2f}%)")
    print(f"{'='*60}")

    return {
        'mode': 'weekly',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'total_allocated': total_allocated,
        'current_value': total_value,
        'total_pnl': total_pnl,
        'total_pnl_pct': total_pnl_pct,
        'positions': results
    }


def generate_report(check_results: dict, output_file: Path):
    """Generate markdown report."""

    mode = check_results['mode']
    date = check_results['date']

    if mode == 'daily':
        # Daily stop check report
        report = f"""# Daily Portfolio Guard - {date}

**Positions Checked:** {check_results['positions_checked']}

## Stop Loss Status

"""
        if check_results['warnings']:
            report += "### ⚠️  WARNINGS\n\n"
            for warn in check_results['warnings']:
                report += f"**{warn['symbol']}**: ${warn['current_price']:.2f} (Stop: ${warn['stop_loss']:.2f}, {warn['distance_pct']:.1f}% away)\n"
            report += "\n"
        else:
            report += "### ✅ All positions safe\n\n"

        report += "## Position Details\n\n"
        for result in check_results['results']:
            if result.get('status') == 'error':
                report += f"**{result['symbol']}**: ❌ {result['error']}\n"
            elif result.get('status') == 'no_stop':
                report += f"**{result['symbol']}**: ${result['current_price']:.2f} (No stop - cash equivalent)\n"
            else:
                status_emoji = "⚠️" if result['status'] == 'warning' else ("⚡" if result['status'] == 'caution' else "✅")
                report += f"**{result['symbol']}**: {status_emoji} ${result['current_price']:.2f} (Stop: ${result['stop_loss']:.2f}, {result['distance_pct']:.1f}% away)\n"

    else:
        # Weekly review report
        report = f"""# Weekly Portfolio Review - {date}

## Portfolio Summary

**Total Allocated:** ${check_results['total_allocated']:,.0f}
**Current Value:** ${check_results['current_value']:,.0f}
**Total P&L:** ${check_results['total_pnl']:,.2f} ({check_results['total_pnl_pct']:.2f}%)

## Position Details

"""
        for pos in check_results['positions']:
            report += f"""### {pos['symbol']} - {pos['status'].upper()}

**Allocated:** ${pos['allocated']:,.0f}
**Current Value:** ${pos['current_value']:,.0f}
**P&L:** ${pos['pnl']:,.2f} ({pos['pnl_pct']:.2f}%)

---

"""

    report += "\n*Generated by JARVIS Portfolio Monitor*\n"

    with open(output_file, 'w') as f:
        f.write(report)

    print(f"\n📄 Report saved: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="JARVIS Portfolio Monitor - Monitor positions and stops"
    )
    parser.add_argument(
        "--mode",
        choices=["daily", "weekly"],
        default="daily",
        help="Monitor mode: daily (stop checks) or weekly (full review)"
    )
    parser.add_argument(
        "--check-stops",
        action="store_true",
        help="Check all positions against stop levels (daily mode)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Run monitor
    if args.mode == "daily":
        results = daily_mode(check_stops=args.check_stops)
    else:
        results = weekly_mode()

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Generate and save report
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"portfolio-{args.mode}-{date_str}.md"
        output_file = REPORTS_DIR / filename

        generate_report(results, output_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
