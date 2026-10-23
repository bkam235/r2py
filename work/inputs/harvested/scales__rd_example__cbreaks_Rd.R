# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: cbreaks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 20

suppressPackageStartupMessages(library(scales))
cbreaks(c(0, 100))
cbreaks(c(0, 100), breaks_pretty(3))
cbreaks(c(0, 100), breaks_pretty(10))
cbreaks(c(1, 100), log_breaks())
cbreaks(c(1, 1e4), log_breaks())

cbreaks(c(0, 100), labels = math_format())
cbreaks(c(0, 1), labels = percent_format())
cbreaks(c(0, 1e6), labels = comma_format())
cbreaks(c(0, 1e6), labels = dollar_format())
cbreaks(c(0, 30), labels = dollar_format())

# You can also specify them manually:
cbreaks(c(0, 100), breaks = c(15, 20, 80))
cbreaks(c(0, 100), breaks = c(15, 20, 80), labels = c(1.5, 2.0, 8.0))
cbreaks(c(0, 100),
  breaks = c(15, 20, 80),
  labels = expression(alpha, beta, gamma)
)