# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: quo_label.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 17

suppressPackageStartupMessages(library(rlang))
# Quosures can contain nested quosures:
quo <- quo(foo(!! quo(bar)))
quo

# quo_squash() unwraps all quosures and returns a raw expression:
quo_squash(quo)

# This is used by quo_text() and quo_label():
quo_text(quo)

# Compare to the unwrapped expression:
expr_text(quo)

# quo_name() is helpful when you need really short labels:
quo_name(quo(sym))
quo_name(quo(!! sym))