#### Luv Manipulation of Images

This project was done as part of CS 6384 at The University of Texas at Dallas in Spring 2017. Submitted by Harsha Kokel.  

The code is written in Python version 3.6.2.  

This program performs two operations:
**Linear Scaling** and **Histogram equalization**.   

Both these operations are performed in Luv domain with the L values alone. To achieve this, the program first change the color image in sRGB domain to Luv domain performs operation and converts it back to the sRGB domain.

The operations are performed based on the histogram computed from a specific window of the image. The window is specified in terms of the normalized coordinates w1 h1 w2 h2, where the window's upper left point is (w1,h1), and its lower right point is (w2,h2). For example, w1=0, h1=0, w2=1, h2=1 is the entire image, and w1=0.3, h1=0.3, w2=0.7, h2=0.7 is window in the center of the image.

This program takes 7 arguments:  
*operation*       :  operation you want to perform
 '**s**' for Linear Scaling and '**e**' for histogram equalization.  
*w1*    :   X axis upper left corner  
*h1*    :   Y axis upper left corner  
*w2*    :   X axis lower right corner  
*h2*    :   Y axis lower right corner  
*ImageIn*   : path of input image  
*ImageOut*  : path and name of output image

#### Sample Usage Linear Scaling:
```python
python3 project1.py s 0 0 0.2 0.2 img/Lenna.png scaling/Lenna.png
```

#### Sample Usage Histogram Equalization:
```python
python3 project1.py e 0 0 0.2 0.2 img/Lenna.png equalization/Lenna.png
```

#### Notes  
While converting the images across domains following rules were used.

* While converting XYZ to Luv, if d = 0 then u_prime = 0, v_prime = 0  
* While converting Luv to XYZ, if L = 0 then u_prime & v_prime = 0
* While converting Luv to XYZ, if v_prime = 0 then X, Y, & Z = 0
* In histogram equalization, We requires a discretization step where the real-valued L is discretized
into 101 values to compute histogram. To discretize this I round off to nearest integer.  
* While converting linear RGB to non linear RGB, if RGB values are out of [0, 1] range then they are replaced with 0 or 1.  

#### Observations

* It appears that equalization is much more uniform than the linear scaling. If the window provided for the linear scaling is very bright, the shadowed/darker areas in the original image go totally black. For example. See abhinav.jpg, 4.1.08.tiff in linear scaling 00_02.
* We get lot of fireflies for the extreme points after linear scaling.
