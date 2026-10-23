# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_sprintf.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 36

suppressPackageStartupMessages(library(stringi))
stri_printf("%4s=%.3f", c("e", "e\u00b2", "\u03c0", "\u03c0\u00b2"),
    c(exp(1), exp(2), pi, pi^2))

x <- c(
  "xxabcd",
  "xx\u0105\u0106\u0107\u0108",
  stri_paste(
    "\u200b\u200b\u200b\u200b",
    "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F",
    "abcd"
  ))
stri_printf("[%10s]", x)  # minimum width = 10
stri_printf("[%-10.3s]", x)  # output of max width = 3, but pad to width of 10
stri_printf("[%10s]", x, use_length=TRUE)  # minimum number of Unicode code points = 10

# vectorization wrt all arguments:
p <- runif(10)
stri_sprintf(ifelse(p > 0.5, "P(Y=1)=%1$.2f", "P(Y=0)=%2$.2f"), p, 1-p)

# using a "preformatted" logical vector:
x <- c(TRUE, FALSE, FALSE, NA, TRUE, FALSE)
stri_sprintf("%s) %s", letters[seq_along(x)], c("\u2718", "\u2713")[x+1])

# custom NA/Inf/NaN strings:
stri_printf("%+10.3f", c(-Inf, -0, 0, Inf, NaN, NA_real_),
    na_string="<NA>", nan_string="\U0001F4A9", inf_string="\u221E")

stri_sprintf("UNIX time %1$f is %1$s.", Sys.time())

# the following do not work in sprintf()
stri_sprintf("%1$#- *2$.*3$f", 1.23456, 10, 3)  # two asterisks
stri_sprintf(c("%s", "%f"), pi)  # re-coercion needed
stri_sprintf("%1$s is %1$f UNIX time.", Sys.time())  # re-coercion needed
stri_sprintf(c("%d", "%s"), factor(11:12))  # re-coercion needed
stri_sprintf(c("%s", "%d"), factor(11:12))  # re-coercion needed