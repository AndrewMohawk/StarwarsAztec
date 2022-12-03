import os
import zxing 

DIR = "../seen_codes/seen_aztec_codes/"
# list all files in the directory and try decode them
for filename in os.listdir(DIR):
    if filename.endswith(".jpg"): 
        print(filename)
        try:
            # decode the file
            reader = zxing.BarCodeReader()
            result = reader.decode(DIR + filename)
            print(result.parsed)
        except Exception as e:
            print(e)