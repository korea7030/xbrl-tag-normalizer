"""
xbrl-tag-normalizer — Lite version (free, open source)

Maps SEC XBRL tags to standard financial fields using rule-based matching.
Full version with Claude LLM fallback + S-1 stockholder table parser:
→ https://gumroad.com/YOUR_HANDLE  [link coming soon]
"""
import argparse
import json
from typing import Any, Optional

STANDARD_FIELDS = {
    "revenue", "net_income", "gross_profit", "operating_income",
    "assets", "liabilities", "equity", "eps", "shares_outstanding", "cash", "unknown",
}

RULE_MAP = {
    "revenues": "revenue",
    "totalrevenues": "revenue",
    "salesrevenuenet": "revenue",
    "netsales": "revenue",
    "servicerevenue": "revenue",
    "productrevenue": "revenue",
    "subscriptionrevenue": "revenue",
    "advertisingrevenue": "revenue",
    "licenserevenue": "revenue",
    "revenuefromrelatedparties": "revenue",
    "revenuefromcontractwithcustomer": "revenue",
    "gamingrevenue": "revenue",
    "servicesrevenue": "revenue",
    "netincomeloss": "net_income",
    "incomelossfromcontinuingoperations": "net_income",
    "comprehensiveincomenetoftax": "net_income",
    "profitloss": "net_income",
    "grossprofit": "gross_profit",
    "grossprofitloss": "gross_profit",
    "operatingincomeloss": "operating_income",
    "operatingincome": "operating_income",
    "operatingprofit": "operating_income",
    "assets": "assets",
    "assetscurrent": "assets",
    "liabilities": "liabilities",
    "liabilitiescurrent": "liabilities",
    "stockholdersequity": "equity",
    "earningspersharebasic": "eps",
    "earningspersharediluted": "eps",
    "commonstocksharesoutstanding": "shares_outstanding",
    "weightedaveragenumberofshares": "shares_outstanding",
    "cash": "cash",
    "cashandcashequivalents": "cash",
}


def _normalize_rule(tag: str, value: Any) -> Optional[dict]:
    tag_for_match = tag.split(":", 1)[1] if ":" in tag else tag
    tag_l = tag_for_match.lower()
    for key, field in RULE_MAP.items():
        if tag_l == key or tag_l.startswith(key):
            normalized_value = None if "textblock" in tag_l else value
            return {"standard_field": field, "value": normalized_value, "source_tag": tag, "confidence": 1.0}
    return None


def normalize_tag(tag: str, value: Any = None) -> dict:
    """Normalize an XBRL tag to a standard financial field.

    Returns dict with keys: standard_field, value, source_tag, confidence.
    standard_field is 'unknown' when the tag is not recognized.

    For LLM-powered fallback that handles arbitrary tags, see the full version:
    https://gumroad.com/YOUR_HANDLE
    """
    result = _normalize_rule(tag, value)
    if result is None:
        result = {"standard_field": "unknown", "value": value, "source_tag": tag, "confidence": 0.0}
    if "textblock" in tag.lower():
        result["value"] = None
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize XBRL tags to standard financial fields (Lite)")
    parser.add_argument("--tag", required=True)
    parser.add_argument("--value", type=float)
    args = parser.parse_args()
    print(json.dumps(normalize_tag(args.tag, args.value), ensure_ascii=False))


if __name__ == "__main__":
    main()
