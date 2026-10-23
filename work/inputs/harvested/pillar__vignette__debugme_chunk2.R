# r2py crawler metadata
# package: pillar
# source_type: vignette
# topic: debugme_chunk2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\doc\debugme.Rmd
# lines: 7

Sys.setenv(DEBUGME = "!!!!pillar")
Sys.setenv(DEBUGME_SHOW_TIMESTAMP = "no")

library(pillar)

tbl <- tibble::tibble(a = 1:3, b = tibble::tibble(c = 4:6, d = 7:9), e = 10:12)
print(tbl, width = 23)