# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: do_once.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 13

suppressPackageStartupMessages(library(xfun))
do_once(message("Today's date is ", Sys.Date()), "xfun.date.reminder")
# if you run it again, it will not emit the message again
do_once(message("Today's date is ", Sys.Date()), "xfun.date.reminder")

do_once({
    Sys.sleep(2)
    1 + 1
}, "xfun.task.1plus1")
do_once({
    Sys.sleep(2)
    1 + 1
}, "xfun.task.1plus1")