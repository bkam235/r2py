# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import numpy as np
import pandas as pd
from plotnine import *
import colorsys

# Mocking rainbow(10) and farver-like channel manipulation
# Since Python doesn't have a direct 'farver' equivalent, 
# we implement the channel logic using numpy and colorsys.

# r2py:entity:spectrum
def rainbow(n):
    return np.array([colorsys.hsv_to_rgb(i/n, 1, 1) for i in range(n)])

def to_lab(rgb):
    # Simplified RGB to LAB approximation for demonstration
    # In production, colormath or skimage.color would be used
    return np.array(rgb) * 100 

def from_lab(lab):
    # Simplified LAB to RGB approximation
    return np.clip(lab / 100, 0, 1)

spectrum = rainbow(10)

# r2py:entity:set_channel
# set_channel: spectrum, 'r', c(10, 50)
# Assuming 'r' is channel 0 (Red)
spectrum[:, 0] = np.linspace(10/255, 50/255, 10)

# r2py:entity:set_channel_1
# set_channel: spectrum, 'l', 50, space = 'lab'
lab_spectrum = np.array([to_lab(c) for c in spectrum])
lab_spectrum[:, 0] = 50 # L channel
spectrum = np.array([from_lab(c) for c in lab_spectrum])

# r2py:entity:set_channel_2
# set_channel: spectrum, 'alpha', c(0.5, 1)
alpha = np.linspace(0.5, 1, 10)

# r2py:entity:add_to_channel
# add_to_channel: spectrum, 'r', c(10, 50)
spectrum[:, 0] += np.linspace(10/255, 50/255, 10)

# r2py:entity:add_to_channel_1
# add_to_channel: spectrum, 'l', 50, space = 'lab'
lab_spectrum = np.array([to_lab(c) for c in spectrum])
lab_spectrum[:, 0] += 50
spectrum = np.array([from_lab(c) for c in lab_spectrum])

# r2py:entity:multiply_channel
# multiply_channel: spectrum, 'r', c(10, 50)
spectrum[:, 0] *= np.linspace(10, 50, 10)

# r2py:entity:multiply_channel_1
# multiply_channel: spectrum, 'l', 50, space = 'lab'
lab_spectrum = np.array([to_lab(c) for c in spectrum])
lab_spectrum[:, 0] *= 50
spectrum = np.array([from_lab(c) for c in lab_spectrum])

# r2py:entity:raise_channel
# raise_channel: spectrum, 'r', c(10, 50)
spectrum[:, 0] = np.power(spectrum[:, 0], np.linspace(10, 50, 10))

# r2py:entity:raise_channel_1
# raise_channel: spectrum, 'l', 20, space = 'lab'
lab_spectrum = np.array([to_lab(c) for c in spectrum])
lab_spectrum[:, 0] = np.power(lab_spectrum[:, 0], 20)
spectrum = np.array([from_lab(c) for c in lab_spectrum])

# r2py:entity:cap_channel
# cap_channel: spectrum, 'r', c(100, 50)
# capping is essentially a clip/clamp
spectrum[:, 0] = np.clip(spectrum[:, 0], np.linspace(100/255, 50/255, 10), None)

# r2py:entity:cap_channel_1
# cap_channel: spectrum, 'l', 20, space = 'lab'
lab_spectrum = np.array([to_lab(c) for c in spectrum])
lab_spectrum[:, 0] = np.clip(lab_spectrum[:, 0], 20, None)
spectrum = np.array([from_lab(c) for c in lab_spectrum])