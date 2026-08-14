"""
Financial Data Client

Fetches equity prices, credit metrics, and macroeconomic indicators from
public APIs (Yahoo Finance, World Bank, IMF).
"""

from __future__ import annotations

from typing import Any

import requests


class FinancialDataClient:
    """
    Multi-source financial data fetcher with caching and rate-limiting.
    """

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def get_stock_metrics(self, ticker: str) -> dict[str, Any] | None:
        """
        Fetch key financial metrics from Yahoo Finance v8 API.

        Args:
            ticker: Stock ticker symbol (e.g., "TSM", "AMAT").

        Returns:
            Dict with price, market_cap, pe_ratio, fifty_two_week_range.
        """
        if ticker in self._cache:
            return self._cache[ticker]

        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            data = resp.json()
            meta = data["chart"]["result"][0]["meta"]
            result = {
                "ticker": ticker,
                "currency": meta.get("currency"),
                "regular_market_price": meta.get("regularMarketPrice"),
                "previous_close": meta.get("previousClose"),
                "fifty_two_week_high": meta.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": meta.get("fiftyTwoWeekLow"),
            }
            self._cache[ticker] = result
            return result
        except Exception:
            return None

    def get_world_bank_indicator(self, indicator: str, country: str) -> list[dict[str, Any]]:
        """
        Fetch World Bank development indicators.

        Args:
            indicator: WB indicator code (e.g., "NY.GDP.MKTP.CD").
            country: ISO-3166 country code.

        Returns:
            List of {year, value} dicts.
        """
        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
        params = {"format": "json", "date": "2020:2026", "per_page": 50}
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if len(data) > 1:
                return [{"year": int(d["date"]), "value": d["value"]} for d in data[1] if d["value"]]
        except Exception:
            pass
        return []
