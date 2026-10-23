# r2py crawler metadata
# package: vroom
# source_type: rd_example
# topic: locale.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\help
# lines: 6

suppressPackageStartupMessages(library(vroom))
locale()
locale("fr")

# South American locale
locale("es", decimal_mark = ",")