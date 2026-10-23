# r2py crawler metadata
# package: farver
# source_type: rd_example
# topic: convert_colour.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\farver\help
# lines: 7

suppressPackageStartupMessages(library(farver))
spectrum <- decode_colour(rainbow(10))
spec_lab <- convert_colour(spectrum, 'rgb', 'lab')
spec_lab

# Convert between different white references
convert_colour(spec_lab, 'lab', 'lab', white_from = 'D65', white_to = 'F10')