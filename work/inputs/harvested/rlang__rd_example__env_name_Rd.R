# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_name.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 9

suppressPackageStartupMessages(library(rlang))
# Some environments have specific names:
env_name(global_env())
env_name(ns_env("rlang"))

# Anonymous environments don't have names but are labelled by their
# address in memory:
env_name(env())
env_label(env())