# r2py crawler metadata
# package: ids
# source_type: rd_example
# topic: uuid.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ids\help
# lines: 9

suppressPackageStartupMessages(library(ids))
# Generate one id
uuid()

# Or a bunch
uuid(10)

# More in the style of random_id()
uuid(drop_hyphens = TRUE)