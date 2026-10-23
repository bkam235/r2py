# r2py crawler metadata
# package: brew
# source_type: rd_example
# topic: brew.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\brew\help
# lines: 30

suppressPackageStartupMessages(library(brew))
## A port of the Sweave test file.
brew(system.file("brew-test-1.brew",package="brew"),"brew-test-1.tex",envir=new.env())
##clean up generated files
unlink("brew-test-1-1.eps")
unlink("brew-test-1-2.eps")
unlink("brew-test-1.tex")

## Everything you wanted to know about your R session.
brew(system.file("brew-test-2.brew",package="brew"),"brew-test-2.html",envir=new.env())
browseURL(paste('file://',file.path(getwd(),'brew-test-2.html'),sep=''))

## clean up generated files
unlink("brew-test-2.html")

## Don't sully up environment, so use envir=new.env(). Nested brew calls will still work.
brew(system.file("example1.brew",package="brew"),envir=new.env())

## Various ways to print R output 
library(datasets)
brew(system.file("catprint.brew",package="brew"),envir=new.env())
rm(iris)

## The example from the Details section
brew(system.file("featurefull.brew",package="brew"),envir=new.env())

## Using the tplParser argument
tParse <- function(text) paste('Got this: <',text,'>\n',sep='',collapse='')
brew(system.file("featurefull.brew",package="brew"),envir=new.env(),tplParser=tParse)
rm(tParse)