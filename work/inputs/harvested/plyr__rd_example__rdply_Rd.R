# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: rdply.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 4

suppressPackageStartupMessages(library(plyr))
rdply(20, mean(runif(100)))
rdply(20, each(mean, var)(runif(100)))
rdply(20, data.frame(x = runif(2)))