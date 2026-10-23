# r2py crawler metadata
# package: shape
# source_type: rd_example
# topic: shape.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shape\help
# lines: 15

suppressPackageStartupMessages(library(shape))
## show examples (see respective help pages for details)
example(rotatexy)
example(filledshape)

## run demos
demo("colorshapes") # creating colored shapes

## open the directory with source code of demos
browseURL(paste(system.file(package="shape"), "/demo", sep=""))

## show package vignette
vignette("shape")
edit(vignette("shape"))
browseURL(paste(system.file(package="shape"), "/doc", sep=""))