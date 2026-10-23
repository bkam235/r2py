# r2py crawler metadata
# package: yaml
# source_type: rd_example
# topic: as.yaml.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\yaml\help
# lines: 48

suppressPackageStartupMessages(library(yaml))
as.yaml(1:10)
  as.yaml(list(foo=1:10, bar=c("test1", "test2")))
  as.yaml(list(foo=1:10, bar=c("test1", "test2")), indent=3)
  as.yaml(list(foo=1:10, bar=c("test1", "test2")), indent.mapping.sequence=TRUE)
  as.yaml(data.frame(a=1:10, b=letters[1:10], c=11:20))
  as.yaml(list(a=1:2, b=3:4), omap=TRUE)
  as.yaml("multi\nline\nstring")
  as.yaml(function(x) x + 1)
  as.yaml(list(foo=list(list(x = 1, y = 2), list(x = 3, y = 4))))

  # custom handler
  as.yaml(Sys.time(), handlers = list(
    POSIXct = function(x) format(x, "%Y-%m-%d")
  ))

  # custom handler with verbatim output to change how logical vectors are
  # emitted
  as.yaml(c(TRUE, FALSE), handlers = list(
    logical = verbatim_logical))

  # force quotes around a string
  port_def <- "80:80"
  attr(port_def, "quoted") <- TRUE
  x <- list(ports = list(port_def))
  as.yaml(x)

  # custom tag for scalar
  x <- "thing"
  attr(x, "tag") <- "!thing"
  as.yaml(x)

  # custom tag for sequence
  x <- 1:10
  attr(x, "tag") <- "!thing"
  as.yaml(x)

  # custom tag for mapping
  x <- data.frame(a = letters[1:5], b = letters[6:10])
  attr(x, "tag") <- "!thing"
  as.yaml(x)

  # custom tag for each element in a list
  x <- list(1, 2, 3)
  attr(x[[1]], "tag") <- "!a"
  attr(x[[2]], "tag") <- "!b"
  attr(x[[3]], "tag") <- "!c"
  as.yaml(x)