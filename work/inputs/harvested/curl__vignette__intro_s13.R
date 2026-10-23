# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 5

suppressPackageStartupMessages(library(curl))
try({
h <- new_handle(failonerror = TRUE)
curl_fetch_memory('https://cloud.r-project.org/CRAN_mirrorZ.csv', handle = h)
})