"""CMP1: Core (arm CR) vs Codex 0.159.0, both gpt-6-luna at effort max, 25 majority-pass TB2.1 tasks, 1 rep.
Run on the run host. Aggregates only leave it.

Labels: Harbor reward only. Cost per row from token usage at the same prices for both agents
($0.225/M uncached input, $0.01/M cached, $0.50/M output) plus $0.01 a hosted search for Codex (proxy ledger
`searches`); board totals from each proxy's own ledger. Time: agent execution seconds from Harbor's result.json.

  compare.py CORE_BOARD_DIR[,CORE_BOARD_DIR...] CODEX_JOB_DIR[,CODEX_JOB_DIR...] CODEX_PROXY_LEDGER
"""
import glob
import json
import statistics as S
import sys
from datetime import datetime

PRICE = (0.225e-6, 0.01e-6, 0.5e-6)


def usd(inp, cached, out):
    return (inp - cached) * PRICE[0] + cached * PRICE[1] + out * PRICE[2]


def secs(r):
    a = r.get("agent_execution") or {}
    try:
        return (datetime.fromisoformat(a["finished_at"]) - datetime.fromisoformat(a["started_at"])).total_seconds()
    except (KeyError, TypeError, ValueError):
        return None


def core(boards):
    out = {}
    for rj in [f for b in boards.split(",") for f in glob.glob(f"{b}/runs/q5-*/row.json")]:
        board = rj.split("/runs/")[0]
        r = json.load(open(rj))
        u = r.get("usage") or {}
        res = glob.glob(f"{board}/{r['trial']}/result.json") or glob.glob(rj.rsplit("/", 1)[0] + "/*/*/result.json")
        out[r["task"]] = {"reward": r["reward"], "valid": r.get("valid", True) and r.get("exception") is None,
                          "usd": usd(u.get("input", 0), u.get("cached", 0), u.get("output", 0)),
                          "agent_s": secs(json.load(open(res[0]))) if res else r.get("agent_s"), "steps": r.get("calls")}
    return out


def codex(job):
    out = {}
    for res in [f for j in job.split(",") for f in sorted(glob.glob(f"{j}/*__*/result.json"))]:  # later jobs = reruns, override
        r = json.load(open(res))
        t = (r.get("task_name") or "").split("/")[-1]
        rew = ((r.get("verifier_result") or {}).get("rewards") or {}).get("reward")
        tr = glob.glob(res.rsplit("/", 1)[0] + "/agent/trajectory.json")
        m = json.load(open(tr[0])).get("final_metrics", {}) if tr else {}
        steps = len(json.load(open(tr[0])).get("steps", [])) if tr else None
        out[t] = {"reward": rew, "valid": r.get("exception_info") is None and rew is not None,
                  "usd": usd(m.get("total_prompt_tokens", 0), m.get("total_cached_tokens", 0),
                             m.get("total_completion_tokens", 0)),
                  "agent_s": secs(r), "steps": steps}
    return out


def main(board, job, ledger):
    c, x = core(board), codex(job)
    searches = sum(json.loads(l).get("searches") or 0 for l in open(ledger))
    ledger_usd = sum(json.loads(l).get("usd") or 0 for l in open(ledger))
    core_ledger = sum(json.loads(l).get("usd") or 0 for b in board.split(",") for l in open(f"{b}/proxy.jsonl"))
    tasks = sorted(set(c) | set(x))
    print(f"{'task':34} {'core':>5} {'codex':>5} {'core$':>7} {'codex$':>7} {'core_s':>7} {'codex_s':>7} {'c_st':>4} {'x_st':>4}")
    for t in tasks:
        a, b = c.get(t, {}), x.get(t, {})
        f = lambda v, k: ("-" if v.get(k) is None else (f"{v[k]:.3f}" if isinstance(v[k], float) and k == "usd" else
                          (f"{v[k]:.0f}" if isinstance(v[k], float) else str(v[k]))))
        print(f"{t:34} {f(a,'reward'):>5} {f(b,'reward'):>5} {f(a,'usd'):>7} {f(b,'usd'):>7} {f(a,'agent_s'):>7} "
              f"{f(b,'agent_s'):>7} {f(a,'steps'):>4} {f(b,'steps'):>4}")
    for name, d in (("Core", c), ("Codex", x)):
        v = [r for r in d.values() if r["valid"]]
        sec = [r["agent_s"] for r in v if r["agent_s"]]
        print(f"{name}: valid {len(v)}/{len(d)}  pass {sum((r['reward'] or 0) >= 1 for r in v)}  "
              f"usd(tokens) {sum(r['usd'] for r in v):.3f}  median agent_s {S.median(sec) if sec else None:.0f}  "
              f"total agent_s {sum(sec):.0f}")
    both = [t for t in tasks if c.get(t, {}).get("valid") and x.get(t, {}).get("valid")]
    print(f"paired valid tasks {len(both)}: Core pass {sum(c[t]['reward'] >= 1 for t in both)}, "
          f"Codex pass {sum(x[t]['reward'] >= 1 for t in both)}; "
          f"Core-only {[t for t in both if c[t]['reward'] >= 1 > x[t]['reward']]}; "
          f"Codex-only {[t for t in both if x[t]['reward'] >= 1 > c[t]['reward']]}")
    print(f"ledgers: Core proxy ${core_ledger:.3f}; Codex proxy ${ledger_usd:.3f} (incl. smoke) with {searches} searches")


if __name__ == "__main__":
    main(*sys.argv[1:4])
