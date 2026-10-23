# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_config.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 24

suppressPackageStartupMessages(library(gert))
# Set and inspect a local, custom Git option
r <- file.path(tempdir(), "gert-demo")
git_init(r)

previous <- git_config_set("aaa.bbb", "ccc", repo = r)
previous
cfg <- git_config(repo = r)
subset(cfg, level == "local")
cfg$value[cfg$name == "aaa.bbb"]

previous <- git_config_set("aaa.bbb", NULL, repo = r)
previous
cfg <- git_config(repo = r)
subset(cfg, level == "local")
cfg$value[cfg$name == "aaa.bbb"]

unlink(r, recursive = TRUE)


# Set global Git options
git_config_global_set("user.name", "Your Name")
git_config_global_set("user.email", "your@email.com")
git_config_global()