#!/usr/bin/python3
# -*- coding: utf-8 -*-

# KLM Calculator Application
import sys

# Standard KLM Values
standardValues = {
    "k" : 0.28,
    "p" : 1.1,
    "b" : 0.1,
    "m" : 1.2,
    "h" : 0.4
}

# Building a string that contains all no-comment characters of the input file
def getOperatorString():
    operatorString = ""
    try:
        file = open(sys.argv[1])
        lines = file.readlines()
        for line in lines:
            for character in line:
                if character == "#":
                    break
                else:
                    operatorString += character
        return operatorString.replace(" ","").replace("\n","").lower()
    except IndexError:
        print("define a filename as argument");

#Computing duration based on the given character/value pairs
def getDuration(operatorString, values):
    duration = 0.0
    digit = ""
    for character in operatorString:
        # determine if multiplier is present
        if character.isdigit():
            digit += character
        else:
            try:
                if digit == "":
                    duration += values[character]
                else:
                    duration += int(digit) * values[character]
                    digit = ""
            except KeyError:
                print("ignoring illegal character '" + character + "' in input file...")
                pass
    return duration

# Compute duration
operatorString = getOperatorString()
duration = getDuration(operatorString, standardValues)

# Print out results
print(operatorString)
print(duration)
