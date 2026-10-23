# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: sample_n.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 28

suppressPackageStartupMessages(library(dplyr))
df <- tibble(x = 1:5, w = c(0.1, 0.1, 0.1, 2, 2))

# sample_n() -> slice_sample() ----------------------------------------------
# Was:
sample_n(df, 3)
sample_n(df, 10, replace = TRUE)
sample_n(df, 3, weight = w)

# Now:
slice_sample(df, n = 3)
slice_sample(df, n = 10, replace = TRUE)
slice_sample(df, n = 3, weight_by = w)

# Note that sample_n() would error if n was bigger than the group size
# slice_sample() will just use the available rows for consistency with
# the other slice helpers like slice_head()
try(sample_n(df, 10))
slice_sample(df, n = 10)

# sample_frac() -> slice_sample() -------------------------------------------
# Was:
sample_frac(df, 0.25)
sample_frac(df, 2, replace = TRUE)

# Now:
slice_sample(df, prop = 0.25)
slice_sample(df, prop = 2, replace = TRUE)