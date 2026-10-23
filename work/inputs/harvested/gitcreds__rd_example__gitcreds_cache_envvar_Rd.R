# r2py crawler metadata
# package: gitcreds
# source_type: rd_example
# topic: gitcreds_cache_envvar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gitcreds\help
# lines: 5

suppressPackageStartupMessages(library(gitcreds))
gitcreds_cache_envvar("https://github.com")
gitcreds_cache_envvar("https://api.github.com/path/to/endpoint")
gitcreds_cache_envvar("https://jane@github.com")
gitcreds_cache_envvar("https://another.site.github.com")