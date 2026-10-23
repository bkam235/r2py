# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: runs.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 18

suppressPackageStartupMessages(library(vctrs))
x <- c("a", "z", "z", "c", "a", "a")

vec_identify_runs(x)
vec_run_sizes(x)
vec_unrep(x)

y <- c(1, 1, 1, 2, 2, 3)

# With multiple columns, the runs are constructed rowwise
df <- data_frame(
  x = x,
  y = y
)

vec_identify_runs(df)
vec_run_sizes(df)
vec_unrep(df)