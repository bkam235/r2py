# r2py crawler metadata
# package: lava
# source_type: vignette
# topic: influencefunction_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\doc\influencefunction.R
# lines: 9

suppressPackageStartupMessages(library(lava))
m <- lvm() |>
  regression(y1 ~ x1 + a + w) |>
  regression(y2 ~ x2 + a + w) |>
  regression(y3 ~ x3 + a + w) |>
  regression(y4 ~ x4 + a + w) |>
  regression(a ~ w) |>
  distribution(~ y1 + y2 + y3 + y4 + a, value = binomial.lvm()) |>
  distribution(~id, value = Sequence.lvm(integer = TRUE))