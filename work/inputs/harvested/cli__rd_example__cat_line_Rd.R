# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: cat_line.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 5

suppressPackageStartupMessages(library(cli))
cat_line("This is ", "a ", "line of text.", col = "red")
cat_bullet(letters[1:5])
cat_bullet(letters[1:5], bullet = "tick", bullet_col = "green")
cat_rule()