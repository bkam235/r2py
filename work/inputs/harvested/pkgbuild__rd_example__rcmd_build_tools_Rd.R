# r2py crawler metadata
# package: pkgbuild
# source_type: rd_example
# topic: rcmd_build_tools.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgbuild\help
# lines: 8

suppressPackageStartupMessages(library(pkgbuild))
# These env vars are always set
callr::rcmd_safe_env()

if (has_build_tools()) {
  rcmd_build_tools("CONFIG", "CC")$stdout
  rcmd_build_tools("CC", "--version")$stdout
}