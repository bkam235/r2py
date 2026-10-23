# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: aes_cbc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 10

suppressPackageStartupMessages(library(openssl))
# aes-256 requires 32 byte key
passphrase <- charToRaw("This is super secret")
key <- sha256(passphrase)

# symmetric encryption uses same key for decryption
x <- serialize(iris, NULL)
y <- aes_cbc_encrypt(x, key = key)
x2 <- aes_cbc_decrypt(y, key = key)
stopifnot(identical(x, x2))