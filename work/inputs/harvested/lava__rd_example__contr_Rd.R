# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: contr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 13

suppressPackageStartupMessages(library(lava))
contr(2,n=5)
contr(as.list(2:4),n=5)
contr(list(1,2,4),n=5)
contr(c(2,3,4),n=5)
contr(list(c(1,3),c(2,4)),n=5)
contr(list(c(1,3),c(2,4),5))

parsedesign(c("aa","b","c"),"?","?",diff=c(FALSE,TRUE))

## All pairs comparisons:
pdiff <- function(n) lava::contr(lapply(seq(n-1), function(x) seq(x, n)))
pdiff(4)