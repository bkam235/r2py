library(stats)

# Variable assignment
x <- 42L

# Constant
PI <- 3.14159

# NA usage (§3.7 na_semantics)
na_val <- NA

# Function definition
add_one <- function(n) {
  n + 1
}

# Function call with side-effect prediction (STDOUT)
print(add_one(x))

# If/else — one branch not taken (false branch for branch_extractor)
if (x > 100) {
  cat("big\n")
} else {
  message("small")
}

# super-assignment (§3.7 super_assign)
counter <- 0L
increment <- function() {
  counter <<- counter + 1L
}
increment()

# Indexing (§3.7 indexing_1based)
v <- c(1, 2, 3)
first <- v[1]

# write.csv predicted effect (FILES)
# write.csv(data.frame(x = v), "out.csv")
