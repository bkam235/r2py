# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 8

suppressPackageStartupMessages(library(curl))
h <- new_handle()
handle_setopt(h, copypostfields = "moo=moomooo");
handle_setheaders(h,
  "Content-Type" = "text/moo",
  "Cache-Control" = "no-cache",
  "User-Agent" = "A cow"
)