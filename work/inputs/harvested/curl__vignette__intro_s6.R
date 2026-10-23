# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 8

suppressPackageStartupMessages(library(curl))
pool <- new_pool()
success <- function(req){cat("success:", req$url, ": HTTP:", req$status, "\n")}
failure <- function(err){cat("failure:", err, "\n")}
curl_fetch_multi('https://www.google.com', done = success, fail = failure, pool = pool)
curl_fetch_multi('https://cloud.r-project.org', done = success, fail = failure, pool = pool)
curl_fetch_multi('https://hb.cran.dev/blabla', done = success, fail = failure, pool = pool)
curl_fetch_multi('https://doesnotexit.xyz', done = success, fail = failure, pool = pool)