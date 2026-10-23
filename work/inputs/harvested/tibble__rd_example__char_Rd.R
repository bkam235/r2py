# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: char.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 32

suppressPackageStartupMessages(library(tibble))
# Display as a vector:
char(letters[1:3])
if ({ set.seed(20210331); rlang::is_installed("stringi") }) withAutoprint({ # examplesIf
# Space constraints:
rand_strings <- stringi::stri_rand_strings(10, seq(40, 22, by = -2))

# Plain character vectors get truncated if space is limited:
data_with_id <- function(id) {
  tibble(
    id,
    some_number_1 = 1, some_number_2 = 2, some_number_3 = 3,
    some_number_4 = 4, some_number_5 = 5, some_number_6 = 6,
    some_number_7 = 7, some_number_8 = 8, some_number_9 = 9
  )
}
data_with_id(rand_strings)

# Use char() to avoid or control truncation
data_with_id(char(rand_strings, min_chars = 24))
data_with_id(char(rand_strings, min_chars = Inf))
data_with_id(char(rand_strings, min_chars = 24, shorten = "mid"))

# Lorem Ipsum, one sentence per row.
lipsum <- unlist(strsplit(stringi::stri_rand_lipsum(1), "(?<=[.]) +", perl = TRUE))
tibble(
  back = char(lipsum, shorten = "back"),
  front = char(lipsum, shorten = "front"),
  mid = char(lipsum, shorten = "mid")
)
tibble(abbr = char(lipsum, shorten = "abbreviate"))
}) # examplesIf