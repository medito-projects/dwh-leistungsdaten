"""Erzeugt erfundene Rohdaten zu Leistungsausgaben (keine echten Versichertendaten).

Die Daten sind absichtlich unsauber (doppelte Zeilen, fehlende Beträge,
unterschiedliche Datumsformate, uneinheitliche Schreibweisen), damit die
Aufbereitung im ETL-Schritt etwas zu tun hat.
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)

REGIONEN = ["Dortmund", "Münster", "Bielefeld", "Essen", "Köln"]
LEISTUNGSARTEN = {
    "Krankenhaus": (800, 9000),
    "Arzneimittel": (10, 600),
    "Arztbehandlung": (25, 400),
    "Zahnbehandlung": (30, 900),
    "Heilmittel": (20, 250),
}
ANZAHL = 2000
START = date(2024, 1, 1)


def schreibweise(region):
    # absichtlich uneinheitlich
    return random.choice([region, region.upper(), region.lower(), f" {region} "])


def datum_text(d):
    return random.choice([d.isoformat(), d.strftime("%d.%m.%Y")])


def main():
    zeilen = []
    for i in range(1, ANZAHL + 1):
        art = random.choice(list(LEISTUNGSARTEN))
        low, high = LEISTUNGSARTEN[art]
        betrag = round(random.uniform(low, high), 2)
        d = START + timedelta(days=random.randint(0, 729))
        zeilen.append({
            "beleg_id": f"B{i:05d}",
            "datum": datum_text(d),
            "region": schreibweise(random.choice(REGIONEN)),
            "leistungsart": art,
            "betrag_eur": f"{betrag:.2f}",
        })

    # Fehler einbauen
    for z in random.sample(zeilen, 15):
        z["betrag_eur"] = ""
    for z in random.sample(zeilen, 5):
        z["betrag_eur"] = "-" + z["betrag_eur"].lstrip("-")
    for z in random.sample(zeilen, 20):
        zeilen.append(dict(z))  # doppelte Zeile

    random.shuffle(zeilen)
    with open("data/rohdaten_leistungen.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(zeilen[0]))
        w.writeheader()
        w.writerows(zeilen)
    print(f"{len(zeilen)} Zeilen geschrieben")


if __name__ == "__main__":
    main()
