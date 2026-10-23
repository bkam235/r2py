# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: funs.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 8

suppressPackageStartupMessages(library(dplyr))
funs("mean", mean(., na.rm = TRUE))
# ->
list(mean = mean, mean = ~ mean(.x, na.rm = TRUE))

funs(m1 = mean, m2 = "mean", m3 = mean(., na.rm = TRUE))
# ->
list(m1 = mean, m2 = "mean", m3 = ~ mean(.x, na.rm = TRUE))