# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_fetch.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 29

suppressPackageStartupMessages(library(gert))
{# Clone a small repository
git_dir <- file.path(tempdir(), 'antiword')
git_clone('https://github.com/ropensci/antiword', git_dir)

# Change into the repo directory
olddir <- getwd()
setwd(git_dir)

# Show some stuff
git_log()
git_branch_list()
git_remote_list()

# Add a file
write.csv(iris, 'iris.csv')
git_add('iris.csv')

# Commit the change
jerry <- git_signature("Jerry", "jerry@hotmail.com")
git_commit('added the iris file', author = jerry)

# Now in the log:
git_log()

# Cleanup
setwd(olddir)
unlink(git_dir, recursive = TRUE)
}