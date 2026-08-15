"""
Unit tests for the deterministic risk scoring engine.
"""

from __future__ import annotations

import pytest

from osint_risk_analyst.core.risk_engine import RiskEngine
from osint_risk_analyst.models.risk_models import CorporateNode, RiskLevel


@pytest.fixture
def engine() -> RiskEngine:
    return RiskEngine()


@pytest.fixture
def mock_nodes() -> list[CorporateNode]:
    return [
        CorporateNode(
            entity_id="TEST-001",
            name="Test Fab Co",
            tier=1,
            jurisdiction="US",
            sector="Semiconductors",
            revenue_dependency_pct=100.0,
            latitude=33.0,
            longitude=-112.0,
            risk_level=RiskLevel.HIGH,
            key_exposure="Test exposure",
        ),
        CorporateNode(
            entity_id="ASML-001",
            name="ASML Holding N.V.",
            tier=2,
            jurisdiction="NL",
            sector="Semiconductors",
            revenue_dependency_pct=85.0,
            latitude=51.0,
            longitude=5.0,
            risk_level=RiskLevel.CRITICAL,
            key_exposure="Sole EUV",
        ),
    ]


def test_assess_produces_gvi(engine: RiskEngine, mock_nodes: list[CorporateNode]) -> None:
    corpus = {
        "metadata": {"ingestion_timestamp": "2026-08-14T22:06:00Z"},
        "sanctions": {"data": {"hits": [], "screened_count": 2}},
        "news": {"data": {"articles": []}},
        "financial": {"data": {}},
        "logistics": {"data": {}},
        "geopolitical": {"data": {}},
        "climate": {"data": {}},
        "provenance": [],
    }
    gvi = engine.assess(mock_nodes, corpus)
    assert 0 <= gvi.gvi_score <= 100
    assert gvi.confidence_interval >= 0
    assert len(gvi.vectors) == 8
    assert any(v.threshold_triggered for v in gvi.vectors)


def test_spof_detection(engine: RiskEngine, mock_nodes: list[CorporateNode]) -> None:
    corpus = {"sanctions": {"data": {}}, "news": {"data": {}}, "financial": {"data": {}}, "logistics": {"data": {}}, "geopolitical": {"data": {}}, "climate": {"data": {}}, "provenance": []}
    gvi = engine.assess(mock_nodes, corpus)
    spof = next(v for v in gvi.vectors if v.vector_id == "SPOF-001")
    assert spof.threshold_triggered is True
    assert spof.score >= 60.0


def test_scenario_probabilities_sum_to_one(engine: RiskEngine, mock_nodes: list[CorporateNode]) -> None:
    corpus = {"sanctions": {"data": {}}, "news": {"data": {}}, "financial": {"data": {}}, "logistics": {"data": {}}, "geopolitical": {"data": {}}, "climate": {"data": {}}, "provenance": []}
    gvi = engine.assess(mock_nodes, corpus)
    total_prob = sum(s.probability_weight for s in gvi.scenarios)
    assert abs(total_prob - 1.0) < 0.01


def test_mitigations_address_triggered_vectors(engine: RiskEngine, mock_nodes: list[CorporateNode]) -> None:
    corpus = {"sanctions": {"data": {}}, "news": {"data": {}}, "financial": {"data": {}}, "logistics": {"data": {}}, "geopolitical": {"data": {}}, "climate": {"data": {}}, "provenance": []}
    gvi = engine.assess(mock_nodes, corpus)
    triggered = {v.vector_id for v in gvi.vectors if v.threshold_triggered}
    addressed = set()
    for m in gvi.mitigations:
        addressed.update(m.risk_vectors_addressed)
    assert len(addressed) > 0
    assert addressed.issubset({v.vector_id for v in gvi.vectors})
