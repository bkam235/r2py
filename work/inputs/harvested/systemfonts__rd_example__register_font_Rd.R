# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: register_font.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 19

suppressPackageStartupMessages(library(systemfonts))
if (nrow(system_fonts()) >= 4) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# Create a random font collection
fonts <- system_fonts()
random_fonts <- sample(nrow(fonts), 4)
register_font(
  'random',
  plain = list(fonts$path[random_fonts[1]], fonts$index[random_fonts[1]]),
  bold = list(fonts$path[random_fonts[2]], fonts$index[random_fonts[2]]),
  italic = list(fonts$path[random_fonts[3]], fonts$index[random_fonts[3]]),
  bolditalic = list(fonts$path[random_fonts[4]], fonts$index[random_fonts[4]])
)

# Look at your creation
registry_fonts()

# Reset
clear_registry()
}) # examplesIf