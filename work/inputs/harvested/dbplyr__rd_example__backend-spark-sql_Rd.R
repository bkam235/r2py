# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: backend-spark-sql.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 10

suppressPackageStartupMessages(library(dbplyr))
library(dplyr, warn.conflicts = FALSE)

lf <- lazy_frame(a = TRUE, b = 1, d = 2, c = "z", con = simulate_spark_sql())

lf %>% summarise(x = median(d, na.rm = TRUE))
lf %>% summarise(x = var(c, na.rm = TRUE), .by = d)

lf %>% mutate(x = first(c))
lf %>% mutate(x = first(c), .by = d)