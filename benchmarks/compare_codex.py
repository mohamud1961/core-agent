"""Core vs Codex on Terminal-Bench 2.1, on the tasks both ran, at one price table.

Inputs (aggregates only, no task text):
  core.json   rows {task, reward, agent_s, prompt, cached, completion} from Core's Harbor result.json files
  codex.json  the same fields for the public Harbor leaderboard row "Codex / GPT-5.6 Luna, effort max"
              (TB2.1 leaderboard 60330f75, row e5f3feda), fetched with
              `harbor hub leaderboard row trial list e5f3feda-4629-46ba-963f-300dcf7c2a4c -q -l 1000`,
              `harbor hub trial show ID --json` and `harbor hub trial download ID --trajectory`.

Every run is priced at gpt-6-luna list prices ($0.10 / $0.01 / $0.50 per million uncached input / cached input /
output tokens), so the comparison measures the harness, not the model's price.

Usage: python benchmarks/compare_codex.py core.json codex.json > benchmarks/tb21_vs_codex.json
"""

import json
import statistics as st
import sys

PRICE = (0.10, 0.01, 0.50)


def cost(r):
    p, c, o = (r.get(k) or 0 for k in ("prompt", "cached", "completion"))
    return ((p - c) * PRICE[0] + c * PRICE[1] + o * PRICE[2]) / 1e6


def summary(rows):
    passes = [r for r in rows if r["reward"] == 1]
    total = sum(map(cost, rows))
    return {"runs": len(rows), "passes": len(passes), "pass_rate": round(len(passes) / len(rows), 3),
            "usd_per_run": round(total / len(rows), 4), "usd_per_pass": round(total / len(passes), 4),
            "median_tokens_per_run": int(st.median(r["prompt"] + r["completion"] for r in rows))}


def main(core_path, codex_path):
    core = [r for r in json.load(open(core_path)) if r.get("prompt")]
    codex = [r for r in json.load(open(codex_path)) if r.get("prompt")]
    tasks = sorted({r["task"] for r in core} & {r["task"] for r in codex})
    core = [r for r in core if r["task"] in tasks]
    codex = [r for r in codex if r["task"] in tasks]
    per_task = {}
    for t in tasks:
        a = [r for r in core if r["task"] == t]
        b = [r for r in codex if r["task"] == t]
        per_task[t] = {name: {"runs": len(x), "passes": sum(r["reward"] == 1 for r in x),
                              "usd_per_run": round(sum(map(cost, x)) / len(x), 4),
                              "median_minutes": round(st.median(r["agent_s"] for r in x) / 60, 1)}
                       for name, x in (("core", a), ("codex", b))}
    json.dump({"price_per_million": dict(zip(("uncached_input", "cached_input", "output"), PRICE)),
               "tasks": len(tasks), "core": summary(core), "codex": summary(codex), "per_task": per_task},
              sys.stdout, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
