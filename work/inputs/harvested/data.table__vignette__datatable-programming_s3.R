# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-programming_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-programming.R
# lines: 10

suppressPackageStartupMessages(library(data.table))
registerS3method("print", "data.frame", function(x, ...) {
  base::print.data.frame(head(x, 2L), ...)
  cat("...\n")
  invisible(x)
})
.opts = options(
  datatable.print.topn=2L,
  datatable.print.nrows=20L
)