# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: env_option.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 15

suppressPackageStartupMessages(library(xfun))
xfun::env_option("xfun.test.option")  # NULL

Sys.setenv(R_XFUN_TEST_OPTION = "1234")
xfun::env_option("xfun.test.option")  # 1234

options(xfun.test.option = TRUE)
xfun::env_option("xfun.test.option")  # TRUE (from options())
options(xfun.test.option = NULL)  # reset the option
xfun::env_option("xfun.test.option")  # 1234 (from env var)

Sys.unsetenv("R_XFUN_TEST_OPTION")
xfun::env_option("xfun.test.option")  # NULL again

xfun::env_option("xfun.test.option", FALSE)  # use default