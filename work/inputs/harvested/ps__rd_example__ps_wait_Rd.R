# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_wait.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 17

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ! ps:::is_cran_check() && ps::ps_os_type()["POSIX"]) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# this example calls `sleep`, so it only works on Unix
p1 <- processx::process$new("sleep", "100")
p2 <- processx::process$new("sleep", "100")

# returns c(FALSE, FALSE) immediately if p1 and p2 are running
ps_wait(list(p1$as_ps_handle(), p2$as_ps_handle()), 0)

# timeouts at one second
ps_wait(list(p1$as_ps_handle(), p2$as_ps_handle()), 1000)

p1$kill()
p2$kill()
# returns c(TRUE, TRUE) immediately
ps_wait(list(p1$as_ps_handle(), p2$as_ps_handle()), 1000)
}) # examplesIf