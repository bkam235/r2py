# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s65
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 52

suppressPackageStartupMessages(library(clock))
naive_find_by_abbrev <- function(x, abbrev) {
  if (!is_naive_time(x)) {
    abort("`x` must be a naive-time.")
  }
  if (length(x) != 1L) {
    abort("`x` must be length 1.")
  }
  if (!rlang::is_string(abbrev)) {
    abort("`abbrev` must be a single string.")
  }
  
  zones <- tzdb_names()
  info <- naive_time_info(x, zones)
  info$zones <- zones
  
  c(
    compute_uniques(x, info, abbrev),
    compute_ambiguous(x, info, abbrev)
  )
}

compute_uniques <- function(x, info, abbrev) {
  info <- info[info$type == "unique",]
  
  # If the abbreviation of the unique time matches the input `abbrev`,
  # then that candidate zone should be in the output
  matches <- info$first$abbreviation == abbrev
  zones <- info$zones[matches]
  
  lapply(zones, as_zoned_time, x = x)
}

compute_ambiguous <- function(x, info, abbrev) {
  info <- info[info$type == "ambiguous",]

  # Of the two possible times,
  # does the abbreviation of the earliest match the input `abbrev`?
  matches <- info$first$abbreviation == abbrev
  zones <- info$zones[matches]
  
  earliest <- lapply(zones, as_zoned_time, x = x, ambiguous = "earliest")
  
  # Of the two possible times,
  # does the abbreviation of the latest match the input `abbrev`?
  matches <- info$second$abbreviation == abbrev
  zones <- info$zones[matches]
  
  latest <- lapply(zones, as_zoned_time, x = x, ambiguous = "latest")
  
  c(earliest, latest)
}