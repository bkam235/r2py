# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: drop_style.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 5

suppressPackageStartupMessages(library(crayon))
make_style(new_style = "maroon", bg = TRUE)
cat(style("I am maroon", "new_style"), "\n")
drop_style("new_style")
"new_style" %in% names(styles())