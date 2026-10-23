# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: format_glimpse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 18

suppressPackageStartupMessages(library(pillar))
format_glimpse(1:3)

# Lists use [], vectors inside lists use <>
format_glimpse(list(1:3))
format_glimpse(list(1, 2:3))
format_glimpse(list(list(1), list(2:3)))
format_glimpse(list(as.list(1), as.list(2:3)))
format_glimpse(list(character()))
format_glimpse(list(NULL))

# Character strings are always quoted
writeLines(format_glimpse(letters[1:3]))
writeLines(format_glimpse(c("A", "B, C")))

# Factors are quoted only when needed
writeLines(format_glimpse(factor(letters[1:3])))
writeLines(format_glimpse(factor(c("A", "B, C"))))