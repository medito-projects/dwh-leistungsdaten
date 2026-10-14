"""Führt die Abfragen aus sql/berichte.sql aus und gibt sie als Tabellen aus."""
import re
import sqlite3
from pathlib import Path

from etl import DB


def lade_abfragen(pfad="sql/berichte.sql"):
    text = Path(pfad).read_text(encoding="utf-8")
    teile = re.split(r"^-- name: (.+)$", text, flags=re.MULTILINE)
    return list(zip(teile[1::2], [t.strip() for t in teile[2::2]]))


def main():
    conn = sqlite3.connect(DB)
    for name, sql in lade_abfragen():
        cur = conn.execute(sql)
        spalten = [c[0] for c in cur.description]
        zeilen = cur.fetchall()
        print(f"\n== {name} ==")
        print(" | ".join(spalten))
        for z in zeilen[:12]:
            print(" | ".join(str(x) for x in z))
        if len(zeilen) > 12:
            print(f"... ({len(zeilen)} Zeilen)")
    conn.close()


if __name__ == "__main__":
    main()
