# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: in_int.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 40

suppressPackageStartupMessages(library(timeDate))
## create a time interval by rounding to the enclosing hour
ti <- timeInterval(timeDate("2024-12-20 10:20:30"), unit = "hours")
ti

## a similar interval on the following day
tib <- timeInterval(timeDate("2024-12-21 10:20:30"), unit = "hours")
tib

ti2 <- ti | tib
ti2

ti & ti2
ti | ti2

!ti
!ti2

identical(!ti, ti ^ timeInterval(left = -Inf, right = Inf))
identical(!ti2, ti2 ^ timeInterval(left = -Inf, right = Inf))

## tiInf represents the time interval (-Inf, Inf)
identical(tiInf, timeInterval(left = -Inf, right = Inf))

ti ^ ti2 # ti2 \ ti
ti2 ^ ti # ti  \ ti2

timeDate("2024-12-20 10:20:30") %in_int% ti2  # TRUE
timeDate("2024-12-20 11:20:30") %in_int% ti2  # FALSE

timeDate(c("2024-12-20 10:20:30", "2024-12-20 11:20:30")) %in_int% ti2  

## ti's are closed on the left and open on the right, hence:
ti2@left %in_int% ti2    # [1] TRUE TRUE
ti2@right %in_int% ti2   # [1] FALSE FALSE

## a timeInterval is a scalar, so the following give a single TRUE/FALSE
## indicating whether or not the first interval is contained in the second
ti %in_int% ti2
ti2 %in_int% ti