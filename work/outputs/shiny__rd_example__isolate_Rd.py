from shiny import App, render, ui, reactive
import pandas as pd
import numpy as np

# Mock functions for database operations since they aren't defined in R snippet
# r2py:entity:writeToDatabase
def writeToDatabase(data):
    print(f"Writing to database: {data}")

# Simulation of Shiny's input object for standalone execution
class MockInput:
    def __init__(self):
        self.saveButton = None
        self.dataset = "some_dataset"
        self.valueA = 10
        self.valueB = 20

input = MockInput()

# Block 1: Dependency on saveButton, isolated dataset
@reactive.effect
def effect1():
    # Trigger on saveButton
    _ = input.saveButton 
    
    # isolate(input$dataset) -> In Python, use the context manager
# r2py:entity:data
    with reactive.isolate():
        dataset_name = input.dataset
        # Simulation of get() from R
        data = globals().get(dataset_name) 
# r2py:entity:writeToDatabase
    writeToDatabase(data)

# Block 2: Dependency on saveButton, isolated block of values
@reactive.effect
def effect2():
    # Trigger on saveButton
    _ = input.saveButton 
    
    # isolate a whole block
# r2py:entity:data_1
    with reactive.isolate():
# r2py:entity:a
        a = input.valueA
# r2py:entity:b
        b = input.valueB
# r2py:entity:c
        data = {"a": a, "b": b}
# r2py:entity:writeToDatabase_1
    writeToDatabase(data)

# Block 3: Isolation and scoping tests
@reactive.effect
def effect3():
    global x, y # Use global to mimic R's environment behavior for the print tests
# r2py:entity:x
    x = 1
    # isolate(x <- 2)
# r2py:entity:isolate
    with reactive.isolate():
        x = 2
# r2py:entity:print
    print(x) # 2

# r2py:entity:y
    y = 1
    # Use local() to avoid affecting calling environment
# r2py:entity:isolate_1
    with reactive.isolate():
        def local_scope():
            y_local = 2
        local_scope()
# r2py:entity:print_1
    print(y) # 1

# Block 4: reactiveValues and isolated reactive call
# R's reactiveValues is like a reactive dictionary.
# r2py:entity:values
class ReactiveValues:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        # In a real Shiny app, these would be wrapped in reactive.Value
        # For this snippet, we simulate the access.

values = ReactiveValues(A=1)

# r2py:entity:fun
@reactive.calc
def fun():
# r2py:entity:as.character
    return str(values.A)

# isolate(fun())
# r2py:entity:isolate_2
with reactive.isolate():
    isolated_val = fun()