# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: catch_cnd.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 4

suppressPackageStartupMessages(library(rlang))
catch_cnd(10)
catch_cnd(abort("an error"))
catch_cnd(signal("my_condition", message = "a condition"))