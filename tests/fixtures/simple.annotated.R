library(stats)
# r2py: import_stats

# Variable assignment
x <- 42L
# r2py: x

# Constant
PI <- 3.14159
# r2py: PI

# NA usage (§3.7 na_semantics)
na_val <- NA
# r2py: na_val

# Function definition
add_one <- function(n) {
  n + 1
}
# r2py: add_one

# Function call with side-effect prediction (STDOUT)
print(add_one(x))
# r2py: print
# r2py: add_one_1

# If/else — one branch not taken (false branch for branch_extractor)
if (x > 100) {
  cat("big\n")
  # r2py: cat
} else {
  message("small")
  # r2py: message
}

# super-assignment (§3.7 super_assign)
counter <- 0L
# r2py: counter
increment <- function() {
  counter <<- counter + 1L
  # r2py: counter_1
}
# r2py: increment
increment()
# r2py: increment_1

# Indexing (§3.7 indexing_1based)
v <- c(1, 2, 3)
# r2py: v
first <- v[1]
# r2py: first

# write.csv predicted effect (FILES)
# write.csv(data.frame(x = v), "out.csv")
