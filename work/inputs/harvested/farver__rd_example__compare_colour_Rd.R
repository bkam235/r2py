# r2py crawler metadata
# package: farver
# source_type: rd_example
# topic: compare_colour.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\farver\help
# lines: 13

suppressPackageStartupMessages(library(farver))
r <- decode_colour(rainbow(10))
h <- decode_colour(heat.colors(15))

# Compare two sets of colours
compare_colour(r, h, 'rgb', method = 'cie2000')

# Compare a set of colours with itself
compare_colour(r, from_space = 'rgb', method = 'cmc')

# Compare colours from different colour spaces
h_luv <- convert_colour(h, 'rgb', 'luv')
compare_colour(r, h_luv, 'rgb', 'luv')