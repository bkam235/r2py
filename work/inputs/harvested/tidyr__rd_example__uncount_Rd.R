# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: uncount.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 10

suppressPackageStartupMessages(library(tidyr))
df <- tibble(x = c("a", "b"), n = c(1, 2))
uncount(df, n)
uncount(df, n, .id = "id")

# You can also use constants
uncount(df, 2)

# Or expressions
uncount(df, 2 / n)