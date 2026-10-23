# r2py crawler metadata
# package: httr
# source_type: vignette
# topic: secrets_chunk11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\doc\secrets.Rmd
# lines: 19

suppressPackageStartupMessages(library(httr))
library(openssl)
library(jsonlite)
library(curl)

encrypt <- function(secret, username) {
  url <- paste("https://api.github.com/users", username, "keys", sep = "/")

  resp <- httr::GET(url)
  httr::stop_for_status(resp)
  pubkey <- httr::content(resp)[[1]]$key

  opubkey <- openssl::read_pubkey(pubkey)
  cipher <- openssl::rsa_encrypt(charToRaw(secret), opubkey)
  jsonlite::base64_enc(cipher)
}
  
cipher <- encrypt("<username>\n<password>", "hadley")
cat(cipher)