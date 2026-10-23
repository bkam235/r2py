# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: inheritance-expectations.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 26

suppressPackageStartupMessages(library(testthat))
x <- data.frame(x = 1:10, y = "x", stringsAsFactors = TRUE)
# A data frame is an S3 object with class data.frame
expect_s3_class(x, "data.frame")
show_failure(expect_s4_class(x, "data.frame"))
# A data frame is built from a list:
expect_type(x, "list")

f <- factor(c("a", "b", "c"))
o <- ordered(f)

# Using multiple class names tests if the object inherits from any of them
expect_s3_class(f, c("ordered", "factor"))
# Use exact = TRUE to test for exact match
show_failure(expect_s3_class(f, c("ordered", "factor"), exact = TRUE))
expect_s3_class(o, c("ordered", "factor"), exact = TRUE)

# An integer vector is an atomic vector of type "integer"
expect_type(x$x, "integer")
# It is not an S3 object
show_failure(expect_s3_class(x$x, "integer"))

# Above, we requested data.frame() converts strings to factors:
show_failure(expect_type(x$y, "character"))
expect_s3_class(x$y, "factor")
expect_type(x$y, "integer")