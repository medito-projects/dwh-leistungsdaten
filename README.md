# Mini-Data-Warehouse: Leistungsausgaben


In diesem Projekt probiere ich aus, wie man Daten mit Python aufbereitet, in einer Datenbank speichert und mit SQL auswertet.

Als Beispiel verwende ich selbst erzeugte Daten zu Krankenkassenleistungen. Die Daten sind nicht echt und enthalten absichtlich einige Fehler, damit ich auch die Datenbereinigung testen kann.

## Was macht das Projekt?

- `generate_data.py` erstellt eine CSV-Datei mit Beispieldaten.
- `etl.py` liest die Daten ein, entfernt fehlerhafte Einträge und speichert die übrigen Daten in SQLite.
- `checks.py` prüft, ob die Daten richtig übernommen wurden.
- `report.py` führt verschiedene SQL-Abfragen aus und zeigt die Ergebnisse an.

Die Datenbank besteht aus einer Faktentabelle und drei Dimensionstabellen für Zeit, Region und Leistungsart.

## Verwendete Technologien

Python, SQL, SQLite und pytest

## Projekt starten

Python 3 wird benötigt. Für die Tests muss pytest installiert sein.

Die Befehle im Projektordner nacheinander ausführen:

```bash
python generate_data.py
python etl.py
python checks.py
python report.py
```

Tests ausführen:

```bash
python -m pytest tests -v
```

## Ergebnisse

Mit den SQL-Abfragen kann ich zum Beispiel die Kosten nach Leistungsart, Region und Zeitraum anzeigen lassen.

## Was noch fehlt

Aktuell läuft alles über das Terminal. Später würde ich gerne ein Dashboard ergänzen mit Power BI.


## Was noch fehlen würde

- Echte Quellsysteme
- Eine Dimension für Versicherte (mit username oder sowas)
- Schrittweises Laden neuer Daten statt jedes Mal alles neu aufzubauen
- Ein Dashboard ( Power BI oder SAP Analytics Cloud) auf den Abfragen
