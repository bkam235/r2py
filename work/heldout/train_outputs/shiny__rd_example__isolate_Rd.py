# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

from shiny import reactive
import pandas as pd
import numpy as np

# Mocking Shiny-like behavior for standalone execution as per the R source's logic
class MockInput:
    def __init__(self):
        self.saveButton = None
        self.dataset = "some_dataset"
        self.valueA = 10
        self.valueB = 20

input = MockInput()

# r2py:entity:writeToDatabase
def writeToDatabase(data):
    # Approximation of writeToDatabase side effect
    pass

# r2py:entity:isolate
def isolate(expr):
    # In R, isolate prevents the expression from creating a reactive dependency.
    # In this standalone translation, it simply executes the expression.
    if callable(expr):
        return expr()
    return expr

# Snippet 1: observe({ ... })
def observe_1():
    # input$saveButton (dependency)
    _ = input.saveButton
    
    # isolate a simple expression
    # data <- get(isolate(input$dataset))
# r2py:entity:data
    dataset_name = isolate(input.dataset)
    # r2py:entity:data
    data = globals().get(dataset_name, None)
    # r2py:entity:writeToDatabase
    writeToDatabase(data)

# Snippet 2: observe({ ... })
def observe_2():
    # input$saveButton (dependency)
    _ = input.saveButton
    
    # isolate a whole block
    # data <- isolate({ ... })
# r2py:entity:data_1
    def isolated_block():
        # r2py:entity:a
# r2py:entity:a
        a = input.valueA
        # r2py:entity:b
# r2py:entity:b
        b = input.valueB
        # r2py:entity:c
# r2py:entity:c
        return {"a": a, "b": b}
    
    # r2py:entity:data_1
    data = isolate(isolated_block)
    # r2py:entity:writeToDatabase_1
# r2py:entity:writeToDatabase_1
    writeToDatabase(data)

# Snippet 3: observe({ ... })
def observe_3():
    # r2py:entity:x
# r2py:entity:x
    global x
    x = 1
    # x outside of isolate() is affected
    # isolate(x <- 2)
    def update_x():
        global x
        x = 2
    # r2py:entity:isolate
    isolate(update_x)
    # r2py:entity:print
# r2py:entity:print
    print(x) # 2

    # r2py:entity:y
# r2py:entity:y
    global y
    y = 1
    # Use local() to avoid affecting calling environment
    # isolate(local(y <- 2))
# r2py:entity:isolate_1
    def local_update_y():
        y = 2 # local scope
    # r2py:entity:isolate_1
    isolate(local_update_y)
    # r2py:entity:print_1
# r2py:entity:print_1
    print(y) # 1

# Run the mocks to simulate R's behavior
observe_1()
observe_2()
observe_3()

# Can also use isolate to call reactive expressions from the R console
values = reactive.Value(1) # Using shiny.reactive.Value as equivalent to reactiveValues
# Note: R's reactiveValues is a list-like object. 
# To match values$A, we'll use a simple class or dict if needed, 
# but for the snippet, we just need a value.
# r2py:entity:values
class ReactiveValues:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
values = ReactiveValues(A=1)

# r2py:entity:fun
def fun():
    # r2py:entity:as.character
# r2py:entity:as.character
    return str(values.A)

# isolate(fun())
# r2py:entity:isolate_2
result = isolate(fun)
print(f'"{result}"') # "1"