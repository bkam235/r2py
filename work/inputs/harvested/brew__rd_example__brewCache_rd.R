# r2py crawler metadata
# package: brew
# source_type: rd_example
# topic: brewCache.rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\brew\help
# lines: 22

suppressPackageStartupMessages(library(brew))
## Turn on caching
brewCacheOn()

## Brew a template
brew(system.file("featurefull.brew",package="brew"),envir=new.env())

## Get the internal cache
cache <- brewCache()

## Inspect
as.list(cache)

## Inspect first file cached in list
as.list(cache)[[1]]

## Inspect environment that contains text and parsed code
as.list(as.list(cache)[[1]]$env)

## Turn off brew caching
brewCacheOff()
rm(cache)