# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: combine_styles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 16

suppressPackageStartupMessages(library(crayon))
## Use style names
alert <- combine_styles("bold", "red4", "bgCyan")
cat(alert("Warning!"), "\n")

## Or style functions
alert <- combine_styles(bold, red, bgCyan)
cat(alert("Warning!"), "\n")

## Combine a composite style
alert <- combine_styles(bold, combine_styles(red, bgCyan))
cat(alert("Warning!"), "\n")

## Shorter notation
alert <- bold $ red $ bgCyan
cat(alert("Warning!"), "\n")