# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: stats-kurtosis.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 9

suppressPackageStartupMessages(library(timeDate))
r = rnorm(100)
mean(r)
var(r)
   
## kurtosis
kurtosis(r)

kurtosis(data.frame(r = r, r2 = r^2))