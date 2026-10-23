# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: calc_element.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 13

suppressPackageStartupMessages(library(ggplot2))
t <- theme_grey()
calc_element('text', t)

# Compare the "raw" element definition to the element with calculated inheritance
t$axis.text.x
calc_element('axis.text.x', t, verbose = TRUE)

# This reports that axis.text.x inherits from axis.text,
# which inherits from text. You can view each of them with:
t$axis.text.x
t$axis.text
t$text