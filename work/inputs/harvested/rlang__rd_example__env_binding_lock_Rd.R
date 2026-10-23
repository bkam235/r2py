# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_binding_lock.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 22

suppressPackageStartupMessages(library(rlang))
# Bindings are unlocked by default:
env <- env(a = "A", b = "B")
env_binding_are_locked(env)

# But can optionally be locked:
env_binding_lock(env, "a")
env_binding_are_locked(env)

# If run, the following would now return an error because `a` is locked:
# env_bind(env, a = "foo")
# with_env(env, a <- "bar")

# Let's unlock it. Note that the return value indicate which
# bindings were locked:
were_locked <- env_binding_unlock(env)
were_locked

# Now that it is unlocked we can modify it again:
env_bind(env, a = "foo")
with_env(env, a <- "bar")
env$a