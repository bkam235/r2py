# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: extending_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\extending.R
# lines: 15

suppressPackageStartupMessages(library(roxygen2))
roclet_process.roclet_memo <- function(x, blocks, env, base_path) {
  results <- list()
  
  for (block in blocks) {
    tags <- block_get_tags(block, "memo")

    for (tag in tags) {
      msg <- paste0("[", tag$file, ":", tag$line, "] ", tag$val$message)
      results[[tag$val$header]] <- c(results[[tag$val$header]], msg)
    }
  }
  
  results
}