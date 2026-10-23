# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: describe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 29

suppressPackageStartupMessages(library(testthat))
describe("matrix()", {
  it("can be multiplied by a scalar", {
    m1 <- matrix(1:4, 2, 2)
    m2 <- m1 * 2
    expect_equal(matrix(1:4 * 2, 2, 2), m2)
  })
  it("can have not yet tested specs")
})

# Nested specs:
## code
addition <- function(a, b) a + b
division <- function(a, b) a / b

## specs
describe("math library", {
  describe("addition()", {
    it("can add two numbers", {
      expect_equal(1 + 1, addition(1, 1))
    })
  })
  describe("division()", {
    it("can divide two numbers", {
      expect_equal(10 / 2, division(10, 2))
    })
    it("can handle division by 0") #not yet implemented
  })
})