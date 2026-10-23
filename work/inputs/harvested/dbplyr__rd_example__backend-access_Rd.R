# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: backend-access.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 7

suppressPackageStartupMessages(library(dbplyr))
library(dplyr, warn.conflicts = FALSE)
lf <- lazy_frame(x = 1, y = 2, z = "a", con = simulate_access())

lf %>% head()
lf %>% mutate(y = as.numeric(y), z = sqrt(x^2 + 10))
lf %>% mutate(a = paste0(z, " times"))