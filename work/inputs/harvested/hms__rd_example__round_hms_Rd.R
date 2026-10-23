# r2py crawler metadata
# package: hms
# source_type: rd_example
# topic: round_hms.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hms\help
# lines: 9

suppressPackageStartupMessages(library(hms))
round_hms(as_hms("12:34:56"), 5)
round_hms(as_hms("12:34:56"), 60)
round_hms(as_hms("12:34:56.78"), 0.25)
round_hms(as_hms("12:34:56.78"), digits = 1)
round_hms(as_hms("12:34:56.78"), digits = -2)
trunc_hms(as_hms("12:34:56"), 60)
ceiling_hms(as_hms("12:34:56"), 60)
floor_hms(as_hms("12:34:56"), 60)