# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 26

suppressPackageStartupMessages(library(testthat))
expect_s3_object <- function(object, class = NULL) {
  if (!rlang::is_string(class) && is.null(class)) {
    rlang::abort("`class` must be a string or NULL.")
  }

  act <- quasi_label(rlang::enquo(object))

  if (!is.object(act$val)) {
    fail(sprintf("Expected %s to be an object.", act$lab))
  } else if (isS4(act$val)) {
    fail(c(
      sprintf("Expected %s to be an S3 object.", act$lab),
      "Actual OO type: S4"
    ))
  } else if (!is.null(class) && !inherits(act$val, class)) {
    fail(c(
      sprintf("Expected %s to inherit from %s.", act$lab, class),
      sprintf("Actual class: %s", class(act$val))
    ))
  } else {
    pass()
  }

  invisible(act$val)
}