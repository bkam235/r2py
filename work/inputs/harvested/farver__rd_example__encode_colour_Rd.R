# r2py crawler metadata
# package: farver
# source_type: rd_example
# topic: encode_colour.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\farver\help
# lines: 11

suppressPackageStartupMessages(library(farver))
spectrum <- decode_colour(rainbow(10))

encode_colour(spectrum)

# Attach alpha values
encode_colour(spectrum, alpha = c(0.5, 1))

# Encode from a different colour space
spectrum_hcl <- convert_colour(spectrum, 'rgb', 'hcl')
encode_colour(spectrum_hcl, from = 'hcl')