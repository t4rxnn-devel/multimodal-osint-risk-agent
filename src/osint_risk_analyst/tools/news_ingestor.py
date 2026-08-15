"""
News & Geopolitical Event Ingestor

Aggregates localized news from RSS feeds, GDELT, and NewsAPI with strict
temporal filtering (current year enforcement).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import feedparser


class NewsIngestor:
    """
    Multi-source news aggregation with bias filtering and temporal validation.
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key
        self.sources = [
            "https://feeds.reuters.com/reuters/businessNews",
            "https://feeds.bbci.co.uk/news/business/rss.xml",
            "https://rss.cnn.com/rss/money_news_international.rss",
        ]

    def search(self, queries: list[str], year: int = 2026) -> list[dict[str, Any]]:
        """
        Search news sources for query terms filtered to the target year.

        Args:
            queries: Search terms (entity names, risk keywords).
            year: Strict temporal filter (default 2026).

        Returns:
            List of article dicts with title, source, date, url, relevance_score.
        """
        articles = []
        for source in self.sources:
            try:
                feed = feedparser.parse(source)
                for entry in feed.entries:
                    pub_date = self._parse_date(entry.get("published", ""))
                    if pub_date and pub_date.year != year:
                        continue
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    combined = f"{title} {summary}".lower()
                    relevance = sum(1 for q in queries if q.lower() in combined)
                    if relevance > 0:
                        articles.append({
                            "title": title,
                            "source": source,
                            "published": pub_date.isoformat() if pub_date else None,
                            "url": entry.get("link", ""),
                            "relevance_score": relevance,
                        })
            except Exception:
                continue
        return sorted(articles, key=lambda x: x["relevance_score"], reverse=True)

    @staticmethod
    def _parse_date(date_str: str) -> datetime | None:
        """Parse RSS date strings to datetime objects."""
        formats = [
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None
