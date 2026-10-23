# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: Extract_PaletteOfStyles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 5

suppressPackageStartupMessages(library(diffobj))
pal <- PaletteOfStyles()
pal[["ansi256", "light", "rgb"]]
pal["ansi256", "light", ]
pal["ansi256", "light", "rgb"] <- list(StyleAnsi8NeutralRgb())