# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vctrs-unspecified.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 41

suppressPackageStartupMessages(library(vctrs))
# Returns `unspecified()`
vec_ptype(NA)
vec_ptype(c(NA, NA))

# We've chosen to make this return `logical()`, but this is admittedly
# ambiguous, as it could be seen as "an empty vector of `NA`s" that could
# also be treated as unspecified.
vec_ptype(logical())

# These return `unspecified()`
vec_ptype2(NA, NA)
vec_ptype2(NA, NULL)
vec_ptype2(NULL, NA)

# An unspecified vector can combine with any other type
vec_ptype2(NA, "x")
vec_ptype2("x", NA)

# Same as using `unspecified()` directly
vec_ptype2(unspecified(1), "x")
vec_ptype2("x", unspecified(1))

# Finalising a ptype turns unspecified back to logical
vec_ptype(NA)
vec_ptype_finalise(vec_ptype(NA))

# This works recursively over data frames
df <- data_frame(x = NA, y = data_frame(z = NA))
vec_ptype_show(vec_ptype(df))
vec_ptype_show(vec_ptype_finalise(vec_ptype(df)))

# `vec_ptype_common()` finalises automatically rather than returning an
# unspecified type
vec_ptype_common(NA)
vec_ptype_common(NA, NA)
vec_ptype_show(vec_ptype_common(df))

# `vec_ptype_common()` lets you opt out of finalisation using `.finalise`
vec_ptype_common(NA, .finalise = FALSE)
vec_ptype_show(vec_ptype_common(df, .finalise = FALSE))