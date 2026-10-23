# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: specialHolidayGB.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 16

suppressPackageStartupMessages(library(timeDate))
## UK Millenium day
specialHolidayGB(1999)     # as a dateTime object
specialHolidayGB(1999, "") # as a character string

## 2 special holidays in UK in 2022
specialHolidayGB(2022)     # [2022-06-03] [2022-09-19]
## what are their names?
specialHolidayGB(2022, named = TRUE)

## the Spring BH is usually on last Monday of May, but not in 2022
dayOfWeek(GBSpringBankHoliday(2020:2024))

## the above formed a nice 4-day weekend in early June 2022
## (look at the Thu-Fri sequence on 2-3 June)
dayOfWeek(holidayLONDON(2022))