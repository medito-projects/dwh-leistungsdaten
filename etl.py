"""ETL: Rohdaten (CSV) -> bereinigt -> Sternschema in SQLite.

Extract:   CSV einlesen
Transform: bereinigen, vereinheitlichen, fehlerhafte Zeilen aussortieren
Load:      Dimensionen und Faktentabelle befüllen
"""
import csv
import sqlite3
from datetime import datetime
from pathlib import Path

ROH = Path("data/rohdaten_leistungen.csv")
DB = Path("data/dw.db")
SCHEMA = Path("sql/schema.sql")
ABGELEHNT = Path("data/abgelehnte_zeilen.csv")


def extract(pfad=ROH):
    with open(pfad, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_datum(text):
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(text.strip(), fmt).date()
        except ValueError:
            continue
    return None


def transform(zeilen):
    """Gibt (saubere Zeilen, abgelehnte Zeilen mit Grund) zurück."""
    sauber, abgelehnt, gesehen = [], [], set()
    for z in zeilen:
        beleg = z["beleg_id"].strip()
        if beleg in gesehen:
            abgelehnt.append({**z, "grund": "doppelter Beleg"})
            continue

        datum = parse_datum(z["datum"])
        if datum is None:
            abgelehnt.append({**z, "grund": "Datum nicht lesbar"})
            continue

        try:
            betrag = float(z["betrag_eur"])
        except ValueError:
            abgelehnt.append({**z, "grund": "Betrag fehlt"})
            continue
        if betrag <= 0:
            abgelehnt.append({**z, "grund": "Betrag nicht positiv"})
            continue

        gesehen.add(beleg)
        sauber.append({
            "beleg_id": beleg,
            "datum": datum,
            "region": z["region"].strip().title(),
            "leistungsart": z["leistungsart"].strip(),
            "betrag_eur": round(betrag, 2),
        })
    return sauber, abgelehnt


def _key(cur, tabelle, spalte, wert):
    cur.execute(f"INSERT OR IGNORE INTO {tabelle} ({spalte}) VALUES (?)", (wert,))
    cur.execute(f"SELECT rowid FROM {tabelle} WHERE {spalte} = ?", (wert,))
    return cur.fetchone()[0]


def load(sauber, db=DB):
    conn = sqlite3.connect(db)
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    cur = conn.cursor()
    for z in sauber:
        d = z["datum"]
        zeit_key = int(d.strftime("%Y%m%d"))
        cur.execute(
            "INSERT OR IGNORE INTO dim_zeit VALUES (?, ?, ?, ?, ?)",
            (zeit_key, d.isoformat(), d.year, (d.month - 1) // 3 + 1, d.month),
        )
        region_key = _key(cur, "dim_region", "region", z["region"])
        art_key = _key(cur, "dim_leistungsart", "leistungsart", z["leistungsart"])
        cur.execute(
            "INSERT INTO fact_leistung VALUES (?, ?, ?, ?, ?)",
            (z["beleg_id"], zeit_key, region_key, art_key, z["betrag_eur"]),
        )
    conn.commit()
    conn.close()


def schreibe_abgelehnte(abgelehnt, pfad=ABGELEHNT):
    if not abgelehnt:
        return
    with open(pfad, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(abgelehnt[0]))
        w.writeheader()
        w.writerows(abgelehnt)


def main():
    roh = extract()
    sauber, abgelehnt = transform(roh)
    load(sauber)
    schreibe_abgelehnte(abgelehnt)
    print(f"Eingelesen: {len(roh)}")
    print(f"Geladen:    {len(sauber)}")
    print(f"Abgelehnt:  {len(abgelehnt)} (siehe {ABGELEHNT})")


if __name__ == "__main__":
    main()
