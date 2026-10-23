# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: compatibility_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\compatibility.R
# lines: 9

suppressPackageStartupMessages(library(S7))
Foo <- new_class("Foo")
class(Foo())

mean.Foo <- function(x, ...) {
  "mean of foo"
}

mean(Foo())