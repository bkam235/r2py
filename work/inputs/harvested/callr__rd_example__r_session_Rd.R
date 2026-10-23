# r2py crawler metadata
# package: callr
# source_type: rd_example
# topic: r_session.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\callr\help
# lines: 13

suppressPackageStartupMessages(library(callr))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
rs <- r_ression$new()

rs$run(function() 1 + 2)

rs$call(function() Sys.sleep(1))
rs$get_state()

rs$poll_process(-1)
rs$get_state()
rs$read()
}) # examplesIf