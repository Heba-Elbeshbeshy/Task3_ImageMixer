## enum for different operation modes

import enum

class Modes(enum.Enum):
    magAndPhase = "testMagAndPhaseMode"
    realAndImag = "testRealAndImagMode"
    magAndUniPhase = "testMagAndUniPhaseMode"
    phaseAndUniMag = "testPhaseAndUniMagMode"
    uniMagAndUniPhase = "testUniMagAndUniPhaseMode"
    uniMagAndPhase = "testUniMagAndPhase"
    uniPhaseAndMag = "testUniPhaseAndMag"

# How to use enum?
# Just type enumName.enumElement
# for example enum.magnitudeAndPhase or enum.realAndImaginary

# Why should we use enum instead of strings?
# Strings can be typed in different formats "lower, UPPER, camelCase, under_score" or spellings
# enum gives you the flexibilty to change the string to anything and no to ruin your program
# Try to change the value of any elemnt in enum and you'll find that the test still works, "I hope =D"
# You can assign integers, strings .... to your enum elements
