# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_send_signal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 10

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ps::ps_os_type()["POSIX"] && ! ps:::is_cran_check()) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
px <- processx::process$new("sleep", "10")
p <- ps_handle(px$get_pid())
p
ps_send_signal(p, signals()$SIGINT)
p
ps_is_running(p)
px$get_exit_status()
}) # examplesIf