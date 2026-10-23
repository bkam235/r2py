# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: substr_ctl.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 54

suppressPackageStartupMessages(library(fansi))
substr_ctl("\033[42mhello\033[m world", 1, 9)
substr_ctl("\033[42mhello\033[m world", 3, 9)

## Positions 2 and 4 are in the middle of the full width W (\uFF37) for
## the `start` and `stop` positions respectively. Use `round`
## to control result:
x <- "\uFF37n\uFF37"
x
substr2_ctl(x, 2, 4, type='width', round='start')
substr2_ctl(x, 2, 4, type='width', round='stop')
substr2_ctl(x, 2, 4, type='width', round='neither')
substr2_ctl(x, 2, 4, type='width', round='both')

## We can specify which escapes are considered special:
substr_ctl("\033[31mhello\tworld", 1, 6, ctl='sgr', warn=FALSE)
substr_ctl("\033[31mhello\tworld", 1, 6, ctl=c('all', 'c0'), warn=FALSE)

## `carry` allows SGR to carry from one element to the next
substr_ctl(c("\033[33mhello", "world"), 1, 3)
substr_ctl(c("\033[33mhello", "world"), 1, 3, carry=TRUE)
substr_ctl(c("\033[33mhello", "world"), 1, 3, carry="\033[44m")

## We can omit the termination
bleed <- substr_ctl(c("\033[41mhello", "world"), 1, 3, terminate=FALSE)
writeLines(bleed)      # Style will bleed out of string
end <- "\033[0m\n"
writeLines(end)        # Stanch bleeding

## Trailing sequences omitted unless `stop` past end.
substr_ctl("ABC\033[42m", 1, 3, terminate=FALSE)
substr_ctl("ABC\033[42m", 1, 4, terminate=FALSE)

## Replacement functions
x0<- x1 <- x2 <- x3 <- c("\033[42mABC", "\033[34mDEF")
substr_ctl(x1, 2, 2) <- "_"
substr_ctl(x2, 2, 2) <- "\033[m_"
substr_ctl(x3, 2, 2) <- "\033[45m_"
writeLines(c(x0, end, x1, end, x2, end, x3, end))

## With `carry = TRUE` strings look like original
x0<- x1 <- x2 <- x3 <- c("\033[42mABC", "\033[34mDEF")
substr_ctl(x0, 2, 2, carry=TRUE) <- "_"
substr_ctl(x1, 2, 2, carry=TRUE) <- "\033[m_"
substr_ctl(x2, 2, 2, carry=TRUE) <- "\033[45m_"
writeLines(c(x0, end, x1, end, x2, end, x3, end))

## Work-around to specify carry strings in replacement mode
x <- c("ABC", "DEF")
val <- "#"
x2 <- c("\033[42m", x)
val2 <- c("\033[45m", rep_len(val, length(x)))
substr_ctl(x2, 2, 2, carry=TRUE) <- val2
(x <- x[-1])