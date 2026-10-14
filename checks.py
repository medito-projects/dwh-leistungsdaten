"""Prüft die Datenqualität im Data Warehouse.

Jede Prüfung gibt OK oder FEHLER aus. So sieht man, ob ein Bericht auf
vollständigen und stimmigen Daten beruht.
"""
import sqlite3
import sys

from etl import DB, ROH, extract, transform


def pruefe(conn):
    cur = conn.cursor()
    ergebnisse = []

    # 1. Summe im Warehouse = Summe der bereinigten Rohdaten (Abgleich Quelle/Ziel)
    sauber, _ = transform(extract(ROH))
    soll = round(sum(z["betrag_eur"] for z in sauber), 2)
    ist = round(cur.execute("SELECT SUM(betrag_eur) FROM fact_leistung").fetchone()[0], 2)
    ergebnisse.append(("Summe Quelle = Summe Warehouse", soll == ist, f"{soll} / {ist}"))

    # 2. Anzahl Zeilen stimmt
    anzahl = cur.execute("SELECT COUNT(*) FROM fact_leistung").fetchone()[0]
    ergebnisse.append(("Anzahl Zeilen stimmt", anzahl == len(sauber), f"{len(sauber)} / {anzahl}"))

    # 3. Keine doppelten Belege
    dup = cur.execute(
        "SELECT COUNT(*) FROM (SELECT beleg_id FROM fact_leistung GROUP BY beleg_id HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    ergebnisse.append(("Keine doppelten Belege", dup == 0, str(dup)))

    # 4. Keine Fakten ohne passende Dimension
    for dim, key in (("dim_zeit", "zeit_key"), ("dim_region", "region_key"),
                     ("dim_leistungsart", "leistungsart_key")):
        waisen = cur.execute(
            f"SELECT COUNT(*) FROM fact_leistung f LEFT JOIN {dim} d ON f.{key} = d.{key} "
            f"WHERE d.{key} IS NULL"
        ).fetchone()[0]
        ergebnisse.append((f"Alle Fakten haben Eintrag in {dim}", waisen == 0, str(waisen)))

    # 5. Alle Beträge positiv
    neg = cur.execute("SELECT COUNT(*) FROM fact_leistung WHERE betrag_eur <= 0").fetchone()[0]
    ergebnisse.append(("Alle Beträge positiv", neg == 0, str(neg)))

    # 6. Regionen einheitlich geschrieben
    regionen = [r[0] for r in cur.execute("SELECT region FROM dim_region")]
    ergebnisse.append(("Regionen einheitlich", len(regionen) == len({r.title() for r in regionen}),
                       ", ".join(sorted(regionen))))
    return ergebnisse


def main():
    conn = sqlite3.connect(DB)
    fehler = 0
    for name, ok, detail in pruefe(conn):
        print(f"{'OK    ' if ok else 'FEHLER'}  {name}  ({detail})")
        fehler += 0 if ok else 1
    conn.close()
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
