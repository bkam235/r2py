# r2py crawler metadata
# package: xtable
# source_type: rd_example
# topic: autoformat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\help
# lines: 31

suppressPackageStartupMessages(library(xtable))
## 1  Vector
xalign(precip)
xdigits(precip)
xdisplay(precip)


## 2  Data frame
head(mtcars)
xdigits(mtcars, pad = FALSE)
xdigits(mtcars, pad = TRUE)
xalign(mtcars)
xdisplay(mtcars)


## 3  Autoformat when xtable is created
xtable(mtcars, align = xalign(mtcars), digits = xdigits(mtcars),
       display = xdisplay(mtcars))

## equivalent shortcut
xtable(mtcars, auto = TRUE)


## 4  Autoformat existing xtable
mt <- xtable(mtcars)
align(mt) <- xalign(mt)
digits(mt) <- xdigits(mt)
display(mt) <- xdisplay(mt)

## equivalent shortcut
mt <- autoformat(mt)