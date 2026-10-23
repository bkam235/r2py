# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_chunk8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.Rmd
# lines: 6

suppressPackageStartupMessages(library(stringr))
x <- c("Short", "This is a long string")
    
    x %>% 
      str_trunc(10) %>% 
      str_pad(10, "right")