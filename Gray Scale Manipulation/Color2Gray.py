import cv2
import numpy as np
import sys

# Check for 3 arguments
if(len(sys.argv) != 4) :
    print(sys.argv[0], ": takes 3 arguments. Not ", len(sys.argv)-1)
    sys.exit()

name_input = sys.argv[1]
conversion_method = sys.argv[2]
name_output = sys.argv[3]

def use_green(r, g, b):
    return g

def max_of_rgb(r, g, b):
    return max(r, g, b)

def average_of_rgb(r, g, b):
    return round((int(r) + int(g)+ int(b))/3.0)

def weighted_rgb(r,g,b):
    return round((0.3*r)+(0.6*g)+(0.1*b))


options = {'0': use_green,
           '1': max_of_rgb,
           '2': average_of_rgb,
           '3': weighted_rgb}
#Read input image
image_input = cv2.imread(name_input, cv2.IMREAD_UNCHANGED);
if(image_input is None) :
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()
cv2.imshow('original image', image_input);

# Check for color image
if(len(image_input.shape) != 3 or image_input.shape[2] != 3) :
    print(sys.argv[0], ": not a standard color image: ", name_input)
    sys.exit()

rows, cols, bands = image_input.shape # bands == 3
image_output = np.zeros([rows, cols, bands], dtype=np.uint8)

# this is slow but we are not concerned with speed here
for i in range(0, rows) :
    for j in range(0, cols) :
        b, g, r = image_input[i, j]
        image_output[i,j] = options[conversion_method](r, g, b)

cv2.imshow('output image', image_output);
cv2.imwrite(name_output, image_output);



# wait for key to exit

cv2.waitKey(0)
cv2.destroyAllWindows()
