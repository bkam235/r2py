# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: msg_cat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 8

suppressPackageStartupMessages(library(xfun))
{
    # a message without a newline at the end
    xfun::msg_cat("Hello world!")
    # add a newline at the end
    xfun::msg_cat(" This message appears right after the previous one.\n")
}
suppressMessages(xfun::msg_cat("Hello world!"))