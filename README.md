```markdown
# multimodal-osint-risk-analyst

> **Enterprise-grade Open-Source Intelligence (OSINT) agent skill** for mapping global corporate dependencies, geopolitical choke points, and real-time operational risks via deterministic multi-vector heuristic analysis.

[![Skill Registry](https://img.shields.io/badge/Registry-Active-22c55e)](./SKILL.md)
[![Confidence Model](https://img.shields.io/badge/Confidence-Weighted-3b82f6)](./SKILL.md)
[![Temporal Filter](https://img.shields.io/badge/Temporal-2026-ef4444)](./SKILL.md)
[![Deterministic](https://img.shields.io/badge/Output-Deterministic-a855f7)](./SKILL.md)

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Execution Pipeline (4 Phases)](#execution-pipeline-4-phases)
- [Heuristic Risk Vectors](#heuristic-risk-vectors)
- [Tool Ingestion Matrix](#tool-ingestion-matrix)
- [Output Schema](#output-schema)
- [Confidence Scoring Model](#confidence-scoring-model)
- [Technical Implementation](#technical-implementation)
- [Deployment](#deployment)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENT RUNTIME (Kimi)                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  web_search │  │ web_open_url│  │get_data_src │  │  show_widget /      │ │
│  │  (News/Geo) │  │ (Filings)   │  │ (Fin/Legal) │  │  ipython runtime    │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         └─────────────────┴─────────────────┴────────────────────┘          │
│                                    │                                        │
│                         ┌──────────▼──────────┐                             │
│                         │   SKILL ORCHESTRATOR  │                           │
│                         │  multimodal-osint-    │                           │
│                         │  risk-analyst         │                           │
│                         └──────────┬──────────┘                             │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐             │
│         ▼                          ▼                          ▼             │
│  ┌─────────────┐            ┌─────────────┐            ┌─────────────┐      │
│  │  Phase 1    │ ───────►   │  Phase 2    │ ───────►   │  Phase 3    │      │
│  │  Node       │            │  Multimodal │            │  Cross-     │      │
│  │  Profiling  │            │  Ingestion  │            │  Correlation│      │
│  └─────────────┘            └─────────────┘            └──────┬──────┘      │
│                                                               │             │
│                                                        ┌──────▼──────┐      │
│                                                        │  Phase 4    │      │
│                                                        │  Executive  │      │
│                                                        │  Reporting  │      │
│                                                        └─────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Execution Pipeline (4 Phases)

| Phase | Objective | Input | Output | Data Surfaces |
|-------|-----------|-------|--------|---------------|
| **P1 — Node Profiling** | Map primary → secondary → tertiary corporate dependencies | Target entity (corporation, asset, trade corridor) | Structured Node Hierarchy Table with depth indicators, jurisdiction tags, revenue dependency % | OpenCorporates, SEC EDGAR, UK Companies House, EU Business Registers, ESG disclosures, procurement records |
| **P2 — Multimodal Ingestion** | Parallel collection across logistics, geopolitical, and financial/legal surfaces | Node map from P1 | Timestamped, multi-sourced raw data corpus (constrained to CY2026) | AIS vessel data, GDELT/NewsAPI, OFAC SDN, NOAA/USGS, Federal Register, WTO panels |
| **P3 — Vulnerability Assessment** | Multi-vector heuristic analysis with confidence-weighted scoring | Raw corpus from P2 | Global Vulnerability Index (GVI) 0-100 matrix + per-vector risk scores | Cross-referenced sanctions lists, geospatial conflict overlays, credit rating deltas, transit route histories |
| **P4 — Executive Reporting** | Compile unstructured data into an enterprise-ready risk brief | GVI matrix + node map + scenario models | Scannable markdown matrices, predictive scenario planning, alternative trade routing | Deterministic markdown tables, probability-weighted scenario trees, mitigation action items |

---

## Heuristic Risk Vectors

The skill evaluates **8 deterministic heuristic vectors**. Each vector is scored `0–100` and weighted by a tri-factor confidence model.

| # | Vector | Detection Logic | Threshold | Data Anchors |
|---|--------|-----------------|-----------|--------------|
| 1 | **Single Point of Failure** | Supplier provides `>60%` of critical input with no viable alternative within `90-day` lead time | `>60%` concentration | Procurement data, trade volume, supplier count |
| 2 | **Geographic Concentration** | `>40%` of supply chain nodes reside in a single region with elevated risk score | `>40%` geo-cluster | Node map, geopolitical indices (e.g., Fragile States Index) |
| 3 | **Sanctions Exposure** | Direct or indirect UBO link to OFAC SDN, EU Consolidated, or UN Sanctions lists | Any match | Ownership chains, beneficial ownership registries, joint-venture mappings |
| 4 | **Regulatory Shift Risk** | Pending legislation, trade policy change, or active WTO dispute panel affecting target HS codes | Bill introduced or panel active | Federal Register, EU Official Journal, legislative trackers |
| 5 | **Conflict Proximity** | Active kinetic conflict (ACLED `fatality >0`) within `100km` of critical facility | `≤100km` radius | ACLED, GDACS, satellite imagery anomaly detection |
| 6 | **Climate Vulnerability** | Facility located in zone with `>1-in-10` annual probability of flood, drought, or seismic event | `>10%` AEP | NOAA, USGS, IPCC AR6 projections, ECMWF seasonal forecasts |
| 7 | **Financial Distress** | Supplier credit rating downgrade or liquidity ratio below sector median | Downgrade or `Q<median` | S&P/Moody's/Fitch, SEC 10-K/Q filings, Altman Z-score |
| 8 | **Transit Chokepoint** | Route traverses strait/canal with documented disruption history or elevated piracy/conflict risk | Historical disruption `≥2` events in 5yr | AIS vessel tracking, Lloyd's List, port authority reports |

### Global Vulnerability Index (GVI) Bands

| Score | Band | Color | Interpretation |
|-------|------|-------|----------------|
| `0–25` | **Low Risk** | 🟢 | Resilient supply architecture; diversified nodes and routes |
| `26–50` | **Moderate Risk** | 🟡 | Observable vulnerabilities; monitoring recommended |
| `51–75` | **High Risk** | 🟠 | Active threat vectors; mitigation planning required |
| `76–100` | **Critical Risk** | 🔴 | Cascade failure probable; immediate executive action |

---

## Tool Ingestion Matrix

| Analysis Domain | Primary Tool | API / Route | Fallback |
|-----------------|-------------|-------------|----------|
| **Equity & Financial Metrics** | `get_data_source` | `yahoo_finance` · `stock_finance_data` | `web_search` with ticker + `2026` filter |
| **Sanctions & Legal Compliance** | `web_search` + `web_open_url` | OFAC SDN · EU Consolidated · UN Sanctions · UK Sanctions List | — |
| **News & Geopolitical Events** | `web_search` | Date-filtered queries (`after:2026-01-01`) + region keywords | `web_open_url` on Tier-1 wire URLs (Reuters, Bloomberg, FT) |
| **Academic & Technical Research** | `get_data_source` | `arxiv` · `scholar` | `web_search` with `site:arxiv.org OR site:scholar.google.com` |
| **Macroeconomic Indicators** | `get_data_source` | `world_bank_open_data` · `imf` | `web_search` with `WEO` or `World Bank Data` |
| **Risk Visualization** | `show_widget` | SVG/Canvas risk dashboards, dependency graphs, heatmaps | `ipython` (Matplotlib/Plotly static exports) |
| **Structured Data Export** | `ipython` | Pandas DataFrames → CSV/JSON/Parquet | — |

---

## Output Schema

Every execution produces a deterministic, scannable intelligence brief with the following mandatory sections:

```
┌────────────────────────────────────────────────────────────────────────────┐
│  INTELLIGENCE BRIEF: [TARGET ENTITY]                                       │
│  Classification: OPEN SOURCE | Date: [YYYY-MM-DD] | Analyst: Kimi OSINT    │
│  Confidence: [High / Medium / Low] | GVI: [XX/100] [COLOR] [TREND ↗ → ↘]  │
├────────────────────────────────────────────────────────────────────────────┤
│  1. EXECUTIVE SUMMARY (3-4 sentence high-density thesis)                   │
├────────────────────────────────────────────────────────────────────────────┤
│  2. GLOBAL VULNERABILITY INDEX                                             │
│     Score: [XX/100] | Trend: [↗ improving / → stable / ↘ deteriorating]    │
│     Confidence Interval: [XX ± X]                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  3. NODE DEPENDENCY MAP                                                     │
│     Entity | Tier | Jurisdiction | Sector | Risk Level | Key Exposure       │
│     ● Low ● Moderate ● High ● Critical                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  4. RISK VECTOR BREAKDOWN (sorted by severity descending)                   │
│     Vector | Score | Confidence | Trend | Primary Data Source               │
├─────────────────────────────────────────────────────────────────────────────┤
│  5. SCENARIO ANALYSIS                                                       │
│     Base Case    (P=XX%) — Most likely 12-month trajectory                  │
│     Upside Case  (P=XX%) — Risk mitigation succeeds                         │
│     Downside Case(P=XX%) — Cascade failure triggered                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  6. PROACTIVE MITIGATION STRATEGIES                                         │
│     • Alternative Sourcing — specific regions/suppliers                     │
│     • Logistics Rerouting — corridor swaps with cost/time deltas            │
│     • Risk Hedging — insurance, derivatives, contractual clauses            │
│     • Monitoring Triggers — reassessment frequency & data watchpoints       │
├─────────────────────────────────────────────────────────────────────────────┤
│  7. DATA LINEAGE & PROVENANCE                                               │
│     Source | URL | Retrieval Timestamp | Inferred / Direct Observation      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Confidence Scoring Model

All risk assertions are scored via a **tri-factor confidence heuristic**:

```
Confidence Score = (Source Count × 0.30) + (Source Authority × 0.40) + (Data Recency × 0.30)
```

| Factor | Weight | Scoring Rubric |
|--------|--------|----------------|
| **Source Count** | `0.30` | `1` source = 25pts · `2` sources = 60pts · `3+` sources = 100pts |
| **Source Authority** | `0.40` | Tier-3 (social/blog) = 20pts · Tier-2 (trade pub) = 60pts · Tier-1 (gov/regulatory/filing) = 100pts |
| **Data Recency** | `0.30` | `>90 days` = 20pts · `30-90 days` = 60pts · `<30 days` = 100pts |

**Hard Constraints:**
- `High` or `Critical` risk flags require **≥2 independent Tier-1 or Tier-2 sources**.
- Unverified social media claims are **instantly discounted** to `Confidence = 0` unless corroborated.
- Speculative language ("may", "could", "possibly") triggers an automatic **−15pt confidence penalty**.

---

## Technical Implementation

### LLM Function-Calling Architecture

The skill is implemented as a **declarative orchestration layer** on top of the Kimi agent runtime. It does not execute arbitrary code. Instead, it constrains the LLM's tool-selection policy through a deterministic prompt schema embedded in `SKILL.md`:

```yaml
---
name: multimodal-osint-risk-analyst
description: >
  Advanced OSINT and corporate risk intelligence agent...
---
```

The runtime parses this YAML frontmatter to:
1. **Route intent** — trigger keywords (e.g., *"supply chain risk"*, *"sanctions screening"*) activate the skill via regex + semantic matching.
2. **Constrain tool selection** — each phase declares a primary tool and fallback, preventing the LLM from hallucinating non-existent APIs.
3. **Enforce output schema** — the markdown template is injected into the system context, ensuring every response adheres to the 7-section brief format.

### Deterministic Prompt Engineering

The skill employs **structured few-shot prompting with chain-of-thought (CoT) constraints**:

- **Phase-gating**: The LLM is instructed to complete Phase 1 (node profiling) before invoking Phase 2 tools. This prevents premature data ingestion on an unmapped target.
- **Temporal guardrails**: All `web_search` queries are suffixed with `2026` or date-range operators (`after:2026-01-01`) to eliminate stale signal.
- **Source anchoring**: Every risk claim must terminate in a citation pattern: `[(Source Type) | (URL) | (Retrieval Date)]`. Claims without anchors are rejected by the output validator.
- **Confidence floor**: The CoT preamble includes: *"If confidence score < 50, downgrade risk level by one band and flag as 'Requires Verification'."*

### Multi-Step Agent Workflows

The execution graph is a **directed acyclic workflow (DAG)** with explicit data dependencies:

```
P1: Node Profiling
  └─► emits: Node_Hierarchy_Table[]
      │
      ▼
P2: Multimodal Ingestion (parallel fan-out)
  ├─► Logistics Thread    → AIS + port data
  ├─► Geopolitical Thread → news + regulatory feeds
  └─► Financial Thread    → sanctions + credit data
      │
      ▼
P3: Cross-Correlation (reduce / join)
  └─► emits: GVI_Matrix + Risk_Vector_Scores[]
      │
      ▼
P4: Executive Reporting (render)
  └─► emits: Markdown_Brief + Widget_Dashboard
```

- **Parallelism**: Phases 2a/2b/2c execute concurrently via the agent's multi-tool call capability.
- **Deterministic reduce**: Phase 3 performs a left-join on `entity_id` across all three threads, surfacing only intersections with `confidence ≥ 50`.
- **Idempotency**: Re-running the skill on the same target within a 24-hour window hits cached retrieval timestamps, avoiding redundant API calls.

### Safety & Compliance Layer

| Rule                   | Implementation                                                                  |
|------------------------|---------------------------------------------------------------------------------|
| No insider information | All data paths terminate at public registries, filings, or open APIs            |
| Jurisdiction tagging   | Every node is tagged with applicable legal framework (OFAC, EU, UN, UK)         |
| Temporal accuracy      | Search queries auto-inject current calendar year (`2026`)                       |
| Speculative dampening  | Unverified social media → `confidence = 0`; corroboration required for elevation|

---

## Deployment

```bash
# Skill registry location
/app/.agents/skills/multimodal-osint-risk-analyst/SKILL.md

# Activation trigger (example user prompt)
"Assess supply chain risk for TSMC's Arizona fab, focusing on water scarcity
 and geopolitical export control exposure."

# Expected runtime behavior:
# 1. Skill activates on keyword match
# 2. P1: Profiles TSMC Arizona → parent (TSMC Taiwan) → key suppliers (ASML, AMAT, LRCX)
# 3. P2: Ingests Arizona drought data (NOAA), BIS export controls, ASML licensing restrictions
# 4. P3: Correlates water stress × export control risk × single-source lithography dependency
# 5. P4: Emits GVI score, node map, scenario analysis, and mitigation strategies
```

---

**License:** MIT · **Maintainer:** Senior AI Systems Architect · **Registry:** `/app/.agents/skills/multimodal-osint-risk-analyst/SKILL.md`
```
