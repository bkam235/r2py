# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: cache_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 28

suppressPackageStartupMessages(library(httr))
# Never cached, always causes redownload
r1 <- GET("https://www.google.com")
cache_info(r1)
r1$date
rerequest(r1)$date

# Expires in a year
r2 <- GET("https://www.google.com/images/srpr/logo11w.png")
cache_info(r2)
r2$date
rerequest(r2)$date


# Has last-modified and etag, so does revalidation
r3 <- GET("http://httpbin.org/cache")
cache_info(r3)
r3$date
rerequest(r3)$date

# Expires after 5 seconds
r4 <- GET("http://httpbin.org/cache/5")
cache_info(r4)
r4$date
rerequest(r4)$date
Sys.sleep(5)
cache_info(r4)
rerequest(r4)$date