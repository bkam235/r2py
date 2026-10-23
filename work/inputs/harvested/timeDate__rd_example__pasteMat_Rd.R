# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: pasteMat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 23

suppressPackageStartupMessages(library(timeDate))
a <- c("a",  NA, "b", NA, "c")
b <- c("x", "y",  NA, NA, "z")

## turns NAs into the string "NA"
paste(a, b)

## keeps NAs in the result
pasteMat(a, b)
pasteMat(cbind(a, b)) # same

dts <- c("1989-09-28", NA, "2004-08-30", "1990-02-09")
tms <- c(  "23:12:55",   "10:34:02",   NA,   "11:18:23")

paste(dts, tms)
## this throws error (since NAs are converted to the string NA):
##   timeDate(paste(dts, tms), FinCenter = "Europe/Zurich")

## these work
td1 <- timeDate(pasteMat(cbind(dts, tms)), FinCenter = "Europe/Zurich")
td2 <- timeDate(pasteMat(dts, tms), FinCenter = "Europe/Zurich")       
identical(td1, td2)                                                    
td1