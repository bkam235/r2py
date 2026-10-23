# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: col_mix.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 7

suppressPackageStartupMessages(library(scales))
col_mix("blue", "red") # purple
col_mix("blue", "red", amount = 1) # red
col_mix("blue", "red", amount = 0) # blue

# Not recommended:
col_mix("blue", "red", space = "hcl") # green!