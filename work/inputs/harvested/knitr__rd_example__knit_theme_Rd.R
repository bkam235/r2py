# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: knit_theme.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 10

suppressPackageStartupMessages(library(knitr))
opts_knit$set(out.format = "latex")
knit_theme$set("edit-vim")

knit_theme$get()  # names of all available themes

thm = knit_theme$get("acid")  # parse the theme to a list
knit_theme$set(thm)

opts_knit$set(out.format = NULL)  # restore option