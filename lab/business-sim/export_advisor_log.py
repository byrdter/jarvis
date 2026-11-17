"""Export the reorder advisor's decision log (every purchase it made, with its reason) for video captures.

python3 export_advisor_log.py --seed 7 --day 2026-11-16
Writes out/exports/advisor-log-seed7.csv (all decisions) and advisor-log-seed7-<day>.txt (one morning).
"""
import argparse, csv
from pathlib import Path

import sim


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--day", default="2026-11-16", help="the morning to print as a readable page")
    a = ap.parse_args()
    out = Path("out/exports"); out.mkdir(parents=True, exist_ok=True)
    store = sim.Store(a.days, a.seed, Path("out/replay/advisor-log"), "advisor", write_mbox=False)
    store.run()
    names = {p["id"]: (f"{p['cat'].title()} item {p['id']}", p["cat"]) for p in store.products}
    log = store.advisor.log
    with open(out / f"advisor-log-seed{a.seed}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["day", "product_id", "product", "category", "ordered", "why"])
        for day, pid, qty, why in log:
            w.writerow([day, pid, names[pid][0], names[pid][1], qty, why])
    page = [f"Harbor & Pine reorder advisor, morning of {a.day} (seed {a.seed})", ""]
    page += [f"#{pid:<4} {names[pid][0]:<22} order {qty:>4}   {why}" for day, pid, qty, why in log if day == a.day]
    (out / f"advisor-log-seed{a.seed}-{a.day}.txt").write_text("\n".join(page) + "\n")
    print(f"{len(log)} decisions; {len(page) - 2} on {a.day}")
    print("\n".join(page))


if __name__ == "__main__":
    main()
