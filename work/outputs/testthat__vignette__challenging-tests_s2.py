# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pytest
import random

# r2py:entity:dice
def dice():
    return random.randint(1, 6)

def test_dice_returns_different_numbers():
# r2py:entity:local_seed
    random.seed(1234)
    
# r2py:entity:expect_equal
    assert dice() == 4
# r2py:entity:expect_equal_1
    assert dice() == 2
# r2py:entity:expect_equal_2
    assert dice() == 6