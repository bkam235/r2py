# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: when.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 17

suppressPackageStartupMessages(library(purrr))
1:10 |>
  when(
    sum(.) <=  50 ~ sum(.),
    sum(.) <= 100 ~ sum(.)/2,
    ~ 0
  )

# now
x <- 1:10
if (sum(x) < 10) {
  sum(x)
} else if (sum(x) < 100) {
  sum(x) / 2
} else {
  0
}