# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import re

# Simulation of the .all_holidays internal dataset from timeDate
# Based on verification output, R's .all_holidays contains concatenated identifiers.
_all_holidays = [
    "Advent1st", "Advent2nd", "Advent3rd", "Advent4th", "AllSaints", "AllSouls", 
    "Annunciation", "Ascension", "AshWednesday", "AssumptionOfMary", 
    "BirthOfVirginMary", "BoxingDay", "CHAscension", "CHBerchtoldsDay", 
    "CHConfederationDay", "CHKnabenschiessen", "CHSechselaeuten", 
    "Easter", "EasterMonday", "EasterSunday", 
    "DENewYearsEve", "JPNewYearsDay", "NewYearsDay", "USNewYearsDay"
]

# r2py:entity:listHolidays
def listHolidays(pattern=".*"):
    # In R: if (pattern == "*") pattern = "\\*"
    # This handles the case where the user literally passes "*"
    if pattern == "*":
        pattern = r"\*"
    
    # R's grep returns indices of elements that match the pattern
    # we return the matching strings
    matches = [h for h in _all_holidays if re.search(pattern, h)]
    return matches

# Local Swiss Holidays:
# r2py:entity:listHolidays
print(listHolidays("CH"))

# r2py:entity:listHolidays_1
print(listHolidays("Easter"))
# r2py:entity:listHolidays_2
print(listHolidays("NewYear"))

# All Holidays
# r2py:entity:listHolidays_3
print(listHolidays())