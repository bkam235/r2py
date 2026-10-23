# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 24

suppressPackageStartupMessages(library(vctrs))
purrr <- c("p", "u", "r", "r", "r")
vec_group_id(purrr)
vec_group_rle(purrr)

groups <- mtcars[c("vs", "am")]
vec_group_id(groups)

group_rle <- vec_group_rle(groups)
group_rle

# Access fields with `field()`
field(group_rle, "group")
field(group_rle, "length")

# `vec_group_id()` is equivalent to
vec_match(groups, vec_unique(groups))

vec_group_loc(mtcars$vs)
vec_group_loc(mtcars[c("vs", "am")])

if (require("tibble")) {
  as_tibble(vec_group_loc(mtcars[c("vs", "am")]))
}