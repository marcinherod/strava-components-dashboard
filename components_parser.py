"""
Parsowanie tekstu skopiowanego ze strony "Mój sprzęt" na Stravie.

Oczekiwany format (kolumny rozdzielone tabulatorem, jak przy kopiowaniu z tabeli HTML):
Typ	Marka	Model	Dodano	Usunięte	Dystans	Działanie
Rama	Lapierre	Xelius SL 500 Carbon Disc	Od początku		13 789,1 km	Wycofaj | Usuń
"""

import re

HEADER_KEYWORDS = {"typ", "marka", "model", "dodano"}


def parse_distance(raw: str):
    """Zamienia '13 789,1 km' (format PL) na float 13789.1"""
    if not raw:
        return None
    cleaned = raw.replace("\xa0", " ").replace("km", "").strip()
    cleaned = re.sub(r"\s+", "", cleaned)  # usuń spacje (separator tysięcy)
    cleaned = cleaned.replace(",", ".")     # przecinek dziesiętny -> kropka
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_components_text(raw_text: str) -> list:
    """Parsuje wklejony tekst tabeli na listę słowników z komponentami."""
    lines = [line for line in raw_text.strip().splitlines() if line.strip()]
    results = []

    for line in lines:
        parts = line.split("\t")
        if len(parts) < 6:
            continue  # linia niepełna, pomiń

        typ = parts[0].strip()

        # pomiń wiersz nagłówka tabeli
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
