# r2py crawler metadata
# package: pillar
# source_type: vignette
# topic: extending_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\doc\extending.R
# lines: 10

suppressPackageStartupMessages(library(pillar))
example_tbl <- function(class = NULL) {
  vctrs::new_data_frame(
    list(
      a = letters[1:3],
      b = data.frame(c = 1:3, d = 4:6 + 0.5)
    ),
    class = c(class, "tbl")
  )
}