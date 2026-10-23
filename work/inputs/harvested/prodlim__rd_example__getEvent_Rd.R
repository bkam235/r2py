# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: getEvent.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 7

suppressPackageStartupMessages(library(prodlim))
dat= data.frame(time=1:5,event=letters[1:5])
  x=with(dat,Hist(time,event))
  ## inside integer
  unclass(x)
  ## extract event (the extra level "unknown" is for censored data)
  getEvent(x)