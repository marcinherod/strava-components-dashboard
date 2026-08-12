"""
Parses text copied from the Strava gear/components page.

Expected format (tab-separated columns, as copied from an HTML table):
Type    Brand   Model   Added   Removed Distance    Action
Frame   Lapierre    Xelius SL 500 Carbon Disc   From start      13,789.1 km Retire | Delete
"""

import re

HEADER_KEYWORDS = {"typ", "marka", "model", "dodano", "type", "brand", "model", "added"}


def parse_distance(raw: str):
    """Converts '13 789,1 km' (PL format) or '13,789.1 mi' to a float."""
    if not raw:
        return None
    cleaned = raw.replace("\xa0", " ").replace("km", "").replace("mi", "").strip()
    cleaned = re.sub(r"\s+", "", cleaned)   # remove thousands separator spaces
    cleaned = cleaned.replace(",", ".")      # decimal comma -> dot
    # handle cases like 13.789.1 (PL thousands dot + decimal dot)
    parts = cleaned.split(".")
    if len(parts) > 2:
        cleaned = "".join(parts[:-1]) + "." + parts[-1]
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_components_text(raw_text: str) -> list:
    """Parses pasted component table text into a list of dicts."""
    lines = [line for line in raw_text.strip().splitlines() if line.strip()]
    results = []

    for line in lines:
        parts = line.split("\t")
        if len(parts) < 6:
            continue  # skip incomplete lines

        typ = parts[0].strip()

        # skip header row
        if typ.lower() in HEADER_KEYWORDS:
            continue

        results.append({
            "type": typ,
            "brand": parts[1].strip(),
            "model": parts[2].strip(),
            "added": parts[3].strip(),
            "removed": parts[4].strip(),
            "distance_km": parse_distance(parts[5]),
        })

    return results
