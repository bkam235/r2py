# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: numbers_chunk4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\numbers.Rmd
# lines: 12

suppressPackageStartupMessages(library(tibble))
#| label: numbers-5
num(-1:3, notation = "sci")
tibble(
  x4 = num(8:12 * 100 + 0.5, digits = 4),
  x1 = num(8:12 * 100 + 0.5, digits = -1),
  usd = num(8:12 * 100 + 0.5, digits = 2, label = "USD"),
  percent = num(8:12 / 100 + 0.0005, label = "%", scale = 100),
  eng = num(10^(-3:1), notation = "eng", fixed_exponent = -Inf),
  si = num(10^(-3:1) * 123, notation = "si"),
  char = char(paste(LETTERS, collapse = " "), shorten = "mid")
)