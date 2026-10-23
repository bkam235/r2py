# r2py crawler metadata
# package: reshape2
# source_type: rd_example
# topic: melt.data.frame.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\reshape2\help
# lines: 5

suppressPackageStartupMessages(library(reshape2))
names(airquality) <- tolower(names(airquality))
melt(airquality, id=c("month", "day"))
names(ChickWeight) <- tolower(names(ChickWeight))
melt(ChickWeight, id=2:4)