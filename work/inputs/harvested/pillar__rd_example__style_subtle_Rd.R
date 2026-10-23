# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: style_subtle.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 15

suppressPackageStartupMessages(library(pillar))
style_num(
  c("123", "456"),
  negative = c(TRUE, FALSE)
)
style_num(
  c("123", "456"),
  negative = c(TRUE, FALSE),
  significant = c(FALSE, FALSE)
)
style_subtle("text")
style_subtle_num(0.01 * 1:3, c(TRUE, FALSE, TRUE))
style_bold("Petal.Width")
style_na("NA")
style_neg("123")