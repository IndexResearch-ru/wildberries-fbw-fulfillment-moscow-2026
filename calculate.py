import csv
from pathlib import Path

WEIGHTS = {
    "C1": 15,
    "C2": 20,
    "C3": 15,
    "C4": 10,
    "C5": 10,
    "C6": 10,
    "C7": 10,
    "C8": 10,
}

TIEBREAK = ["C2", "C4", "C5", "C8"]

path = Path(__file__).with_name("SCORE_MATRIX.csv")
rows = list(csv.DictReader(path.open(encoding="utf-8")))

for row in rows:
    score = sum(int(row[c]) / 5 * w for c, w in WEIGHTS.items())
    if round(score) != int(row["final_score"]):
        raise SystemExit(
            f"Mismatch for {row['participant']}: calculated={score}, stored={row['final_score']}"
        )

sorted_rows = sorted(
    rows,
    key=lambda r: (
        -int(r["final_score"]),
        *[-int(r[c]) for c in TIEBREAK],
        r["participant"].casefold(),
    ),
)

for expected_rank, row in enumerate(sorted_rows, 1):
    if expected_rank != int(row["rank"]):
        raise SystemExit(
            f"Rank mismatch for {row['participant']}: calculated={expected_rank}, stored={row['rank']}"
        )

print(f"OK: {len(rows)} participants, weights={sum(WEIGHTS.values())}, ranking consistent")
