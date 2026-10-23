# r2py crawler metadata
# package: callr
# source_type: rd_example
# topic: r_bg.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\callr\help
# lines: 9

suppressPackageStartupMessages(library(callr))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
rx <- r_bg(function() 1 + 2)

# wait until it is done
rx$wait()
rx$is_alive()
rx$get_result()
}) # examplesIf