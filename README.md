# Governance Framework

Structured analysis of a governance framework comprising 26 concepts, source materials, and operational principles.

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `data/raw/` | Source documents (master PDF, original inputs) |
| `data/processed/` | Extracted, structured framework content |
| `data/outputs/` | Scored metrics, analysis outputs |
| `notebooks/exploration/` | Extraction, EDA, scratch work |
| `notebooks/analysis/` | Structured metric-level passes |
| `src/` | Reusable Python modules |
| `docs/` | Framework documentation |
| `reports/` | Final stakeholder outputs |

## Setup

```bash
conda env create -f environment.yml
conda activate governance-framework
jupyter lab
```

## Status

- [ ] Folder structure initialized
- [ ] PDF extracted and structured
- [ ] Metric-level pass: 26 concepts
- [ ] Scoring and validation
- [ ] Reporting