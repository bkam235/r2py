# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: rand_bytes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 19

suppressPackageStartupMessages(library(openssl))
rnd <- rand_bytes(10)
as.numeric(rnd)
as.character(rnd)
as.logical(rawToBits(rnd))

# bytes range from 0 to 255
rnd <- rand_bytes(100000)
hist(as.numeric(rnd), breaks=-1:255)

# Generate random doubles between 0 and 1
rand_num(5)

# Use CDF to map [0,1] into random draws from a distribution
x <- qnorm(rand_num(1000), mean=100, sd=15)
hist(x)

y <- qbinom(rand_num(1000), size=10, prob=0.3)
hist(y)