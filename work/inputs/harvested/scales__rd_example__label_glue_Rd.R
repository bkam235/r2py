# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_glue.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 11

suppressPackageStartupMessages(library(scales))
# Example variables
animal  <- "penguin"
species <- c("Adelie",  "Chinstrap", "Emperor", "Gentoo")

# Typical use, note that {x} will become the breaks
demo_discrete(species, labels = label_glue("The {x}\n{animal}"))
# It adapts to the breaks that are present
demo_discrete(species[-3], labels =  label_glue("The {x}\n{animal}"))
# Contrary to directly glueing species + animal, which results in mislabelling!
demo_discrete(species[-3], labels = glue::glue("The {species}\n{animal}"))