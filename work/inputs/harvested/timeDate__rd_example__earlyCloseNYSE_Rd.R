# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: earlyCloseNYSE.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 7

suppressPackageStartupMessages(library(timeDate))
earlyCloseNYSE(1990)

earlyCloseNYSE(2022:2024) # early closings
holidayNYSE(2022:2024)    # holidays
## early closings & holidays combined
c(earlyCloseNYSE(2022:2024), holidayNYSE(2022:2024))