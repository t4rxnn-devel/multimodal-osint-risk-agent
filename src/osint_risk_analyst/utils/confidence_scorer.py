"""
Confidence Scoring Engine

Implements the tri-factor confidence heuristic:
  Confidence = (Source Count * 0.30) + (Source Authority * 0.40) + (Data Recency * 0.30)
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from osint_risk_analyst.models.risk_models import DataProvenance, SourceTier


class ConfidenceScorer:
    """
    Deterministic confidence calculator for risk assertions.
    """

    def calculate(self, provenance: list[DataProvenance]) -> float:
        """
        Compute confidence score from a list of provenance records.

        Args:
            provenance: List of DataProvenance objects backing a single claim.

        Returns:
            Confidence score 0-100.
        """
        if not provenance:
            return 0.0

        source_count = len(provenance)
        max_authority = max(
            (self._authority_score(p) for p in provenance),
            default=SourceTier.SOCIAL_UNVERIFIED,
        )
        min_recency = min(
            (self._recency_score(p) for p in provenance),
            default=0,
        )

        count_score = min(source_count * 30, 100)  # 1=30, 2=60, 3+=100 (capped)
        authority_score = max_authority.value * 25  # 1->25, 2->50, 3->75, 4->100
        recency_score = min_recency

        confidence = (count_score * 0.30) + (authority_score * 0.40) + (recency_score * 0.30)
        return round(confidence, 1)

    @staticmethod
    def _authority_score(prov: DataProvenance) -> SourceTier:
        """Map source type to authority tier."""
        source = prov.source_type.upper()
        if any(x in source for x in ["SEC", "OFAC", "GOV", "REGULATORY", "FEDERAL"]):
            return SourceTier.PRIMARY_FILING
        if any(x in source for x in ["EDGAR", "BIS", "EU_CONSOLIDATED", "UN_SANCTIONS"]):
            return SourceTier.GOVERNMENT_REGULATORY
        if any(x in source for x in ["REUTERS", "BLOOMBERG", "LLOYDS", "NOAA", "USGS"]):
            return SourceTier.TRADE_PUBLICATION
        return SourceTier.SOCIAL_UNVERIFIED

    @staticmethod
    def _recency_score(prov: DataProvenance) -> int:
        """Score data recency: <30 days = 100, 30-90 = 60, >90 = 20."""
        age = datetime.utcnow() - prov.retrieval_timestamp
        if age < timedelta(days=30):
            return 100
        if age < timedelta(days=90):
            return 60
        return 20
