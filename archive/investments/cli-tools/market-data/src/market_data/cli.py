#!/usr/bin/env python3
"""
JARVIS Market Data CLI Tool

Fetches real market data using yfinance for investment analysis.
"""

import json
from datetime import datetime, timedelta
from typing import Optional

import typer
import yfinance as yf
from rich import print as rprint
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="JARVIS Market Data Tool - Fetch real-time market data")
console = Console()


@app.command()
def current(
    symbol: str = typer.Argument(..., help="Stock/ETF symbol (e.g., SPY, QQQ)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Get current price and basic info for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        data = {
            "symbol": symbol.upper(),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose"),
            "open": info.get("open") or info.get("regularMarketOpen"),
            "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
            "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
            "volume": info.get("volume") or info.get("regularMarketVolume"),
            "market_cap": info.get("marketCap"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
        }

        if json_output:
            print(json.dumps(data, indent=2))
        else:
            table = Table(title=f"{symbol.upper()} - Current Market Data")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            for key, value in data.items():
                if value is not None:
                    if isinstance(value, (int, float)):
                        if key in ["volume", "market_cap"]:
                            formatted = f"{value:,.0f}"
                        else:
                            formatted = f"${value:,.2f}"
                    else:
                        formatted = str(value)
                    table.add_row(key.replace("_", " ").title(), formatted)

            console.print(table)

    except Exception as e:
        console.print(f"[red]Error fetching data for {symbol}: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def history(
    symbol: str = typer.Argument(..., help="Stock/ETF symbol"),
    days: int = typer.Option(200, "--days", "-d", help="Number of days of history"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Get historical price data for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        hist = ticker.history(start=start_date, end=end_date)

        if hist.empty:
            console.print(f"[red]No data found for {symbol}[/red]")
            raise typer.Exit(1)

        if json_output:
            # Convert to JSON-friendly format
            data = {
                "symbol": symbol.upper(),
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "data_points": len(hist),
                "latest_price": float(hist['Close'].iloc[-1]),
                "prices": [
                    {
                        "date": idx.strftime("%Y-%m-%d"),
                        "open": float(row['Open']),
                        "high": float(row['High']),
                        "low": float(row['Low']),
                        "close": float(row['Close']),
                        "volume": int(row['Volume']),
                    }
                    for idx, row in hist.iterrows()
                ]
            }
            print(json.dumps(data, indent=2))
        else:
            console.print(f"\n[cyan]{symbol.upper()} - Last {len(hist)} trading days[/cyan]")
            console.print(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            console.print(f"Latest Close: [green]${hist['Close'].iloc[-1]:.2f}[/green]")
            console.print(f"Period High: ${hist['High'].max():.2f}")
            console.print(f"Period Low: ${hist['Low'].min():.2f}")
            console.print(f"\nUse --json flag for full historical data")

    except Exception as e:
        console.print(f"[red]Error fetching history for {symbol}: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def indicators(
    symbol: str = typer.Argument(..., help="Stock/ETF symbol"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Calculate technical indicators (SMAs, RSI, MACD)."""
    try:
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=250)  # Need extra data for 200 SMA

        hist = ticker.history(start=start_date, end=end_date)

        if len(hist) < 200:
            console.print(f"[yellow]Warning: Only {len(hist)} days of data available[/yellow]")

        # Calculate SMAs
        close_prices = hist['Close']
        sma_20 = close_prices.rolling(window=20).mean().iloc[-1] if len(close_prices) >= 20 else None
        sma_50 = close_prices.rolling(window=50).mean().iloc[-1] if len(close_prices) >= 50 else None
        sma_150 = close_prices.rolling(window=150).mean().iloc[-1] if len(close_prices) >= 150 else None
        sma_200 = close_prices.rolling(window=200).mean().iloc[-1] if len(close_prices) >= 200 else None

        current_price = close_prices.iloc[-1]

        # Calculate RSI
        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1]

        rsi = calculate_rsi(close_prices) if len(close_prices) >= 14 else None

        # Calculate MACD
        def calculate_macd(prices):
            ema_12 = prices.ewm(span=12, adjust=False).mean()
            ema_26 = prices.ewm(span=26, adjust=False).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            return macd_line.iloc[-1], signal_line.iloc[-1]

        macd, macd_signal = calculate_macd(close_prices) if len(close_prices) >= 26 else (None, None)

        data = {
            "symbol": symbol.upper(),
            "current_price": float(current_price),
            "sma_20": float(sma_20) if sma_20 else None,
            "sma_50": float(sma_50) if sma_50 else None,
            "sma_150": float(sma_150) if sma_150 else None,
            "sma_200": float(sma_200) if sma_200 else None,
            "price_vs_sma_50_pct": float((current_price - sma_50) / sma_50 * 100) if sma_50 else None,
            "price_vs_sma_150_pct": float((current_price - sma_150) / sma_150 * 100) if sma_150 else None,
            "price_vs_sma_200_pct": float((current_price - sma_200) / sma_200 * 100) if sma_200 else None,
            "rsi_14": float(rsi) if rsi else None,
            "macd": float(macd) if macd else None,
            "macd_signal": float(macd_signal) if macd_signal else None,
        }

        if json_output:
            print(json.dumps(data, indent=2))
        else:
            table = Table(title=f"{symbol.upper()} - Technical Indicators")
            table.add_column("Indicator", style="cyan")
            table.add_column("Value", style="green")
            table.add_column("vs Price", style="yellow")

            table.add_row("Current Price", f"${current_price:.2f}", "-")

            if sma_20:
                diff_pct = (current_price - sma_20) / sma_20 * 100
                table.add_row("20 SMA", f"${sma_20:.2f}", f"{diff_pct:+.1f}%")

            if sma_50:
                diff_pct = (current_price - sma_50) / sma_50 * 100
                table.add_row("50 SMA", f"${sma_50:.2f}", f"{diff_pct:+.1f}%")

            if sma_150:
                diff_pct = (current_price - sma_150) / sma_150 * 100
                table.add_row("150 SMA", f"${sma_150:.2f}", f"{diff_pct:+.1f}%")

            if sma_200:
                diff_pct = (current_price - sma_200) / sma_200 * 100
                table.add_row("200 SMA", f"${sma_200:.2f}", f"{diff_pct:+.1f}%")

            console.print(table)

            if rsi:
                rsi_status = "Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Neutral"
                console.print(f"\nRSI (14): [cyan]{rsi:.1f}[/cyan] - {rsi_status}")

            if macd and macd_signal:
                macd_status = "Bullish" if macd > macd_signal else "Bearish"
                console.print(f"MACD: [cyan]{macd:.2f}[/cyan] vs Signal: [cyan]{macd_signal:.2f}[/cyan] - {macd_status}")

    except Exception as e:
        console.print(f"[red]Error calculating indicators for {symbol}: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def stage(
    symbol: str = typer.Argument(..., help="Stock/ETF symbol"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Determine the current market stage (1-4) for a symbol."""
    try:
        # First get indicators
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=250)

        hist = ticker.history(start=start_date, end=end_date)
        close_prices = hist['Close']
        current_price = close_prices.iloc[-1]

        # Calculate SMAs
        sma_50 = close_prices.rolling(window=50).mean().iloc[-1] if len(close_prices) >= 50 else None
        sma_150 = close_prices.rolling(window=150).mean().iloc[-1] if len(close_prices) >= 150 else None
        sma_200 = close_prices.rolling(window=200).mean().iloc[-1] if len(close_prices) >= 200 else None

        # Calculate RSI
        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1]

        rsi = calculate_rsi(close_prices) if len(close_prices) >= 14 else None

        # Determine stage based on criteria
        stage_num = None
        stage_name = None
        confidence = "Low"

        if sma_50 and sma_150 and sma_200:
            # Stage 2: Markup (bullish uptrend)
            if (current_price > sma_50 > sma_150 > sma_200 and
                (rsi is None or 50 < rsi < 70)):
                stage_num = 2
                stage_name = "Markup"
                confidence = "High"

            # Stage 4: Decline (bearish downtrend)
            elif (current_price < sma_50 < sma_150 and
                  (rsi is None or rsi < 50)):
                stage_num = 4
                stage_name = "Decline"
                confidence = "High"

            # Stage 1: Accumulation (bottoming)
            elif (current_price < sma_200 or abs(current_price - sma_150) / sma_150 < 0.02):
                stage_num = 1
                stage_name = "Accumulation"
                confidence = "Medium"

            # Stage 3: Distribution (topping)
            else:
                stage_num = 3
                stage_name = "Distribution"
                confidence = "Medium"

        data = {
            "symbol": symbol.upper(),
            "stage": stage_num,
            "stage_name": stage_name,
            "confidence": confidence,
            "current_price": float(current_price),
            "sma_50": float(sma_50) if sma_50 else None,
            "sma_150": float(sma_150) if sma_150 else None,
            "sma_200": float(sma_200) if sma_200 else None,
            "rsi": float(rsi) if rsi else None,
        }

        if json_output:
            print(json.dumps(data, indent=2))
        else:
            stage_emoji = {1: "⏸️", 2: "📈", 3: "⚠️", 4: "📉"}
            emoji = stage_emoji.get(stage_num, "❓")

            console.print(f"\n{emoji} [bold]{symbol.upper()} Stage Assessment[/bold]")
            console.print(f"Stage: [cyan]Stage {stage_num} - {stage_name}[/cyan]")
            console.print(f"Confidence: {confidence}")
            console.print(f"\nCurrent Price: ${current_price:.2f}")
            if sma_50:
                console.print(f"50 SMA: ${sma_50:.2f}")
            if sma_150:
                console.print(f"150 SMA: ${sma_150:.2f}")
            if sma_200:
                console.print(f"200 SMA: ${sma_200:.2f}")
            if rsi:
                console.print(f"RSI: {rsi:.1f}")

    except Exception as e:
        console.print(f"[red]Error determining stage for {symbol}: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def news(
    symbol: str = typer.Argument(..., help="Stock/ETF symbol"),
    count: int = typer.Option(5, "--count", "-n", help="Number of news articles to fetch"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Get recent news articles for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        news_items = ticker.news

        if not news_items:
            console.print(f"[yellow]No news found for {symbol}[/yellow]")
            raise typer.Exit(0)

        # Limit to requested count
        news_items = news_items[:count]

        if json_output:
            data = {
                "symbol": symbol.upper(),
                "count": len(news_items),
                "articles": [
                    {
                        "title": item.get("title", ""),
                        "publisher": item.get("publisher", ""),
                        "link": item.get("link", ""),
                        "published": datetime.fromtimestamp(item.get("providerPublishTime", 0)).strftime("%Y-%m-%d %H:%M") if item.get("providerPublishTime") else None,
                        "type": item.get("type", ""),
                    }
                    for item in news_items
                ]
            }
            print(json.dumps(data, indent=2))
        else:
            console.print(f"\n[bold cyan]{symbol.upper()} - Recent News[/bold cyan]")
            console.print(f"Showing {len(news_items)} most recent articles\n")

            for i, item in enumerate(news_items, 1):
                title = item.get("title", "No title")
                publisher = item.get("publisher", "Unknown")
                link = item.get("link", "")
                pub_time = item.get("providerPublishTime")

                if pub_time:
                    pub_date = datetime.fromtimestamp(pub_time).strftime("%Y-%m-%d %H:%M")
                else:
                    pub_date = "Unknown date"

                console.print(f"[cyan]{i}.[/cyan] {title}")
                console.print(f"   Source: {publisher} | {pub_date}")
                if link:
                    console.print(f"   Link: {link}")
                console.print()

    except Exception as e:
        console.print(f"[red]Error fetching news for {symbol}: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def fundamentals(
    symbol: str = typer.Argument(..., help="Stock/ETF symbol"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Get fundamental data for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # Extract key fundamental data
        data = {
            "symbol": symbol.upper(),
            "name": info.get("longName") or info.get("shortName", ""),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE") or info.get("forwardPE"),
            "dividend_yield": info.get("dividendYield"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "average_volume": info.get("averageVolume"),
            "beta": info.get("beta"),
            "description": info.get("longBusinessSummary", "")[:200] + "..." if info.get("longBusinessSummary") else None,
        }

        if json_output:
            print(json.dumps(data, indent=2))
        else:
            console.print(f"\n[bold cyan]{data['name']} ({symbol.upper()})[/bold cyan]\n")

            if data["sector"]:
                console.print(f"Sector: {data['sector']}")
            if data["industry"]:
                console.print(f"Industry: {data['industry']}")

            console.print()

            table = Table(title="Key Fundamentals")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            if data["market_cap"]:
                market_cap_b = data["market_cap"] / 1_000_000_000
                table.add_row("Market Cap", f"${market_cap_b:.2f}B")

            if data["pe_ratio"]:
                table.add_row("P/E Ratio", f"{data['pe_ratio']:.2f}")

            if data["dividend_yield"]:
                yield_pct = data["dividend_yield"] * 100
                table.add_row("Dividend Yield", f"{yield_pct:.2f}%")

            if data["52_week_high"]:
                table.add_row("52-Week High", f"${data['52_week_high']:.2f}")

            if data["52_week_low"]:
                table.add_row("52-Week Low", f"${data['52_week_low']:.2f}")

            if data["average_volume"]:
                vol_m = data["average_volume"] / 1_000_000
                table.add_row("Avg Volume", f"{vol_m:.2f}M")

            if data["beta"]:
                table.add_row("Beta", f"{data['beta']:.2f}")

            console.print(table)

            if data["description"]:
                console.print(f"\n[bold]Description:[/bold]")
                console.print(data["description"])

    except Exception as e:
        console.print(f"[red]Error fetching fundamentals for {symbol}: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
