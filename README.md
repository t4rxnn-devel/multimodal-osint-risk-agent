# Multimodal OSINT Risk Analyst

An agentic skill for mapping corporate supply chain dependencies, geopolitical chokepoints, and operational risks using open-source intelligence.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill Spec](https://img.shields.io/badge/Spec-SKILL.md-blue)](./SKILL.md)

---

## What It Does

`multimodal-osint-risk-analyst` maps entity dependencies across corporate filings, trade databases, and real-time news to calculate a **Global Vulnerability Index (GVI)**. It evaluates supply chain concentration, sanctions exposure, regulatory shifts, and transit chokepoints through a 4-phase structured workflow.

### Execution Phases

1. **Node Profiling (P1):** Maps primary, secondary, and tertiary corporate dependencies using SEC EDGAR, OpenCorporates, and UK Companies House.
2. **Multimodal Ingestion (P2):** Parallel collection across shipping (AIS), news/geopolitics (GDELT), sanctions (OFAC/EU), and macro data.
3. **Vulnerability Assessment (P3):** Evaluates nodes across 8 weighted risk vectors to generate a GVI score ($0\text{--}100$).
4. **Executive Reporting (P4):** Produces structured markdown briefs with confidence scoring, scenario modeling, and rerouting strategies.

---

## Evaluated Risk Vectors

The analyst scores entities across 8 core heuristic vectors ($0\text{--}100$ scale):

| Vector | Trigger Condition / Threshold | Primary Sources |
| :--- | :--- | :--- |
| **Single Point of Failure** | Supplier holds $>60\%$ critical input with $>90$ day replacement lead time | SEC 10-K, procurement data |
| **Geographic Cluster** | $>40\%$ of supply chain nodes located in a single high-risk region | Node registry, Fragile States Index |
| **Sanctions Exposure** | Direct/indirect UBO link to OFAC SDN, EU, or UN sanction lists | Beneficial ownership registries |
| **Regulatory Shift** | Pending trade policy or active WTO dispute panel on key HS codes | Federal Register, EU Official Journal |
| **Conflict Proximity** | Kinetic conflict event within 100km of a critical facility | ACLED, satellite imagery |
| **Climate Hazard** | Facility in a zone with $>10\%$ annual exceedance probability for extreme weather | NOAA, USGS, IPCC AR6 |
| **Financial Distress** | Supplier credit downgrade or liquidity ratio below sector median | Moody's, S&P, SEC filings |
| **Transit Chokepoints** | Primary route traverses maritime straits with active disruption history | AIS vessel tracking, Lloyd's List |

---

## Vulnerability Scoring & Confidence

### Risk Bands

* **0–25 (Low):** Resilient supply architecture; multi-region redundancy.
* **26–50 (Moderate):** Minor regional clusters; standard monitoring.
* **51–75 (High):** Active single-point dependencies; mitigation required.
* **76–100 (Critical):** Immediate vulnerability to cascading failure.

### Confidence Scoring Model

All risk assertions are weighted by source authority, recency, and verification count:

$$\text{Confidence} = (\text{Source Count} \times 0.30) + (\text{Source Authority} \times 0.40) + (\text{Data Recency} \times 0.30)$$

* **High/Critical flags** require $\ge 2$ independent Tier-1 (government/regulatory) or Tier-2 (trade publication) sources.
* Unverified social or blog claims are discounted to 0 unless corroborated.

---

## Installation & Setup

Drop the skill file into your agent environment directory:

```bash
mkdir -p .agents/skills/
cp SKILL.md .agents/skills/multimodal-osint-risk-analyst.md
```

Example Prompt:
"Assess supply chain and geopolitical risks for TSMC's Arizona facility. Focus on semiconductor raw material dependencies and regional water scarcity."

Project Structure:

├── SKILL.md              # Core agent system prompt & workflow spec
├── README.md             # Repository documentation
└── examples/             # Sample generated risk briefs
    └── tsmc-arizona.md


License: MIT

`
mkdir -p .agents/skills/
cp SKILL.md .agents/skills/multimodal-osint-risk-analyst.md
