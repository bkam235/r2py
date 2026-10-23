# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: ymd.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 24

suppressPackageStartupMessages(library(lubridate))
x <- c("09-01-01", "09-01-02", "09-01-03")
ymd(x)
x <- c("2009-01-01", "2009-01-02", "2009-01-03")
ymd(x)
ymd(090101, 90102)
now() > ymd(20090101)
## TRUE
dmy(010210)
mdy(010210)

yq('2014.2')

## heterogeneous formats in a single vector:
x <- c(20090101, "2009-01-02", "2009 01 03", "2009-1-4",
       "2009-1, 5", "Created on 2009 1 6", "200901 !!! 07")
ymd(x)

## What lubridate might not handle:

## Extremely weird cases when one of the separators is "" and some of the
## formats are not in double digits might not be parsed correctly:
ymd("201002-01", "201002-1", "20102-1")
dmy("0312-2010", "312-2010")