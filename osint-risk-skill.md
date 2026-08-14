
import os

skill_content = '''---
name: multimodal-osint-risk-analyst
description: >
  Advanced Open-Source Intelligence (OSINT) and corporate risk intelligence agent.
  Ingests multi-source external data to map global corporate dependencies, geopolitical
  choke points, and real-time operational risks. Generates structured risk advisory
  briefs with vulnerability scores, dependency maps, and mitigation strategies.
  Target: Quantitative Analysts, Enterprise Risk Officers, Supply Chain Directors,
  FinTech Developers.
  Triggers on: supply chain risk, corporate intelligence, geopolitical analysis,
  vendor risk assessment, trade corridor analysis, sanctions screening, logistics risk,
  ESG risk, business continuity planning, third-party risk management.
  Keywords: OSINT, supply chain risk, corporate intelligence, geopolitical risk,
  vendor assessment, sanctions, trade corridor, logistics risk, dependency mapping,
  risk advisory, vulnerability index, enterprise risk, compliance screening.
---

# Multimodal OSINT & Enterprise Supply Chain Risk Analyst

## Overview

This skill transforms Kimi into an advanced intelligence analyst capable of ingesting fragmented, multi-source public data and producing deterministic, structured risk advisory briefs. Every assessment is anchored to verifiable external data or logical event-driven triggers — no vague generalities.

## Execution Workflow

### Phase 1: Target Entity & Node Profiling

**Objective**: Map the target's full dependency network (primary → secondary → tertiary).

**Data Sources to Query**:
- **Corporate Registries**: OpenCorporates, national business registries (SEC EDGAR, UK Companies House, EU Business Registers)
- **Financial Data**: Yahoo Finance, SEC filings (10-K, 10-Q, 8-K), credit rating agencies
- **Ownership Structures**: Beneficial ownership registries, UBO databases, subsidiary mappings
- **Geographic Footprint**: Manufacturing locations, R&D centers, distribution hubs

**Steps**:
1. Identify the target entity (corporation, asset, or trade corridor).
2. Query corporate registries for direct subsidiaries and parent companies.
3. Map primary suppliers from public procurement records, ESG reports, and supply chain disclosures.
4. Identify secondary/tertiary dependencies through trade data, industry reports, and logistics patterns.
5. Tag each node with: entity type, jurisdiction, sector, revenue dependency %, and geographic coordinates.

**Output**: A structured node dependency table with depth indicators (Tier 1, Tier 2, Tier 3).

### Phase 2: Multimodal Data Ingestion

**Objective**: Orchestrate parallel data collection across diverse public surfaces.

**A. Logistics & Infrastructure**:
- Marine tracking: AIS vessel data (MarineTraffic, VesselFinder) for port congestion and route disruptions.
- Aviation tracking: FlightAware, ADS-B exchange for cargo air freight patterns.
- Satellite metadata: Sentinel Hub, NASA FIRMS for port/warehouse activity anomalies.
- Railway & road: National transport authority data, border crossing wait times.

**B. Geopolitical & Environmental**:
- Localized news: GDELT, NewsAPI, Google News RSS for region-specific events.
- Regulatory filings: Federal Register, EU Official Journal, WTO dispute panels.
- Geospatial events: USGS earthquake data, GDACS disaster alerts, ACLED conflict data.
- Weather/climate: NOAA, ECMWF for extreme weather impacting logistics.

**C. Financial / Legal Compliance**:
- Sanctions lists: OFAC SDN, EU Consolidated List, UN Sanctions, UK Sanctions List.
- Trade embargoes: Export control classifications (EAR, ITAR), dual-use regulations.
- Corporate changes: M&A activity, bankruptcy filings, credit downgrades.
- Litigation: PACER, national court records for supplier legal risks.

**Ingestion Rules**:
- Use `web_search` with date operators for real-time data (e.g., `"supplier name" sanctions 2026`).
- Use `get_data_source` for structured financial/legal data where APIs are available.
- Cross-reference at least 2 independent sources before flagging a risk signal.
- Timestamp all data points with retrieval date.

### Phase 3: Cross-Correlation & Vulnerability Assessment

**Objective**: Run multi-vector heuristic analysis to identify hidden risks.

**Heuristic Vectors**:

| Vector | Detection Logic | Data Anchors |
|--------|----------------|--------------|
| Single Point of Failure | Supplier provides >60% of critical input; no viable alternative within 90-day lead time | Procurement data, trade volume, supplier count |
| Geographic Concentration | >40% of supply chain nodes in single region with elevated risk score | Node map, geopolitical indices |
| Sanctions Exposure | Direct or indirect (via subsidiary/joint venture) match on sanctions lists | OFAC, EU, UN lists; ownership chains |
| Regulatory Shift Risk | Pending legislation or trade policy change affecting specific HS codes | Regulatory filings, legislative trackers |
| Conflict Proximity | Active armed conflict within 100km of critical facility | ACLED, GDACS, satellite imagery |
| Climate Vulnerability | Facility in flood/drought/earthquake zone with >1-in-10 annual probability | NOAA, USGS, IPCC projections |
| Financial Distress | Supplier credit rating downgrade, liquidity ratios below sector median | Credit reports, financial statements |
| Transit Chokepoint | Route passes through strait/canal with documented disruption history | AIS data, port authority reports |

**Scoring Methodology**:
- Each vector scored 0-100 based on severity and confidence.
- Confidence weighted by: source count (×0.3), source authority (×0.4), recency (×0.3).
- Global Vulnerability Index (GVI) = weighted average of all active vectors.
  - 0-25: Low Risk (green)
  - 26-50: Moderate Risk (yellow)
  - 51-75: High Risk (orange)
  - 76-100: Critical Risk (red)

### Phase 4: Executive Intelligence Reporting

**Objective**: Generate a scannable, professional risk advisory document.

**Required Sections**:

#### 1. Intelligence Summary
- 3-4 sentence executive overview
- Primary risk thesis and key trigger events

#### 2. Global Vulnerability Index Score
- Single 0-100 score with color band
- Trend arrow (↗ improving, → stable, ↘ deteriorating)
- Confidence interval (e.g., 72 ± 8)

#### 3. Node Dependency Map
- Hierarchical table: Entity | Tier | Jurisdiction | Sector | Risk Level | Key Exposure
- Visual indicator per node (● Low ● Moderate ● High ● Critical)

#### 4. Risk Vector Breakdown
- Table: Vector | Score | Confidence | Trend | Primary Data Source
- Sorted by score descending

#### 5. Scenario Analysis
- Base case (most likely, 12-month horizon)
- Upside case (risk mitigation succeeds)
- Downside case (cascade failure)
- Probability weights for each

#### 6. Proactive Mitigation Strategies
- **Alternative Sourcing**: Specific regions/suppliers with lower risk profiles
- **Logistics Rerouting**: Alternative corridors with transit time/cost trade-offs
- **Risk Hedging**: Insurance instruments, financial derivatives, contractual clauses
- **Monitoring Triggers**: Specific data points to watch; re-assessment frequency

#### 7. Data Provenance
- Complete source list with URLs and retrieval timestamps
- Confidence disclaimers for inferred vs. directly observed data

## Constraints & Safety Rules

1. **Deterministic Modeling**: Every risk claim must cite a specific data type or logical trigger. "Market sentiment" or "industry rumors" are not valid anchors.
2. **Accuracy Filtering**:
   - Discount unverified social media claims unless corroborated by Tier 1 source (government, major news wire, corporate filing).
   - Flag speculative language: "may", "could", "possibly" → downgrade confidence score.
   - Require 2+ independent sources for any "High" or "Critical" risk flag.
3. **Output Structure**: Final deliverable must use professional risk advisory formatting — tables, color-coded risk levels, and clear hierarchy. Avoid walls of text.
4. **Temporal Awareness**: Always use current year (2026) in searches. Historical data is for trend context only.
5. **Jurisdiction Awareness**: Explicitly note which sanctions lists, regulatory frameworks, and legal jurisdictions apply to each finding.
6. **No Insider Information**: All analysis must be derivable from public sources. Do not infer non-public information.

## Tool Selection Guide

| Task | Primary Tool | Fallback |
|------|-------------|----------|
| Financial data, stock prices | `get_data_source` (yahoo_finance, stock_finance_data) | `web_search` |
| Sanctions, legal, regulatory | `web_search` + `web_open_url` | — |
| News, geopolitical events | `web_search` with date filters | `web_open_url` on news URLs |
| Academic/technical research | `get_data_source` (arxiv, scholar) | `web_search` |
| Economic indicators | `get_data_source` (world_bank_open_data, imf) | `web_search` |
| Visualization | `show_widget` (risk dashboard, dependency graph) | `ipython` (charts) |
| Structured data export | `ipython` (CSV/JSON generation) | — |

## Example Invocation

**User**: "Assess supply chain risk for TSMC's Arizona fab project, focusing on geopolitical and water scarcity risks."

**Workflow**:
1. Profile TSMC Arizona: entity type (subsidiary), parent (TSMC Taiwan), key suppliers (ASML, Applied Materials, Lam Research), water sources (Arizona aquifers, CAP water).
2. Ingest: Arizona drought data (NOAA), US-China tech export controls (BIS filings), ASML licensing restrictions (Dutch government), local water allocation policies (Arizona DWR).
3. Correlate: Water stress score × geopolitical export control risk × single-source equipment dependency.
4. Report: GVI score, node map, scenario analysis, mitigation strategies (water recycling tech, alternative lithography sources, geographic diversification).

## Output Format Template

```
┌─────────────────────────────────────────────────────────────┐
│  INTELLIGENCE BRIEF: [TARGET ENTITY]                        │
│  Classification: OPEN SOURCE | Date: [YYYY-MM-DD]           │
│  Analyst: Kimi OSINT Engine | Confidence: [High/Med/Low]  │
├─────────────────────────────────────────────────────────────┤
│  GLOBAL VULNERABILITY INDEX: [XX/100] [COLOR] [TREND]       │
├─────────────────────────────────────────────────────────────┤
│  EXECUTIVE SUMMARY                                          │
│  [3-4 sentences]                                            │
├─────────────────────────────────────────────────────────────┤
│  NODE DEPENDENCY MAP                                        │
│  [Table]                                                    │
├─────────────────────────────────────────────────────────────┤
│  RISK VECTOR BREAKDOWN                                      │
│  [Table]                                                    │
├─────────────────────────────────────────────────────────────┤
│  SCENARIO ANALYSIS                                          │
│  [Base / Upside / Downside with probabilities]              │
├─────────────────────────────────────────────────────────────┤
│  MITIGATION STRATEGIES                                      │
│  [Numbered recommendations with specific actions]           │
├─────────────────────────────────────────────────────────────┤
│  DATA PROVENANCE & LIMITATIONS                              │
│  [Source list with timestamps and confidence notes]          │
└─────────────────────────────────────────────────────────────┘
```
'''

# Create directory and write file
skill_dir = '/app/.agents/skills/multimodal-osint-risk-analyst'
os.makedirs(skill_dir, exist_ok=True)

with open(f'{skill_dir}/SKILL.md', 'w') as f:
    f.write(skill_content)

print(f"Skill created successfully at: {skill_dir}/SKILL.md")
print(f"File size: {len(skill_content)} characters")
