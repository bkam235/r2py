# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_worktree.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 35

suppressPackageStartupMessages(library(gert))
repo <- git_init(tempfile("gert-examples-repo"))

writeLines("hello", file.path(repo, 'hello.txt'))
git_add('hello.txt', repo = repo)
git_commit("First commit", author = "jeroen <jeroen@blabla.nl>", repo = repo)

# Create a branch that is going to be used for the worktree,
# but don't check it out!
git_branch_create(branch = "branch", checkout = FALSE, repo = repo)

path <- tempfile("gert-examples-worktree")

# Add a worktree for this branch
git_worktree_add(
  name = "worktree",
  path = path,
  branch = "branch",
  repo = repo
)

# Worktree info
git_worktree_list(repo = repo)

# Note how the files are checked out here
dir(path, all.files = TRUE)

# And the branch that we are on at `path` is `"branch"`
git_branch(repo = path)

# Cleanup worktree, and the folder at `path`
git_worktree_remove("worktree", repo = repo)

# Cleanup repo
unlink(repo, recursive = TRUE)