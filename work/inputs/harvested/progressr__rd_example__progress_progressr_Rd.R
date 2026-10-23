# r2py crawler metadata
# package: progressr
# source_type: rd_example
# topic: progress_progressr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\progressr\help
# lines: 11

suppressPackageStartupMessages(library(progressr))
if (requireNamespace("plyr", quietly=TRUE)) {

  with_progress({
    y <- plyr::llply(1:10, function(x) {
      Sys.sleep(0.1)
      sqrt(x)
    }, .progress = "progressr")
  })
  
}