# Simple program to generate a single image from a set of images with descriptions in the image

import os
import sys
import cv2
import numpy as np

# Get the list of files in the barcodes folder
files = os.listdir("barcodes")

number_barcode_images = len(files)
print(f"Found {number_barcode_images} barcode images")

# Create a new image with the correct size
output_barcode_width = 100 #px
output_barcode_height = 100 #px -- 20px for text
output_barcode_spacing = 100 #px -- how much padding will be between images
output_text_spacing = 100 #px -- how much padding will be for text

number_of_rows = 5 

# Calculate the number of columns
number_of_columns = int(number_barcode_images / number_of_rows)
if number_barcode_images % number_of_rows > 0:
    number_of_columns += 1



print(f"Number of columns: {number_of_columns}")
print(f"Number of rows: {number_of_rows}")

# Calculate the output image size
output_width = output_barcode_width * number_of_columns + (number_of_columns * output_barcode_spacing + 200)
output_height = output_barcode_height * number_of_rows + (number_of_rows * (output_barcode_spacing+20) * 2)

print(f"Output image size: {output_width}x{output_height}")

# Create the output image of output_width x output_height
output_image = np.zeros((output_height,output_width,3), np.uint8)

# Loop through the files and add them to the output image
current_row = 0
current_column = 0
for file in files:
    print(f"Processing {file}")
    # Load the image
    image = cv2.imread(f"barcodes/{file}")

    # Resize the image to the correct size
    image = cv2.resize(image, (output_barcode_width,output_barcode_height))

    # Get the description by taking everything after the first - 
    description = file[file.find("-")+1:]
    description = description.replace(".png", "")
    description = description.replace("_", " ")

    # Add the image to the output image
    x = current_column * output_barcode_width + (current_column * output_barcode_spacing) + output_barcode_spacing
    y = current_row * output_barcode_height + (current_row * output_barcode_spacing) + output_barcode_spacing
    if(current_row != 0):
        y += (output_text_spacing * current_row)

    
    #print(f"current_row: {current_row}, current_column: {current_column}, x: {x}, y: {y}")
    
    # print image details
    output_image[y:y+output_barcode_height,x:x+output_barcode_width] = image
    
    # Add the text to the output image
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255,255,255)
    lineType = 2
    lineHeight = 30

    # Lets line wrap the description text for the image
    words = description.split(" ")
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) > 10:
            lines.append(current_line)
            current_line = word
        else:
            current_line += " " + word
    lines.append(current_line)


    # Now we have the lines we can add them to the image
    for line in lines:
        textsize = cv2.getTextSize(line, font, fontScale, lineType)[0]
        textX = x + int((output_barcode_width - textsize[0]) / 2)
        textY = y + output_barcode_height + lineHeight + (lines.index(line) * lineHeight) + 10
        cv2.putText(output_image, line, (textX,textY), font, fontScale, fontColor, lineType)
    
    # Increment the current column
    current_column += 1

    # Check if we need to move to the next row
    if current_column >= number_of_columns:
        current_column = 0
        current_row += 1

# Save the output image
cv2.imwrite("single_image_of_all_barcodes.png", output_image)
