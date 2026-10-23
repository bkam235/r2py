# r2py crawler metadata
# package: base64enc
# source_type: rd_example
# topic: dataURI.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\base64enc\help
# lines: 10

suppressPackageStartupMessages(library(base64enc))
dataURI(as.raw(1:10)) # default is base64
  dataURI(as.raw(1:10), encoding=NULL) # URI
  if (require("png", quietly=TRUE)) {
    # let's say you have an image - e.g. from dev.capture(TRUE)
    img <- matrix(1:16/16, 4)
    dataURI(writePNG(img), "image/png")
    # or straight from a file
    dataURI(file=system.file("img", "Rlogo.png", package="png"), mime="image/png")
  }