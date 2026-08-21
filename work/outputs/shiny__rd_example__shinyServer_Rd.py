# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 5

from shiny import App, render, ui

# A very simple Shiny app that takes a message from the user
# and outputs an uppercase version of it.
# r2py:entity:shinyServer
def server(input, output, session):
# r2py:entity:output$uppercase
    @render.text
    def uppercase():
# r2py:entity:toupper
        return input.message.upper()

# It is also possible for a server.R file to simply return the function,
# without calling shinyServer().
# For example, the server.R file could contain just the following:
def server_alternative(input, output, session):
    @render.text
    def uppercase():
        return input.message.upper()