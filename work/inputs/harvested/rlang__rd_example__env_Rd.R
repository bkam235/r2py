# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: env.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 30

suppressPackageStartupMessages(library(rlang))
# env() creates a new environment that inherits from the current
# environment by default
env <- env(a = 1, b = "foo")
env$b
identical(env_parent(env), current_env())

# Supply one unnamed argument to inherit from another environment:
env <- env(base_env(), a = 1, b = "foo")
identical(env_parent(env), base_env())


# Both env() and child_env() support tidy dots features:
objs <- list(b = "foo", c = "bar")
env <- env(a = 1, !!! objs)
env$c

# You can also unquote names with the definition operator `:=`
var <- "a"
env <- env(!!var := "A")
env$a


# Use new_environment() to create containers with the empty
# environment as parent:
env <- new_environment()
env_parent(env)

# Like other new_ constructors, it takes an object rather than dots:
new_environment(list(a = "foo", b = "bar"))