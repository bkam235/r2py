"""Manual stratified ablation harness — §12.4.1.

Reads the pinned slice manifest (work/inputs/ablation_slice.txt), translates it
twice (library frozen vs. learning on, identical seeds/max_iters), and writes
per-script A/B scores, aggregate B-A with significance check, and the regression
list to work/analysis/ablation/<ts>/.

CLI: r2py ablation
Not yet implemented. See architecture.md §12.4.1.
"""
raise NotImplementedError
