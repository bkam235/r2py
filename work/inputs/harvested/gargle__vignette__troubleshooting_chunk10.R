# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: troubleshooting_chunk10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\troubleshooting.Rmd
# lines: 28

#| eval: !expr can_decrypt
#| purl: !expr can_decrypt
library(gargle)

req <- request_build(
  method = "GET",
  path = "webfonts/v1/webfonts",
  params = list(
    sort = "popularity"
  ),
  key = gargle_api_key(),
  base_url = "https://www.googleapis.com"
)
resp <- request_make(req)
out <- response_process(resp)

lr <- gargle_last_response()
tmp <- tempfile("gargle-last-response-")
saveRDS(lr, tmp)
# you could share this .rds file with a colleague or the gargle maintainer

# how it would look to complete the round trip, i.e. load this on the other end
rt_lr <- readRDS(tmp)

all.equal(lr, rt_lr)

# clean up
unlink("tmp")