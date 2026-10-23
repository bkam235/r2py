# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: combine_ansi_styles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 14

suppressPackageStartupMessages(library(cli))
## Use style names
alert <- combine_ansi_styles("bold", "red4")
cat(alert("Warning!"), "\n")

## Or style functions
alert <- combine_ansi_styles(style_bold, col_red, bg_cyan)
cat(alert("Warning!"), "\n")

## Combine a composite style
alert <- combine_ansi_styles(
  "bold",
  combine_ansi_styles("red", bg_cyan))
cat(alert("Warning!"), "\n")