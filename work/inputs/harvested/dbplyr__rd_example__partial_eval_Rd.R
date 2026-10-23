# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: partial_eval.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 22

suppressPackageStartupMessages(library(dbplyr))
lf <- lazy_frame(year = 1980, id = 1)
partial_eval(quote(year > 1980), data = lf)

ids <- c("ansonca01", "forceda01", "mathebo01")
partial_eval(quote(id %in% ids), lf)

# cf.
partial_eval(quote(id == .data$id), lf)

# You can use local() or .env to disambiguate between local and remote
# variables: otherwise remote is always preferred
year <- 1980
partial_eval(quote(year > year), lf)
partial_eval(quote(year > local(year)), lf)
partial_eval(quote(year > .env$year), lf)

# Functions are always assumed to be remote. Use local to force evaluation
# in R.
f <- function(x) x + 1
partial_eval(quote(year > f(1980)), lf)
partial_eval(quote(year > local(f(1980))), lf)