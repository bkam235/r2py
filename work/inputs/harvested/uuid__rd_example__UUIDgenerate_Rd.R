# r2py crawler metadata
# package: uuid
# source_type: rd_example
# topic: UUIDgenerate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\uuid\help
# lines: 24

suppressPackageStartupMessages(library(uuid))
UUIDgenerate()
UUIDgenerate(TRUE)
UUIDgenerate(FALSE)

## see if the randomness is any good
length(unique(UUIDgenerate(n=1000)))

## generate a native UUID vector
(u <- UUIDgenerate(n=3, output="uuid"))

as.character(u)
as.raw(u[1])

UUIDgenerate(output="raw")

## UUID for DNS namespace
DNS.namespace <- "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
## SHA1 (v5) - default
UUIDfromName(DNS.namespace, "r-project.org")
## MD5 (v3)
UUIDfromName(DNS.namespace, "r-project.org", type="md5")

## see ?UUID for more examples on UUID objects