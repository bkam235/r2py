# r2py crawler metadata
# package: digest
# source_type: rd_example
# topic: vdigest.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\digest\help
# lines: 47

suppressPackageStartupMessages(library(digest))
stretch_key <- function(d, n) {
    md5 <- getVDigest()
    for (i in seq_len(n))
        d <- md5(d, serialize = FALSE)
    d
}
stretch_key('abc123', 65e3)
sha1 <- getVDigest(algo = 'sha1')
sha1(letters)

md5Input <-
    c("",
      "a",
      "abc",
      "message digest",
      "abcdefghijklmnopqrstuvwxyz",
      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
      paste("12345678901234567890123456789012345678901234567890123456789012",
            "345678901234567890", sep=""))
md5Output <-
    c("d41d8cd98f00b204e9800998ecf8427e",
      "0cc175b9c0f1b6a831c399e269772661",
      "900150983cd24fb0d6963f7d28e17f72",
      "f96b697d7cb7938d525a2f31aaf161d0",
      "c3fcd3d76192e4007dfb496cca67e13b",
      "d174ab98d277d9f5a5611c2c9f419d9f",
      "57edf4a22be3c955ac49da2e2107b67a")

md5 <- getVDigest()
stopifnot(identical(md5(md5Input, serialize = FALSE), md5Output))
stopifnot(identical(digest(list("abc")),
                 md5(list(list("abc")))))

sha512Input <-c(
    "",
    "The quick brown fox jumps over the lazy dog."
    )
sha512Output <- c(
    paste0("cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce",
           "47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"),
    paste0("91ea1245f20d46ae9a037a989f54f1f790f0a47607eeb8a14d12890cea77a1bb",
           "c6c7ed9cf205e67b7f2b8fd4c7dfd3a7a8617e45f3c463d481c7e586c39ac1ed")
    )

sha512 <- getVDigest(algo = 'sha512')
stopifnot(identical(sha512(sha512Input, serialize = FALSE), sha512Output))