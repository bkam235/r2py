# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_commit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 33

suppressPackageStartupMessages(library(gert))
oldwd <- getwd()
repo <- file.path(tempdir(), "myrepo")
git_init(repo)
setwd(repo)

# Set a user if no default
if(!user_is_configured()){
  git_config_set("user.name", "Jerry")
  git_config_set("user.email", "jerry@gmail.com")
}

writeLines(letters[1:6], "alphabet.txt")
git_status()

git_add("alphabet.txt")
git_status()

git_commit("Start alphabet file")
git_status()

git_ls()

git_log()

cat(letters[7:9], file = "alphabet.txt", sep = "\n", append = TRUE)
git_status()

git_commit_all("Add more letters")

# cleanup
setwd(oldwd)
unlink(repo, recursive = TRUE)