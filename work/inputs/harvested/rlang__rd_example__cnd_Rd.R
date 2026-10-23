# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: cnd.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 12

suppressPackageStartupMessages(library(rlang))
# Create a condition inheriting only from the S3 class "foo":
cnd <- cnd("foo")

# Signal the condition to potential handlers. Since this is a bare
# condition the signal has no effect if no handlers are set up:
cnd_signal(cnd)

# When a relevant handler is set up, the signal transfers control
# to the handler
with_handlers(cnd_signal(cnd), foo = function(c) "caught!")
tryCatch(cnd_signal(cnd), foo = function(c) "caught!")