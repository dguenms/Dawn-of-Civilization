#
# Roman Numbers
# version 0.9
# By: Sen2000
# 

from CvPythonExtensions import *

import sys
import math

gc = CyGlobalContext()

#Define exeptions
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass

#make a list of Roman numbers
RomanNumberMap = (('M', 1000),
                  ('CM', 900),
                  ('D',  500),
                  ('CD', 400),
                  ('C',  100),
                  ('XC',  90),
                  ('L',   50),
                  ('XL',  40),
                  ('X',   10),
                  ('IX',   9),
                  ('V',    5),
                  ('IV',   4),
                  ('I',    1))

# Makes the Number into RomsnNumber
def toRoman(Number):
    """convert integer to Roman numeral"""

    if not (0 < Number < 10000):
        raise OutOfRangeError, "number out of range (must be 1..9999)"
    
    Roman = ""
    for Romantext, integer in RomanNumberMap:
        while Number >= integer:
            Roman += Romantext
            Number -= integer
    return Roman
