# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: win_over.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 8

suppressPackageStartupMessages(library(dbplyr))
con <- simulate_dbi()

win_over(sql("avg(x)"), con = con)
win_over(sql("avg(x)"), "y", con = con)
win_over(sql("avg(x)"), order = "y", con = con)
win_over(sql("avg(x)"), order = c("x", "y"), con = con)
win_over(sql("avg(x)"), frame = c(-Inf, 0), order = "y", con = con)