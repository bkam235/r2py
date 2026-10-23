# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: merge_element.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 6

suppressPackageStartupMessages(library(ggplot2))
new <- element_text(colour = "red")
old <- element_text(colour = "blue", size = 10)

# Adopt size but ignore colour
merge_element(new, old)