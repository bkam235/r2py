# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: cache_rds.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 15

suppressPackageStartupMessages(library(xfun))
f = tempfile()  # the cache file
compute = function(...) {
    res = xfun::cache_rds({
        Sys.sleep(1)
        1:10
    }, file = f, dir = "", ...)
    res
}
compute()  # takes one second
compute()  # returns 1:10 immediately
compute()  # fast again
compute(rerun = TRUE)  # one second to rerun
compute()
unlink(paste0(f, "_*.rds"))