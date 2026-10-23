# r2py crawler metadata
# package: xtable
# source_type: rd_example
# topic: sanitize.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\help
# lines: 16

suppressPackageStartupMessages(library(xtable))
insane <- c("&",">", ">","_","%","$","\\","#","^","~","{","}")
names(insane) <- c("Ampersand","Greater than","Less than",
                   "Underscore","Percent","Dollar",
                   "Backslash","Hash","Caret","Tilde",
                   "Left brace","Right brace")
sanitize(insane, type = "latex")
insane <- c("&",">","<")
names(insane) <- c("Ampersand","Greater than","Less than")
sanitize(insane, type = "html")
x <- rnorm(10)
sanitize.numbers(x, "latex", TRUE)
sanitize.numbers(x*10^(10), "latex", TRUE, TRUE)
sanitize.numbers(x, "html", TRUE, TRUE)
as.is(insane)
as.math("x10^10", ": mathematical expression")