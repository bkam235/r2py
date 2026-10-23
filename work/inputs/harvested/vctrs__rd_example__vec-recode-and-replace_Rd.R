# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec-recode-and-replace.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 97

suppressPackageStartupMessages(library(vctrs))
x <- c(1, 2, 3, 1, 2, 4, NA, 5)

# Imagine you have a pre-existing lookup table
likert <- data.frame(
  from = c(1, 2, 3, 4, 5),
  to = c(
    "Strongly disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly agree"
  )
)
vec_recode_values(x, from = likert$from, to = likert$to)

# If you don't map all of the values, a `default` is used
x <- c(1, 2, 3, 1, 2, 4, NA, 5, 6, 7)
vec_recode_values(x, from = likert$from, to = likert$to)
vec_recode_values(x, from = likert$from, to = likert$to, default = "Unknown")

# If you want existing `NA`s to pass through, include a mapping for `NA` in
# your lookup table
likert <- data.frame(
  from = c(1, 2, 3, 4, 5, NA),
  to = c(
    "Strongly disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly agree",
    NA
  )
)
vec_recode_values(x, from = likert$from, to = likert$to, default = "Unknown")

# If you believe you've captured all of the cases, you can assert this with
# `unmatched = "error"`, which will error if you've missed any cases
# (including `NA`, which must be explicitly handled)
try(vec_recode_values(
  x,
  from = likert$from,
  to = likert$to,
  unmatched = "error"
))

if (require("tibble")) {
  # If you want to partially update `x`, retaining the type of `x` and
  # leaving values not covered by `from` alone, use `vec_replace_values()`
  universities <- c(
    "Duke",
    "Fake U",
    "Duke U",
    NA,
    "Chapel Hill",
    "UNC",
    NA,
    "Duke"
  )

  standardize <- tibble::tribble(
    ~from, ~to,
    "Duke", "Duke University",
    "Duke U", "Duke University",
    "UNC", "UNC Chapel Hill",
    "Chapel Hill", "UNC Chapel Hill",
  )
  vec_replace_values(
    universities,
    from = standardize$from,
    to = standardize$to
  )

  # In this case, you can use a more powerful feature of
  # `vec_replace_values()`, `from_as_list_of_vectors`, which allows you to
  # provide a list of `from` vectors that each match multiple `from` values
  # to a single `to` value. `tribble()` can help you create these!
  standardize <- tibble::tribble(
    ~from, ~to,
    c("Duke", "Duke U"), "Duke University",
    c("UNC", "Chapel Hill"), "UNC Chapel Hill",
  )

  # Note how `from` is a list column
  standardize

  vec_replace_values(
    universities,
    from = standardize$from,
    to = standardize$to,
    from_as_list_of_vectors = TRUE
  )

  # `vec_replace_values()` is also a useful way to map from or to `NA`
  vec_replace_values(universities, from = NA, to = "Unknown")
  vec_replace_values(universities, from = "Fake U", to = NA)
}