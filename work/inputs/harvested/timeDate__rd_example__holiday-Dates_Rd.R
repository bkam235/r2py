# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: holiday-Dates.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 7

suppressPackageStartupMessages(library(timeDate))
# Sechselaeuten a half Day Bank Holiday in Switzerland
CHSechselaeuten(2000:2010)
CHSechselaeuten(getRmetricsOptions("currentYear"))

## German Unification Day:
DEGermanUnity(getRmetricsOptions("currentYear"))