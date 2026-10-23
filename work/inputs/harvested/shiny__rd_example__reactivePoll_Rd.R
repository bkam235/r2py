# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: reactivePoll.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 21

suppressPackageStartupMessages(library(shiny))
function(input, output, session) {

  data <- reactivePoll(1000, session,
    # This function returns the time that log_file was last modified
    checkFunc = function() {
      if (file.exists(log_file))
        file.info(log_file)$mtime[1]
      else
        ""
    },
    # This function returns the content of log_file
    valueFunc = function() {
      read.csv(log_file)
    }
  )

  output$dataTable <- renderTable({
    data()
  })
}