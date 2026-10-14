import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl import parse_datum, transform  # noqa: E402


def zeile(**kw):
    basis = {"beleg_id": "B1", "datum": "2025-03-14", "region": " dortmund ",
             "leistungsart": "Heilmittel", "betrag_eur": "50.00"}
    basis.update(kw)
    return basis


def test_beide_datumsformate():
    assert parse_datum("2025-03-14") == parse_datum("14.03.2025")


def test_region_wird_vereinheitlicht():
    sauber, _ = transform([zeile(region=" DORTMUND ")])
    assert sauber[0]["region"] == "Dortmund"


def test_doppelter_beleg_wird_abgelehnt():
    sauber, abgelehnt = transform([zeile(), zeile()])
    assert len(sauber) == 1
    assert abgelehnt[0]["grund"] == "doppelter Beleg"


def test_fehlender_betrag_wird_abgelehnt():
    sauber, abgelehnt = transform([zeile(betrag_eur="")])
    assert sauber == []
    assert abgelehnt[0]["grund"] == "Betrag fehlt"


def test_negativer_betrag_wird_abgelehnt():
    _, abgelehnt = transform([zeile(betrag_eur="-10.00")])
    assert abgelehnt[0]["grund"] == "Betrag nicht positiv"
