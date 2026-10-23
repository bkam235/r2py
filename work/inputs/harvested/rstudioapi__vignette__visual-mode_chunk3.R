# r2py crawler metadata
# package: rstudioapi
# source_type: vignette
# topic: visual-mode_chunk3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rstudioapi\doc\visual-mode.Rmd
# lines: 7

suppressPackageStartupMessages(library(rstudioapi))
reformat <- function() {
  id <- rstudioapi::documentId(allowConsole = TRUE)
  selection <- rstudioapi::selectionGet(id = id)
  formatted <- styler::style_text(text = selection$value)
  rstudioapi::selectionSet(value = formatted, id = id)
}