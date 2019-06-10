#!/usr/bin/python3
# -*- coding: utf-8 -*-

# KLM Calculator Application
import sys

standardValues = {
    "k" : 0.28,
    "p" : 1.1,
    "b" : 0.1,
    "m" : 1.2,
    "h" : 0.4
}

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
        return operatorString.replace(" ","").lower()
    except IndexError:
        print("define a filename as argument");

def getDuration(operatorString, values):
    duration = 0.0
    digit = ""
    for character in operatorString:
        if character.isdigit():
            digit += character
        else:
            try:
                if digit == "":
                    duration += values[character]
                else:
                    duration += int(digit) * values[character]
                    digit = ""
            except IndexError:
                print("illegal character " + character + " in input file")
                pass
    return duration

                
            
        

operatorString = getOperatorString()

duration = getDuration(operatorString, standardValues)

print(operatorString)

print(duration)