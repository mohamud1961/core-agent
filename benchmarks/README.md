# Core vs Codex on Terminal-Bench 2.1

**Question:** with the harness as the only difference in price, what does a solved task cost?

## Setup

- **Tasks:** the 24 Terminal-Bench 2.1 tasks that both agents ran, graded by the benchmark's hidden tests.
- **Codex:** the public Harbor leaderboard entry "Codex / GPT-5.6 Luna, effort max" (TB2.1 leaderboard
  `60330f75`, row `e5f3feda`), 5 runs per task. Its token counts come from the published trajectories.
- **Core Agent:** gpt-6-luna, every valid run on these tasks from Core's experiment boards (runs that crashed before
  the agent started are excluded). Token counts come from Harbor's `result.json` for each run.
- **Price:** every run is priced at gpt-6-luna list prices, $0.10 / $0.01 / $0.50 per million uncached input /
  cached input / output tokens. GPT-5.6 Luna itself is listed at $1.00 / $0.10 / $6.00, so at real prices the gap
  is about 10 times larger; pricing both the same isolates the harness.

## Result

| | Core Agent | Codex |
|---|---|---|
| Runs | 325 | 120 |
| Passes | 238 (73%) | 91 (76%) |
| Cost per run | $0.0096 | $0.0334 |
| **Cost per solved task** | **$0.0132** | $0.0441 |
| Tokens per run (median) | 95,372 | 502,779 |

Core spends 3.3× less per solved task and reads 5.3× fewer tokens per run.

## Per task

| Task | Core passes | Core $/run | Core median min | Codex passes | Codex $/run | Codex median min |
|---|---|---|---|---|---|---|
| build-cython-ext | 2/2 | $0.024 | 6.9 | 5/5 | $0.050 | 4.9 |
| chess-best-move | 17/31 | $0.005 | 2.8 | 2/5 | $0.011 | 1.0 |
| cobol-modernization | 2/2 | $0.016 | 3.9 | 5/5 | $0.024 | 3.6 |
| code-from-image | 7/7 | $0.003 | 0.4 | 5/5 | $0.003 | 0.3 |
| configure-git-webserver | 4/14 | $0.017 | 4.3 | 4/5 | $0.028 | 3.3 |
| filter-js-from-html | 0/1 | $0.020 | 5.1 | 0/5 | $0.048 | 5.7 |
| fix-git | 16/16 | $0.004 | 1.2 | 5/5 | $0.009 | 2.1 |
| gcode-to-text | 1/30 | $0.028 | 4.7 | 0/5 | $0.094 | 7.0 |
| git-leak-recovery | 14/14 | $0.004 | 1.1 | 5/5 | $0.005 | 0.7 |
| git-multibranch | 13/14 | $0.009 | 2.7 | 5/5 | $0.017 | 2.1 |
| make-doom-for-mips | 0/1 | $0.054 | 12.8 | 0/5 | $0.288 | 11.7 |
| merge-diff-arc-agi-task | 24/24 | $0.006 | 2.0 | 5/5 | $0.013 | 1.4 |
| model-extraction-relu-logits | 9/23 | $0.020 | 4.7 | 3/5 | $0.024 | 3.4 |
| modernize-scientific-stack | 2/2 | $0.002 | 0.6 | 5/5 | $0.004 | 0.6 |
| multi-source-data-merger | 33/33 | $0.002 | 0.8 | 5/5 | $0.006 | 0.9 |
| nginx-request-logging | 14/14 | $0.003 | 1.0 | 5/5 | $0.006 | 0.8 |
| pytorch-model-recovery | 22/22 | $0.005 | 1.5 | 5/5 | $0.016 | 2.3 |
| qemu-alpine-ssh | 0/2 | $0.011 | 5.3 | 0/5 | $0.043 | 7.9 |
| sanitize-git-repo | 1/14 | $0.021 | 6.9 | 3/5 | $0.041 | 4.5 |
| sparql-university | 25/27 | $0.004 | 1.1 | 5/5 | $0.007 | 0.9 |
| sqlite-with-gcov | 2/2 | $0.005 | 3.0 | 4/5 | $0.017 | 2.1 |
| tune-mjcf | 26/26 | $0.005 | 3.8 | 5/5 | $0.019 | 4.7 |
| vulnerable-secret | 2/2 | $0.002 | 1.1 | 5/5 | $0.005 | 0.5 |
| write-compressor | 2/2 | $0.014 | 3.5 | 5/5 | $0.026 | 3.3 |

## Limits

- Different models: Codex ran GPT-5.6 Luna, Core runs gpt-6-luna. There is no public Codex gpt-6-luna row on
  Terminal-Bench 2.1.
- Core's runs come from many experiment builds rather than one release, and several tasks have only 2 runs.
- Time is not part of the claim: per task, Codex finishes faster on most tasks.

## Reproduce

```sh
python benchmarks/compare_codex.py core.json codex.json > benchmarks/tb21_vs_codex.json
```

The input formats and the commands that fetch Codex's public runs are in
[compare_codex.py](compare_codex.py). Results: [tb21_vs_codex.json](tb21_vs_codex.json).
