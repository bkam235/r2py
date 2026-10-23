# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: createRenderFunction.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 60

suppressPackageStartupMessages(library(shiny))
# A custom render function that repeats the supplied value 3 times
renderTriple <- function(expr) {
  # Wrap user-supplied reactive expression into a function
  func <- quoToFunction(rlang::enquo0(expr))

  createRenderFunction(
    func,
    transform = function(value, session, name, ...) {
      paste(rep(value, 3), collapse=", ")
    },
    outputFunc = textOutput
  )
}

# For better legacy support, consider using installExprFunction() over quoToFunction()
renderTripleLegacy <- function(expr, env = parent.frame(), quoted = FALSE) {
  func <- installExprFunction(expr, "func", env, quoted)

  createRenderFunction(
    func,
    transform = function(value, session, name, ...) {
      paste(rep(value, 3), collapse=", ")
    },
    outputFunc = textOutput
  )
}

# Test render function from the console
reactiveConsole(TRUE)

v <- reactiveVal("basic")
r <- renderTriple({ v() })
r()
#> [1] "basic, basic, basic"

# User can supply quoted code via rlang::quo(). Note that evaluation of the
# expression happens when r2() is invoked, not when r2 is created.
q <- rlang::quo({ v() })
r2 <- rlang::inject(renderTriple(!!q))
v("rlang")
r2()
#> [1] "rlang, rlang, rlang"

# Supplying quoted code without rlang::quo() requires installExprFunction()
expr <- quote({ v() })
r3 <- renderTripleLegacy(expr, quoted = TRUE)
v("legacy")
r3()
#> [1] "legacy, legacy, legacy"

# The legacy approach also supports with quosures (env is ignored in this case)
q <- rlang::quo({ v() })
r4 <- renderTripleLegacy(q, quoted = TRUE)
v("legacy-rlang")
r4()
#> [1] "legacy-rlang, legacy-rlang, legacy-rlang"

# Turn off reactivity in the console
reactiveConsole(FALSE)