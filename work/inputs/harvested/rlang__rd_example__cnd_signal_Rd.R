# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: cnd_signal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 9

suppressPackageStartupMessages(library(rlang))
# The type of signal depends on the class. If the condition
# inherits from "warning", a warning is issued:
cnd <- warning_cnd("my_warning_class", message = "This is a warning")
cnd_signal(cnd)

# If it inherits from "error", an error is raised:
cnd <- error_cnd("my_error_class", message = "This is an error")
try(cnd_signal(cnd))