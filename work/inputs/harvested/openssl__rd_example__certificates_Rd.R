# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: certificates.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 11

suppressPackageStartupMessages(library(openssl))
# Verify the r-project HTTPS cert
chain <- download_ssl_cert("cran.r-project.org", 443)
print(chain)
cert_data <- as.list(chain[[1]])
print(cert_data$pubkey)
print(cert_data$alt_names)
cert_verify(chain, ca_bundle())

# Write cert in PEM format
cat(write_pem(chain[[1]]))