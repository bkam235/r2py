# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: ggproto.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 20

suppressPackageStartupMessages(library(ggplot2))
Adder <- ggproto("Adder",
  x = 0,
  add = function(self, n) {
    self$x <- self$x + n
    self$x
  }
 )
is_ggproto(Adder)

Adder$add(10)
Adder$add(10)

Doubler <- ggproto("Doubler", Adder,
  add = function(self, n) {
    ggproto_parent(Adder, self)$add(n * 2)
  }
)
Doubler$x
Doubler$add(10)