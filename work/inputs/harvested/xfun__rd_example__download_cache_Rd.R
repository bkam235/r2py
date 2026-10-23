# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: download_cache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 21

suppressPackageStartupMessages(library(xfun))
if (interactive()) {
# the first time it may take a few seconds
x1 = xfun::download_cache$get("https://www.r-project.org/")
head(x1)

# now you can get the cached content
x2 = xfun::download_cache$get("https://www.r-project.org/")
identical(x1, x2)  # TRUE

# a binary file
x3 = xfun::download_cache$get("https://yihui.org/images/logo.png", "raw")
length(x3)

# show a summary
xfun::download_cache$summary()
# remove a specific cache file
xfun::download_cache$remove("https://yihui.org/images/logo.png", "raw")
# remove all cache files
xfun::download_cache$purge()
}