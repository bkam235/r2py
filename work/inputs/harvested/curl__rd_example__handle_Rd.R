# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: handle.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 24

suppressPackageStartupMessages(library(curl))
h <- new_handle()
handle_setopt(h, customrequest = "PUT")
handle_setform(h, a = "1", b = "2")
r <- curl_fetch_memory("https://hb.cran.dev/put", h)
cat(rawToChar(r$content))

# Or use the list form
h <- new_handle()
handle_setopt(h, .list = list(customrequest = "PUT"))
handle_setform(h, .list = list(a = "1", b = "2"))
r <- curl_fetch_memory("https://hb.cran.dev/put", h)
cat(rawToChar(r$content))

# Posting multipart forms
h <- new_handle()
handle_setform(h,
  foo = "blabla",
  bar = charToRaw("boeboe"),
  iris = form_data(serialize(iris, NULL), "application/rda"),
  description = form_file(system.file("DESCRIPTION")),
  logo = form_file(file.path(R.home('doc'), "html/logo.jpg"), "image/jpeg")
)
req <- curl_fetch_memory("https://hb.cran.dev/post", handle = h)