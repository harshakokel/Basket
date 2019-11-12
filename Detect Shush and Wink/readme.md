#### Detect Shush and Wink

This project was done as part of CS 6384 at The University of Texas at Dallas in Spring 2017. Submitted by Harsha Kokel.  

The code is written in Python version 3.6.2.  

This project contains two programs to detect "winking" and the "shush" (silencing action)
expression.
In both cases the input to the program is either a live video feed or a folder containing images. In case of live video, the video feed will show either blue or green square around the detected face. Blue square indicates that the wink or shush is detected. Green square indicates that wink or shush is not detected. Red square will highlight the detected eye and mouth region in DetectWink and DetectShush respectively. In case folder of images is given as input, the images will be marked and stored in output folder.


#### Sample Usage DetectWink.py:
```python
python3 DetectWink.py    #Live Video
python3 DetectWink.py input/WinkImages/ output_folder  #Image Folder
```

#### Sample Usage DetectShush.py:
```python
python3 DetectWink.py    #Live Video
python3 DetectShush.py input/ShushImages/ output_folder #Image Folder
```

#### Notes

##### On wink detection

This program uses pre-trained haar cascade classifiers available in the OpenCV. The program first detects face using `"haarcascade_frontalface_default"` classifier and then use the area detected as face for detecting eye. To detect eye, this program makes use of multiple haar cascade classifiers. First it uses `"haarcascade_eye"` to detect eyes. If only one eye is identified, wink is detected. But the classifier can also identify more than 2 eyes in a face or no eyes. In case of no eyes, the program use `"haarcascade_eye_tree_eyeglasses"` classifier to identify eyes. Same as before, if only one eye is identified wink is detected. If there are more than 2 eyes, program finds the two detection in almost same y level and then uses `"haarcascade_lefteye_2splits"` and `"haarcascade_righteye_2splits"` to validate those eyes. If only one of them is identified as eye then wink is detected otherwise face is returned.


##### On shush detection

Similar to wink detection, this program only uses pre-trained haar cascade classifiers available open source. First it uses `"haarcascade_frontalface_default"` classifier  to detect the face, then uses `"mouth"` classifier [Castrillon07-jvci] available at http://alereimondo.no-ip.org/OpenCV/34 to detect mouth. If **no** mouth is identified it, detects shush. If mouth is identified, it marks red square around the mouth.

##### Voting

Pre-processing the image using MedianBlur, Histogram Equalization, Gaussian Blur helped improved detection for few images but it also decreased the detection accuracy for other images, So in this program I implemented a voting mechanism. I pre-process images in three different ways and run the detection algorithm. I then use the maximum vote to output the detection.  

Parameters used for each of these classifiers can be found in code.   

##### Reference
[Castrillon07-jvci] *Castrillón Santana, M. and Déniz Suárez, O. and Hernández Tejera, M. and Guerra Artal, C,*  **ENCARA2: Real-time Detection of Multiple Faces at Different Resolutions in Video Streams**, Journal of Visual Communication and Image Representation, 2007
