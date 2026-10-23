# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: diagram.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 17

suppressPackageStartupMessages(library(diagram))
## show examples (see respective help pages for details)
example(plotmat)
example(plotweb)

## run demos
demo("flowchart") # creating flow charts
demo("plotmat")   # plotting diagrams inputted as a matrix
demo("plotweb")   # plotting webs inputted as a matrix

## open the directory with source code of demos
browseURL(paste(system.file(package="diagram"), "/demo", sep=""))

## show package vignette
vignette("diagram")
edit(vignette("diagram"))
browseURL(paste(system.file(package="diagram"), "/doc", sep=""))