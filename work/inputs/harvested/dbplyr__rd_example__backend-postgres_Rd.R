# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: backend-postgres.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 6

suppressPackageStartupMessages(library(dbplyr))
library(dplyr, warn.conflicts = FALSE)

lf <- lazy_frame(a = TRUE, b = 1, c = 2, d = "z", con = simulate_postgres())
lf %>% summarise(x = sd(b, na.rm = TRUE))
lf %>% summarise(y = cor(b, c), z = cov(b, c))