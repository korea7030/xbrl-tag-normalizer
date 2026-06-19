# xbrl-tag-normalizer

Normalize SEC XBRL tags to standard financial fields — no API key required.

```bash
python xbrl_normalizer_lite.py --tag "RevenueFromContractWithCustomerExcludingAssessedTax" --value 383285000000
```

```json
{"standard_field": "revenue", "value": 383285000000, "source_tag": "RevenueFromContractWithCustomerExcludingAssessedTax", "confidence": 1.0}
```

## The Problem

SEC filings use dozens of inconsistent tag names for the same concept:

| Company | Tag |
|---------|-----|
| Apple | `RevenueFromContractWithCustomerExcludingAssessedTax` |
| NVIDIA | `nvda:GamingRevenue` |
| Meta | `Revenues` |
| Microsoft | `RevenueFromContractWithCustomerExcludingAssessedTax` |

This tool maps all of them to `revenue` — plus 10 other standard fields.

## Supported Fields

`revenue` · `net_income` · `gross_profit` · `operating_income` · `assets` · `liabilities` · `equity` · `eps` · `shares_outstanding` · `cash` · `unknown`

## Usage

```python
from xbrl_normalizer_lite import normalize_tag

normalize_tag("nvda:GamingRevenue", 9067000000)
# {"standard_field": "revenue", "value": 9067000000, "source_tag": "nvda:GamingRevenue", "confidence": 1.0}

normalize_tag("OperatingIncomeLossTextBlock", None)
# {"standard_field": "operating_income", "value": None, "source_tag": "OperatingIncomeLossTextBlock", "confidence": 1.0}

normalize_tag("WeirdCustomTag", 12345)
# {"standard_field": "unknown", "value": 12345, "source_tag": "WeirdCustomTag", "confidence": 0.0}
```

## Limitations of This Lite Version

- Rule-based only: ~40 tag variants covered
- Returns `unknown` for anything not in the rule map
- No S-1 stockholder table parser included

## Full Version

The full version adds:
- **Claude-haiku LLM fallback** — handles any arbitrary XBRL tag, not just the 40 in the rule map
- **S-1 stockholder table parser** — fetch any SEC S-1 filing by company name, CIK, or URL and extract the ownership table as JSON
- **3 production-ready prompt sets** — 34 few-shot examples for tag normalization, section detection, and table cleaning
- **30 verified test cases**

**[$49 XBRL Pack / $149 Full Bundle → gumroad.com/YOUR_HANDLE]**

## Requirements

- Python 3.10+
- No API key needed for the lite version
