# Grayscale Manipulation

### 1. Negative images
Create the negative image for a given image.

Code converts a color image to gray level image and then saves the negative of gray image in the output file.  
Code waits for interruption after displaying the input image, gray level image and the negative image.
In case the input image is gray level, it doesn't convert the image.

Usage:

```python3
python3 NegativeImages.py input_file output_file
```

### 2. Gray scale conversion

Code converts a color image to gray level image according to the 'conversion-option' mentioned in argument 2.

Conversion-option    
0  : y = g  
1  : y = max {r, g, b}  
2  : y = round( (r + g + b)/ 3.0 )  
3  : y = round( 0.3r + 0.6g + 0.1b )  

Code waits for interruption after displaying the original image and the output image.

Usage:   

```python3
python3 Color2Gray.py input_file conversion-option output_file
```

After testing it with multiple images, I believe last two methods (option 2 & 3) give almost same results for most of the pictures but for few last method out performs all others.
