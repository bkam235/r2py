# r2py crawler metadata
# package: profvis
# source_type: vignette
# topic: profvis_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\profvis\doc\profvis.R
# lines: 16

library(profvis)
library(knitr)

knitr::opts_chunk$set(collapse = TRUE, comment = "#>")

# Make output a little less tall by default
registerS3method("knit_print", "htmlwidget", function(x, ...) {
  # Get the chunk height
  height <- knitr::opts_current$get("height")
  if (length(height) > 0 && height != FALSE)
    x$height <- height
  else
    x$height <- "450px"

  htmlwidgets:::knit_print.htmlwidget(x, ...)
})