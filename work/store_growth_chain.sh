#!/usr/bin/env bash
# Start C2 once C1 (replay of rewrite_w3 vs rewrite_w3_ondemand) has written all 80 rows.
cd /c/Users/bened/Desktop/r2py_v0.3
until [ "$(wc -l < work/replay_ondemand/results.jsonl 2>/dev/null || echo 0)" -ge 80 ] && grep -q "runs over" work/replay_ondemand/run.log; do sleep 120; done
mkdir -p work/store_growth
python scripts/store_growth.py run --n 64 --workers 4 > work/store_growth/run.log 2>&1
