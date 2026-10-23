# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
starwars[which(starwars$species == "Human"), , drop = FALSE]
starwars[which(starwars$mass > 1000), , drop = FALSE]
starwars[which(starwars$hair_color == "none" & starwars$eye_color == "black"), , drop = FALSE]