# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s30
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 11

suppressPackageStartupMessages(library(curl))
# Posting multipart
h <- new_handle()
handle_setform(h,
  foo = "blabla",
  bar = charToRaw("boeboe"),
  iris = form_data(serialize(iris, NULL), "application/rda"),
  description = form_file(system.file("DESCRIPTION")),
  logo = form_file(file.path(R.home('doc'), "html/logo.jpg"), "image/jpeg")
)
req <- curl_fetch_memory("https://hb.cran.dev/post", handle = h)