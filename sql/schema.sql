-- Sternschema: eine Faktentabelle, drei Dimensionen

DROP TABLE IF EXISTS fact_leistung;
DROP TABLE IF EXISTS dim_zeit;
DROP TABLE IF EXISTS dim_region;
DROP TABLE IF EXISTS dim_leistungsart;

CREATE TABLE dim_zeit (
    zeit_key    INTEGER PRIMARY KEY,   -- z. B. 20250314
    datum       TEXT NOT NULL,
    jahr        INTEGER NOT NULL,
    quartal     INTEGER NOT NULL,
    monat       INTEGER NOT NULL
);

CREATE TABLE dim_region (
    region_key  INTEGER PRIMARY KEY AUTOINCREMENT,
    region      TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_leistungsart (
    leistungsart_key INTEGER PRIMARY KEY AUTOINCREMENT,
    leistungsart     TEXT NOT NULL UNIQUE
);

CREATE TABLE fact_leistung (
    beleg_id         TEXT PRIMARY KEY,
    zeit_key         INTEGER NOT NULL REFERENCES dim_zeit(zeit_key),
    region_key       INTEGER NOT NULL REFERENCES dim_region(region_key),
    leistungsart_key INTEGER NOT NULL REFERENCES dim_leistungsart(leistungsart_key),
    betrag_eur       REAL NOT NULL CHECK (betrag_eur > 0)
);
