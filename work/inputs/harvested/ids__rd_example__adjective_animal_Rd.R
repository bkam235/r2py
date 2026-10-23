# r2py crawler metadata
# package: ids
# source_type: rd_example
# topic: adjective_animal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ids\help
# lines: 30

suppressPackageStartupMessages(library(ids))
# Generate a random identifier:
adjective_animal()

# Generate a bunch all at once:
adjective_animal(5)

# Control the style of punctuation with the style argument:
adjective_animal(style = "lower")
adjective_animal(style = "CONSTANT")
adjective_animal(style = "camel")
adjective_animal(style = "kebab")

# Control the number of adjectives used
adjective_animal(n_adjectives = 3)

# This can get out of hand quickly though:
adjective_animal(n_adjectives = 7)

# Limit the length of adjectives and animals used:
adjective_animal(10, max_len = 6)

# The lengths can be controlled for adjectives and animals
# separately, with Inf meaning no limit:
adjective_animal(10, max_len = c(6, Inf), n_adjectives = 2)

# Pass n = NULL to bind arguments to a function
id <- adjective_animal(NULL, n_adjectives = 2, style = "dot", max_len = 6)
id()
id(10)