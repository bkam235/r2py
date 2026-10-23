# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 11

suppressPackageStartupMessages(library(lifecycle))
lifecycle::deprecate_warn(
  when = "1.0.0",
  what = I('Setting the global option "pkg.opt" to "foo"')
)

lifecycle::deprecate_warn(
  when = "1.0.0",
  what = I('The global option "pkg.another_opt"'),
  with = I('"pkg.this_opt"')
)