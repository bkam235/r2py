# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_formula.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 35

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
dat <- data.frame(x = c(1, 5, 3, 2, 4, 6))

ss <- gs4_create("gs4-formula-demo", sheets = dat)
ss

summaries <- tibble::tribble(
  ~desc, ~summaries,
  "max", "=max(A:A)",
  "sum", "=sum(A:A)",
  "min", "=min(A:A)",
  "sparkline", "=SPARKLINE(A:A, {\"color\", \"blue\"})"
)

# explicitly declare a column as `googlesheets4_formula`
summaries$summaries <- gs4_formula(summaries$summaries)
summaries

range_write(ss, data = summaries, range = "C1", reformat = FALSE)

miscellany <- tibble::tribble(
  ~desc, ~example,
  "hyperlink", "=HYPERLINK(\"http://www.google.com/\",\"Google\")",
  "image", "=IMAGE(\"https://www.google.com/images/srpr/logo3w.png\")"
)
miscellany$example <- gs4_formula(miscellany$example)
miscellany

sheet_write(miscellany, ss = ss)

# clean up
gs4_find("gs4-formula-demo") %>%
  googledrive::drive_trash()
}) # examplesIf