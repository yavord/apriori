#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'fizzBuzz' function below.
#
# The function accepts INTEGER n as parameter.
#

def fizzBuzz(n):
    # Write your code here
    if n < 0 or n > (2*10^5):
        raise ValueError

    for i in range(1,n+1):
        out = ""
        
        if i % 3 == 0:
            out += "Fizz"
        if i % 5 == 0:
            out += "Buzz"
        if i % 5 > 0 and i % 3 > 0:
            out = i

        print(out)
    
if __name__ == '__main__':
    n = int(input().strip())

    fizzBuzz(n)
