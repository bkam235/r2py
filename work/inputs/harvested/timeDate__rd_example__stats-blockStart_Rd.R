# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: stats-blockStart.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 11

suppressPackageStartupMessages(library(timeDate))
## timeSequence
# 360 Days Series:
tS <- timeSequence(to = "2022-09-23 09:39:23", length.out = 360)
    
## blockStart | blockEnd
Start <- blockStart(tS, 30)
End <- blockEnd(tS, 30)
Start
End
End - Start