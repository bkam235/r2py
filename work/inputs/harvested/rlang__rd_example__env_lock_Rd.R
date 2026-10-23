# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env_lock.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 17

suppressPackageStartupMessages(library(rlang))
# New environments are unlocked by default:
env <- env(a = 1)
env_is_locked(env)

# Use env_lock() to lock them:
env_lock(env)
env_is_locked(env)

# Now that `env` is locked, it is no longer possible to remove or
# add bindings. If run, the following would fail:
# env_unbind(env, "a")
# env_bind(env, b = 2)

# Note that even though the environment as a container is locked,
# the individual bindings are still unlocked and can be modified:
env$a <- 10