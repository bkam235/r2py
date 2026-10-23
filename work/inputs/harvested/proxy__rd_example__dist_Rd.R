# r2py crawler metadata
# package: proxy
# source_type: rd_example
# topic: dist.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\proxy\help
# lines: 56

suppressPackageStartupMessages(library(proxy))
### show available proximities
summary(pr_DB)

### get more information about a particular one
pr_DB$get_entry("Jaccard")

### binary data
x <- matrix(sample(c(FALSE, TRUE), 8, replace = TRUE), ncol = 2)
dist(x, method = "Jaccard")

### for real-valued data
dist(x, method = "eJaccard")

### for positive real-valued data
dist(x, method = "fJaccard")

### cross distances
dist(x, x, method = "Jaccard")

### pairwise (diagonal)
dist(x, x, method = "Jaccard", 
	 pairwise = TRUE)

### this is the same but less efficient
as.matrix(stats::dist(x, method = "binary"))

### numeric data
x <- matrix(rnorm(16), ncol = 4)

## test inheritance of names
rownames(x) <- LETTERS[1:4]
colnames(x) <- letters[1:4]
dist(x)
dist(x, x)

## custom distance function
f <- function(x, y) sum(x * y)
dist(x, f)

## working with lists
z <- unlist(apply(x, 1, list), recursive = FALSE)
(d <- dist(z))
dist(z, z)

## subsetting
d[[1:2]]
subset(d, c(1,3,4))
d[[c(1,2,2)]]	    # duplicate index gets ignored

## transformations and self-proximities
as.matrix(as.simil(d, function(x) exp(-x)), diag = 1)

## row and column indexes
row.dist(d)
col.dist(d)