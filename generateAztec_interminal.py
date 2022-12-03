from aztec_code_generator import AztecCode
from itertools import product
import string
import time
import sys
# Generate all two letter combinations of the alphabet
# and store them in a list
alphabet = list(product(string.ascii_uppercase, repeat=2))
prefix = ""
if(len(sys.argv) > 1):
    prefix = sys.argv[1]
else:
    alphabet = list(product(string.ascii_uppercase, repeat=4))
    
numLoops = 0
for i in alphabet:
    # Generate Aztec Code
    if(len(i) == 2):
        code = prefix + "_"+ '' .join(i)
    else:
        # Join the first two characters of the alphabet with a dash and then the second two characters
        code = i[0] + i[1] + "_" + i[2] + i[3]
    print(code)
    aztec_code = AztecCode(code)
    aztec_code.print_fancy()
    if(numLoops % 10 == 0):
        time.sleep(0.2)
    numLoops += 1