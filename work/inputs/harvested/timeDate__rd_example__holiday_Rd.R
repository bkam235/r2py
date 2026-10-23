# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: holiday.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 63

suppressPackageStartupMessages(library(timeDate))
## holiday
# Dates for GoodFriday from 2000 until 2005:
holiday(2000:2005, "GoodFriday")                  
holiday(2000:2005, GoodFriday) # same (GoodFriday is a function)

# Good Friday and Easter
holiday(2000:2005, c("GoodFriday", "Easter"))                  
holiday(2000:2005, c(GoodFriday, Easter))                  
   
## Easter   
Easter(2000:2005)

## GoodFriday
GoodFriday(2000:2005)
Easter(2000:2005, -2) 

#### Named holidays

## single year
holiday(2025, Holiday = "Easter", names = TRUE)
holiday(2025, Holiday = Easter, names = TRUE)

## more years
holiday(2024:2025, Holiday = "Easter", names = TRUE)
holiday(2024:2025, Holiday = Easter, names = TRUE)

## more than one holiday
holiday(2024:2025, Holiday = c("Easter", "ChristmasDay"), names = TRUE)
holiday(2024:2025, Holiday = c(Easter, ChristmasDay), names = TRUE)

## holidays in a variable containing character values
ho1 <- "Easter"
holiday(2025, Holiday = ho1, names = TRUE)


## here, Easter is evaluated and holiday() doesn't see the name
ho1a <- Easter
ho3 <- c(Easter, GBEarlyMayBankHoliday)

holiday(2025, Holiday = ho1a, names = TRUE)

## if you wish/need to use a separate variable, use 'quote':
ho1b <- quote(Easter)
ho3b <- quote(c(Easter, GBEarlyMayBankHoliday))

holiday(2025, Holiday = ho1b, names = TRUE)
holiday(2025, Holiday = ho3b, names = TRUE)
holiday(2024:2025, Holiday = ho3b, names = TRUE)

## with string values there is no need to quote:
ho2 <- c("Easter", "GBEarlyMayBankHoliday")
holiday(2025, Holiday = ho2, names = TRUE)

holiday(Holiday = c(Easter, GBEarlyMayBankHoliday), names = TRUE)

holiday(2024:2025, Holiday = ho2, names = TRUE)
holiday(2024:2025, Holiday = ho1a, names = TRUE)
holiday(2024:2025, Holiday = ho1, names = TRUE)

## redundant c() but no harm done
holiday(2024:2025, Holiday = c("Easter"), names = TRUE)
holiday(2024:2025, Holiday = c(Easter), names = TRUE)