# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 7

suppressPackageStartupMessages(library(clock))
try({
jan31 <- date_build(2019, 1, 31)
dec31 <- date_build(2019, 12, 31)

date_seq(jan31, to = dec31, by = duration_months(1))
})