# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: quo_squash.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 7

suppressPackageStartupMessages(library(rlang))
# Quosures can contain nested quosures:
quo <- quo(wrapper(!!quo(wrappee)))
quo

# quo_squash() flattens all the quosures and returns a simple expression:
quo_squash(quo)