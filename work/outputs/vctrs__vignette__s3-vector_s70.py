# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import numpy as np
import pandas as pd
from plotnine import *
from shiny import App, ui, render

# r2py:entity:meter
class Meter:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Meter):
            return Meter(self.value + other.value)
        raise TypeError("Operands must both be Meter instances")

    def __sub__(self, other):
        if isinstance(other, Meter):
            return Meter(self.value - other.value)
        raise TypeError("Operands must both be Meter instances")

    def __truediv__(self, other):
        if isinstance(other, Meter):
            return self.value / other.value
        raise TypeError("Operands must both be Meter instances")

    def __mul__(self, other):
        raise TypeError("Multiplication of two Meters is incompatible")

    def __repr__(self):
        return f"Meter({self.value})"

# Test cases
try:
# r2py:entity:meter_1
    print(Meter(10) + Meter(1))
# r2py:entity:meter_3
    print(Meter(10) - Meter(1))
# r2py:entity:meter_5
    print(Meter(10) / Meter(1))
# r2py:entity:meter_7
    print(Meter(10) * Meter(1))
except TypeError as e:
    print(f"Error: {e}")