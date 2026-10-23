# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_na_value_to_level.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 18

suppressPackageStartupMessages(library(forcats))
# Most factors store NAs in the values:
f1 <- fct(c("a", "b", NA, "c", "b", NA))
levels(f1)
as.integer(f1)
is.na(f1)

# But it's also possible to store them in the levels
f2 <- fct_na_value_to_level(f1)
levels(f2)
as.integer(f2)
is.na(f2)

# If needed, you can convert back to NAs in the values:
f3 <- fct_na_level_to_value(f2)
levels(f3)
as.integer(f3)
is.na(f3)