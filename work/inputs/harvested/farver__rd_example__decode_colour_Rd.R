# r2py crawler metadata
# package: farver
# source_type: rd_example
# topic: decode_colour.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\farver\help
# lines: 9

suppressPackageStartupMessages(library(farver))
# basic use
decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'))

# Return alpha as well (no alpha value is interpreted as 1)
decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), alpha = TRUE)

# Decode directly into specific colour space
decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'), to = 'lch')