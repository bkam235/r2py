# r2py crawler metadata
# package: openssl
# source_type: vignette
# topic: keys_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\doc\keys.R
# lines: 5

suppressPackageStartupMessages(library(openssl))
key <- ec_keygen()
pubkey <- key$pubkey
bin <- write_der(pubkey)
print(bin)