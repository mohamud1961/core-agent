# Core vs Codex on Terminal-Bench 2.1

## Head to head: same model, same tasks, same prices

Core Agent and Codex 0.159, both on GPT Luna (gpt-6-luna) at max effort, run side by side on the same machine
over 25 Terminal-Bench 2.1 tasks, graded by the benchmark's hidden tests.

| | Core Agent | Codex 0.159 |
|---|---|---|
| Tasks passed | **25/25** | 25/25 |
| **Total cost** | **$0.416** | $0.563 |
| Median time per task | **167 s** | 185 s |
| Total agent time | 6,887 s | 6,782 s |

**Core is 26% cheaper with the same passes.** Core was cheaper on 19 tasks, Codex on 4, and 2 were level. Core
also took fewer steps on most tasks, for example compile-compcert in 39 steps against 92.

Costs here use $0.225 / $0.01 / $0.50 per million uncached input / cached input / output tokens for both agents.
At gpt-6-luna list prices ($0.10 input) the totals are $0.318 against $0.444, so Core is 28% cheaper.

### Per task (list prices)

| Task | Core $ | Codex $ | Core s | Codex s | Core steps | Codex steps |
|---|---|---|---|---|---|---|
| adaptive-rejection-sampler | 0.040 | 0.043 | 728 | 676 | 20 | 25 |
| build-pov-ray | 0.026 | 0.036 | 391 | 362 | 38 | 45 |
| cancel-async-tasks | 0.003 | 0.004 | 66 | 57 | 5 | 9 |
| compile-compcert | 0.034 | 0.083 | 1636 | 1476 | 39 | 92 |
| constraints-scheduling | 0.003 | 0.004 | 62 | 57 | 5 | 9 |
| crack-7z-hash | 0.008 | 0.020 | 361 | 315 | 17 | 37 |
| distribution-search | 0.006 | 0.009 | 111 | 152 | 7 | 12 |
| feal-differential-cryptanalysis | 0.009 | 0.016 | 192 | 295 | 8 | 16 |
| feal-linear-cryptanalysis | 0.012 | 0.044 | 202 | 799 | 15 | 30 |
| financial-document-processor | 0.022 | 0.015 | 213 | 114 | 16 | 16 |
| fix-git | 0.004 | 0.005 | 90 | 73 | 9 | 15 |
| git-leak-recovery | 0.004 | 0.019 | 89 | 303 | 6 | 20 |
| git-multibranch | 0.017 | 0.020 | 287 | 307 | 17 | 17 |
| headless-terminal | 0.030 | 0.011 | 452 | 185 | 23 | 11 |
| log-summary-date-ranges | 0.002 | 0.003 | 45 | 32 | 5 | 9 |
| merge-diff-arc-agi-task | 0.011 | 0.014 | 239 | 194 | 20 | 23 |
| multi-source-data-merger | 0.004 | 0.005 | 91 | 75 | 5 | 9 |
| nginx-request-logging | 0.009 | 0.007 | 157 | 101 | 10 | 12 |
| openssl-selfsigned-cert | 0.004 | 0.005 | 74 | 63 | 6 | 9 |
| overfull-hbox | 0.031 | 0.036 | 497 | 429 | 23 | 37 |
| pytorch-model-recovery | 0.008 | 0.015 | 167 | 242 | 7 | 15 |
| regex-log | 0.007 | 0.005 | 132 | 64 | 5 | 8 |
| sparql-university | 0.008 | 0.007 | 134 | 94 | 6 | 11 |
| sqlite-db-truncate | 0.006 | 0.009 | 102 | 110 | 6 | 11 |
| tune-mjcf | 0.012 | 0.010 | 369 | 205 | 19 | 16 |

### How it was run

- **Tasks:** 25 Terminal-Bench 2.1 tasks that Core passes most of the time, one run each per agent.
- **Core Agent:** the current build (cache-stable context, multi-edit, bundled Python), 6 workers.
- **Codex:** version 0.159.0 at effort max, the version on the public leaderboard, through a metered proxy to the
  same Luna deployment, 6 workers.
- **Rate limits:** with both agents running, Azure rate-limited some requests. Codex aborted 3 runs, which were
  rerun, and the reruns are counted. Core retried through it on 2 runs and passed both.
- **Script:** [head_to_head.py](head_to_head.py), run on the machine that holds the trials.

## Earlier comparison: Codex's public leaderboard run

**Question:** with the harness as the only difference in price, what does a solved task cost?

### Setup

- **Tasks:** the 24 Terminal-Bench 2.1 tasks that both agents ran, graded by the benchmark's hidden tests.
- **Codex:** the public Harbor leaderboard entry "Codex / GPT-5.6 Luna, effort max" (TB2.1 leaderboard
  `60330f75`, row `e5f3feda`), 5 runs per task. Its token counts come from the published trajectories.
- **Core Agent:** gpt-6-luna, every valid run on these tasks from Core's experiment boards (runs that crashed before
  the agent started are excluded). Token counts come from Harbor's `result.json` for each run.
- **Price:** every run is priced at gpt-6-luna list prices, $0.10 / $0.01 / $0.50 per million uncached input /
  cached input / output tokens. GPT-5.6 Luna itself is listed at $1.00 / $0.10 / $6.00, so at real prices the gap
  is about 10 times larger; pricing both the same isolates the harness.

### Result

| | Core Agent | Codex |
|---|---|---|
| Runs | 325 | 120 |
| Passes | 238 (73%) | 91 (76%) |
| Cost per run | $0.0096 | $0.0334 |
| **Cost per solved task** | **$0.0132** | $0.0441 |
| Tokens per run (median) | 95,372 | 502,779 |

Core spends 3.3× less per solved task and reads 5.3× fewer tokens per run.

### Per task

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

### Limits

- Different models: Codex ran GPT-5.6 Luna, Core runs gpt-6-luna. There is no public Codex gpt-6-luna row on
  Terminal-Bench 2.1.
- Core's runs come from many experiment builds rather than one release, and several tasks have only 2 runs.
- Time is not part of the claim: per task, Codex finishes faster on most tasks.

### Reproduce

```sh
python benchmarks/compare_codex.py core.json codex.json > benchmarks/tb21_vs_codex.json
```

The input formats and the commands that fetch Codex's public runs are in
[compare_codex.py](compare_codex.py). Results: [tb21_vs_codex.json](tb21_vs_codex.json).
