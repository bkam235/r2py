# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: weighted_table.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 56

suppressPackageStartupMessages(library(hardhat))
x <- factor(c("x", "y", "z", "x", "x", "y"))
y <- factor(c("a", "b", "a", "a", "b", "b"))
w <- c(1.5, 2, 1.1, .5, 3, 2)

weighted_table(x = x, y = y, weights = w)

# ---------------------------------------------------------------------------
# If `weights` contains missing values, then missing values will be
# propagated into the weighted table
x <- factor(c("x", "y", "y"))
y <- factor(c("a", "b", "b"))
w <- c(1, NA, 3)

weighted_table(x = x, y = y, weights = w)

# You can remove the missing values while summing up the weights with
# `na_remove = TRUE`
weighted_table(x = x, y = y, weights = w, na_remove = TRUE)

# ---------------------------------------------------------------------------
# If there are missing values in the factors, those typically don't show
# up in the weighted table
x <- factor(c("x", NA, "y", "x"))
y <- factor(c("a", "b", "a", NA))
w <- 1:4

weighted_table(x = x, y = y, weights = w)

# This is because the missing values aren't considered explicit levels
levels(x)

# You can force them to show up in the table by using `addNA()` ahead of time
# (or `forcats::fct_expand(x, NA)`)
x <- addNA(x, ifany = TRUE)
y <- addNA(y, ifany = TRUE)
levels(x)

weighted_table(x = x, y = y, weights = w)

# ---------------------------------------------------------------------------
# If there are levels in your factors that aren't actually used in the
# underlying data, then they will still show up in the table with a `0` value
x <- factor(c("x", "y", "x"), levels = c("x", "y", "z"))
y <- factor(c("a", "b", "a"), levels = c("a", "b", "c"))
w <- 1:3

weighted_table(x = x, y = y, weights = w)

# If you want to drop these empty factor levels from the result, you can
# rerun `factor()` ahead of time to drop them (or `forcats::fct_drop()`)
x <- factor(x)
y <- factor(y)
levels(x)

weighted_table(x = x, y = y, weights = w)