# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: match_fonts.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 6

suppressPackageStartupMessages(library(systemfonts))
# Get the system default sans-serif font in italic
match_fonts('sans', italic = TRUE)

# Try to match it to a thin variant
match_fonts(c('sans', 'serif'), weight = "thin")