# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: now.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 11

suppressPackageStartupMessages(library(lubridate))
now()
now("GMT")
now("")
now() == now() # would be TRUE if computer processed both at the same instant
now() < now() # TRUE
now() > now() # FALSE
today()
today("GMT")
today() == today("GMT") # not always true
today() < as.Date("2999-01-01") # TRUE  (so far)