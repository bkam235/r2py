# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: dateInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 35

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  dateInput("date1", "Date:", value = "2012-02-29"),

  # Default value is the date in client's time zone
  dateInput("date2", "Date:"),

  # value is always yyyy-mm-dd, even if the display format is different
  dateInput("date3", "Date:", value = "2012-02-29", format = "mm/dd/yy"),

  # Pass in a Date object
  dateInput("date4", "Date:", value = Sys.Date()-10),

  # Use different language and different first day of week
  dateInput("date5", "Date:",
          language = "ru",
          weekstart = 1),

  # Start with decade view instead of default month view
  dateInput("date6", "Date:",
            startview = "decade"),

  # Disable Mondays and Tuesdays.
  dateInput("date7", "Date:", daysofweekdisabled = c(1,2)),

  # Disable specific dates.
  dateInput("date8", "Date:", value = "2012-02-29",
            datesdisabled = c("2012-03-01", "2012-03-02"))
)

shinyApp(ui, server = function(input, output) { })
}