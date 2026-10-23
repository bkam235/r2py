# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: check_pivot_spec.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 11

suppressPackageStartupMessages(library(tidyr))
# A valid spec
spec <- tibble(.name = "a", .value = "b", foo = 1)
check_pivot_spec(spec)

spec <- tibble(.name = "a")
try(check_pivot_spec(spec))

# `.name` and `.value` are forced to be the first two columns
spec <- tibble(foo = 1, .value = "b", .name = "a")
check_pivot_spec(spec)