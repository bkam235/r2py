# r2py crawler metadata
# package: textshaping
# source_type: rd_example
# topic: get_font_features.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\textshaping\help
# lines: 7

suppressPackageStartupMessages(library(textshaping))
# Select a random font on the system
sys_fonts <- systemfonts::system_fonts()
random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]

# Get the features
get_font_features(random_font)