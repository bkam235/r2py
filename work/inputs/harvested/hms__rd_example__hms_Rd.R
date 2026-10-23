# r2py crawler metadata
# package: hms
# source_type: rd_example
# topic: hms.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hms\help
# lines: 16

suppressPackageStartupMessages(library(hms))
hms(56, 34, 12)
hms()

new_hms(as.numeric(1:3))
# Supports numeric only!
try(new_hms(1:3))

as_hms(1)
as_hms("12:34:56")
as_hms(Sys.time())
as.POSIXct(hms(1))
data.frame(a = hms(1))
d <- data.frame(hours = 1:3)
d$hours <- hms(hours = d$hours)
d