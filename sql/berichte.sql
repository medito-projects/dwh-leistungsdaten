-- name: Kosten pro Leistungsart und Jahr
SELECT z.jahr, l.leistungsart,
       COUNT(*)                 AS anzahl_faelle,
       ROUND(SUM(f.betrag_eur), 2) AS summe_eur
FROM fact_leistung f
JOIN dim_zeit z ON z.zeit_key = f.zeit_key
JOIN dim_leistungsart l ON l.leistungsart_key = f.leistungsart_key
GROUP BY z.jahr, l.leistungsart
ORDER BY z.jahr, summe_eur DESC;

-- name: Kosten pro Region und Quartal
SELECT z.jahr, z.quartal, r.region,
       ROUND(SUM(f.betrag_eur), 2) AS summe_eur
FROM fact_leistung f
JOIN dim_zeit z ON z.zeit_key = f.zeit_key
JOIN dim_region r ON r.region_key = f.region_key
GROUP BY z.jahr, z.quartal, r.region
ORDER BY z.jahr, z.quartal, summe_eur DESC;

-- name: Durchschnittlicher Betrag pro Fall und Leistungsart
SELECT l.leistungsart,
       ROUND(AVG(f.betrag_eur), 2) AS durchschnitt_eur
FROM fact_leistung f
JOIN dim_leistungsart l ON l.leistungsart_key = f.leistungsart_key
GROUP BY l.leistungsart
ORDER BY durchschnitt_eur DESC;

-- name: Anteil der Leistungsarten an den Gesamtkosten
SELECT l.leistungsart,
       ROUND(100.0 * SUM(f.betrag_eur) / (SELECT SUM(betrag_eur) FROM fact_leistung), 1) AS anteil_prozent
FROM fact_leistung f
JOIN dim_leistungsart l ON l.leistungsart_key = f.leistungsart_key
GROUP BY l.leistungsart
ORDER BY anteil_prozent DESC;
