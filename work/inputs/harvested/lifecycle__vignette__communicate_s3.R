# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 4

suppressPackageStartupMessages(library(lifecycle))
lifecycle::deprecate_warn("1.0.0", "old_fun()", "new_fun()")
lifecycle::deprecate_warn("1.0.0", "fun()", "testthat::fun()")
lifecycle::deprecate_warn("1.0.0", "fun(old_arg)", "fun(new_arg)")