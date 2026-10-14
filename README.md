# Mini-Data-Warehouse: Leistungsausgaben

Kleines Lernprojekt zu Data-Warehouse-Grundlagen. Es zeigt in einem überschaubaren Beispiel, wie Rohdaten bereinigt, in ein Sternschema geladen, geprüft und ausgewertet werden.

Die Daten sind **erfunden** (Zufallsdaten, kein Bezug zu echten Versicherten oder einer Krankenkasse). Ich habe das Projekt gebaut, um ETL, Sternschema und Datenqualitätsprüfungen praktisch auszuprobieren.

## Was passiert hier

1. `generate_data.py` erzeugt eine CSV mit Leistungsausgaben (ca. 2000 Zeilen). Die Daten sind absichtlich unsauber: doppelte Belege, fehlende oder negative Beträge, zwei Datumsformate, uneinheitliche Schreibweisen bei Regionen.
2. `etl.py` macht den ETL-Ablauf:
   - **Extract:** CSV einlesen
   - **Transform:** Daten bereinigen und vereinheitlichen, fehlerhafte Zeilen mit Grund aussortieren
   - **Load:** Dimensionen und Faktentabelle in einer SQLite-Datenbank befüllen
3. `checks.py` prüft die Datenqualität im Warehouse, zum Beispiel ob die Summe im Warehouse zur bereinigten Quelle passt, ob es doppelte Belege gibt und ob jede Zeile der Faktentabelle zu einer Dimension passt.
4. `report.py` führt die Abfragen aus `sql/berichte.sql` aus.

## Das Sternschema

In der Mitte liegt die Faktentabelle `fact_leistung` mit dem Betrag. Drumherum liegen drei Dimensionen:

```
dim_zeit ----\
dim_region ---- fact_leistung (betrag_eur)
dim_leistungsart --/
```

Damit lassen sich Fragen beantworten wie: Wie hoch waren die Kosten pro Leistungsart und Quartal? Das Schema steht in `sql/schema.sql`.

## Ausführen

Benötigt wird nur Python 3, ohne zusätzliche Pakete. Für die Tests wird pytest gebraucht.

```
python generate_data.py
python etl.py
python checks.py
python report.py
python -m pytest tests
```

## Ergebnis

Von 2020 Rohzeilen werden 1980 geladen. 40 Zeilen werden mit Begründung in `data/abgelehnte_zeilen.csv` abgelegt: 20 doppelte Belege, 15 fehlende Beträge, 5 negative Beträge.

## Was noch fehlen würde

- Echte Quellsysteme statt einer CSV
- Eine Dimension für Versicherte (mit Pseudonymen)
- Schrittweises Laden neuer Daten statt jedes Mal alles neu aufzubauen
- Ein Dashboard (zum Beispiel Power BI oder SAP Analytics Cloud) auf den Abfragen
