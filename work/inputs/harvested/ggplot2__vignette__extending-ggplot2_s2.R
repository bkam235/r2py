# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 14

suppressPackageStartupMessages(library(ggplot2))
#| label: ggproto-intro
A <- ggproto("A", NULL,
  x = 1,
  inc = function(self) {
    self$x <- self$x + 1
  }
)
A$x
A$inc()
A$x
A$inc()
A$inc()
A$x