import numpy as np
import itertools
import cv2
from os import listdir, makedirs
from os.path import isfile, join, exists
import sys
import copy
from fileinput import filename

# load pre-trained cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades
                                     + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades
                                    + 'haarcascade_eye.xml')
glass_cascade = cv2.CascadeClassifier(cv2.data.haarcascades
                                      + 'haarcascade_eye_tree_eyeglasses.xml')
left_eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades
                                         + 'haarcascade_lefteye_2splits.xml')
right_eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades
                                          + 'haarcascade_righteye_2splits.xml')


def detectWink(frame, location, ROI):
    """Detect Wink in the frame."""
    eyes = eye_cascade.detectMultiScale(
        ROI, 1.1, 15, 0 | cv2.CASCADE_SCALE_IMAGE, (10, 20))
    i = 0
    eyes = merge_overlaps(eyes)
    if len(eyes) == 1:    # number of eyes is one
        x, y, w, h = eyes[0][0], eyes[0][1], eyes[0][2], eyes[0][3]
        x += location[0]
        y += location[1]
        highlight_eye(frame, x, y, h, w, (0, 0, 255))
        return True
    elif len(eyes) < 1:
        eyes = glass_cascade.detectMultiScale(ROI, 1.15, 2,
               0 | cv2.CASCADE_SCALE_IMAGE, (10, 20))
        eyes = merge_overlaps(eyes)
        for e in eyes:
            x, y, w, h = e[0]+location[0], e[1]+location[1], e[2], e[3]
            highlight_eye(frame, x, y, h, w, (0, 0, 255))
        if len(eyes) == 1:    # number of eyes is one
            return True
    if len(eyes) > 2:
        average = sum(eyes)/len(eyes)
        partition_upper = []
        partition_lower = []
        partition_right = []
        partition_left = []
        for e in eyes:
            if e[1] < average[1]:
                partition_upper += [e]
            else:
                partition_lower += [e]
            if e[0] < average[0]:
                partition_left += [e]
            else:
                partition_right += [e]
            # To be commented
            x, y, w, h = e[0]+location[0], e[1]+location[1], e[2], e[3]
            highlight_eye(frame, x, y, h, w, (0, 0, 255))
        if len(partition_upper) == 2:
            eyes = partition_upper
        elif len(partition_lower) == 2:
            eyes = partition_lower
        elif len(partition_right) == 2:
            eyes = partition_right
        elif len(partition_left) == 2:
            eyes = partition_left
    if len(eyes) == 2:
        left_eye = None
        left_x = 0
        for e in eyes:
            if left_x < e[0]:
                left_x = e[0]
                left_eye = e
        x, y, w, h = left_eye[0], left_eye[1], left_eye[2], left_eye[3]
        leftROI = ROI[y-10:y+h+10, x-10:x+w+10]
        left_eye = left_eye_cascade.detectMultiScale(leftROI, 1.15, 3,
                   0 | cv2.CASCADE_SCALE_IMAGE, (10, 20))
        if len(left_eye) < 1:
            left_eye = right_eye_cascade.detectMultiScale(leftROI, 1.15, 3,
                       0 | cv2.CASCADE_SCALE_IMAGE, (10, 20))
        x += location[0]
        y += location[1]
        if len(left_eye) > 0:
            highlight_eye(frame, x, y, h, w, (0, 0, 255))
        right_eye = None
        right_x = len(ROI[0])
        for e in eyes:
            if right_x > e[0]:
                right_x = e[0]
                right_eye = e
        x, y, w, h = right_eye[0], right_eye[1], right_eye[2], right_eye[3]
        rightROI = ROI[y-10:y+h+10, x-10:x+w+10]
        right_eye = right_eye_cascade.detectMultiScale(rightROI, 1.15, 3,
                    0 | cv2.CASCADE_SCALE_IMAGE, (10, 20))
        if len(right_eye) < 1:
            right_eye = left_eye_cascade.detectMultiScale(rightROI, 1.15, 3,
                        0 | cv2.CASCADE_SCALE_IMAGE, (10, 20))
        x += location[0]
        y += location[1]
        if len(right_eye) > 0:
            highlight_eye(frame, x, y, h, w, (0, 0, 255))
        if len(left_eye) + len(right_eye) == 1:
            return True
    if len(eyes) < 1:
        ROI = ROI[0:int(len(ROI)*4/5), 0:len(ROI[0])]
        eyes = eye_cascade.detectMultiScale(
            ROI, 1.05, 2, 0 | cv2.CASCADE_SCALE_IMAGE, (5, 10))
        eyes = merge_overlaps(eyes)
        for e in eyes:
            x, y, w, h = e[0]+location[0], e[1]+location[1], e[2], e[3]
            highlight_eye(frame, x, y, h, w, (0, 0, 255))
        if len(eyes) == 1:
            return True
    return False


def highlight_eye(frame, x,y,h,w, color):
    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)


def detect(frame, preprocessing_option):
    """Detect Wink in the frame."""
    gray_frame = preprocessing_image(frame, preprocessing_option)
    scaleFactor = 1.1  # range is from 1 to ..
    minNeighbors = 10   # range is from 0 to ..
    flag = 0 | cv2.CASCADE_SCALE_IMAGE  # either 0 or 0|cv2.CASCADE_SCALE_IMAGE
    minSize = (30, 30)  # range is from (0,0) to ..
    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor,
        minNeighbors,
        flag,
        minSize)
    if len(faces) == 0:
         faces = face_cascade.detectMultiScale(
             gray_frame,
             scaleFactor,
             5,
             flag,
             minSize)
    detected = 0
    faces = merge_overlaps(faces)
    for f in faces:
        x, y, w, h = f[0], f[1], f[2], f[3]
        faceROI = gray_frame[y:y+h, x:x+w]
        if detectWink(frame, (x, y), faceROI):
            detected += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return detected


def preprocessing_image(frame, option):
    """Run pre processing on the image."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if option == 1:
        gray_frame = cv2.equalizeHist(gray_frame)
    elif option == 2:
        gray_frame = cv2.equalizeHist(gray_frame)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 2.5)
    elif option == 3:
        gray_frame = cv2.equalizeHist(gray_frame)
        gray_frame = cv2.medianBlur(gray_frame, 5)
    return gray_frame


def merge_overlaps(objects):
    """Merge overlapping object detections."""
    overlap = True
    new_objects = []
    while True:
        if len(objects) <= 1:
            break
        for a, b in list(itertools.product(objects, objects)):
            if np.array_equal(a, b):
                continue
            else:
                if check_overlap(a[0], a[1], a[0]+a[2], a[1]+a[3], b[0],
                                 b[1], b[0]+b[2], b[1]+b[3]):
                    new_objects = [x for x in objects if not
                                   (np.array_equal(b, x) or
                                    np.array_equal(a, x))]
                    new_objects += [[min(a[0], b[0]), min(a[1], b[1]), max(a[0]
                                     + a[2], b[0]+b[2])-min(a[0], b[0]), max(
                                     a[1]+a[3], b[1]+b[3])-min(a[1], b[1])]]
                    objects = new_objects
                    break
            overlap = False
        if not overlap:
            break
    return objects


def check_overlap(l1_x, l1_y, r1_x, r1_y, l2_x, l2_y, r2_x, r2_y):
    """Check if two rectangles overlap."""
#      If one rectangle is on total left side of other
    if bool(l1_x > r2_x) ^ bool(l2_x > r1_x):
        return False
#      If one rectangle is above other
    if bool(l1_y < r2_y) ^ bool(l2_y < r1_y):
        return False
    return True


def run_on_folder(folder, output):
    """Detect Winks on all images in the folder."""
    if(folder[-1] != "/"):
        folder = folder + "/"
    files = [join(folder, f) for f in listdir(folder)
             if isfile(join(folder, f))]
    if not exists(output+"/"):
        makedirs(output+"/")
        makedirs(output+"/extra/0/")
        makedirs(output+"/extra/1/")
        makedirs(output+"/extra/2/")
        makedirs(output+"/extra/3/")   
    print("Total images: ", len(files))
    totalCount = 0
    for f in files:
        img = cv2.imread(f, 1)
        if type(img) is np.ndarray:
            img_arr = [copy.deepcopy(img), copy.deepcopy(img), copy.deepcopy(img)] 
            wink = [0, 0, 0]
            filename = f.split("/")[-1] 
            for option in [0, 1, 2]:
                wink[option] = detect(img_arr[option], option)
                cv2.imwrite(output+"/extra/"+str(option)+"/"+filename, img_arr[option])
            cnt = max(set(wink), key=wink.count)
            img_out = img_arr[wink.index(cnt)]
            cv2.imwrite(output+"/"+filename, img_out)
            totalCount += cnt
    print(" Total winks detected  ", totalCount)
    return totalCount


def runonVideo():
    """Detect Winks in the video."""
    videocapture = cv2.VideoCapture(0)
    if not videocapture.isOpened():
        print("Can't open default video camera!")
        exit()

    windowName = "Live Video"
    showlive = True
    while(showlive):
        ret, frame = videocapture.read()

        if not ret:
            print("Can't capture frame")
            exit()

        detect(frame, 2)
        cv2.imshow(windowName, frame)
        if cv2.waitKey(30) >= 0:
            showlive = False

    # outside the while loop
    videocapture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # check command line arguments: nothing or an input & output folderpath
    if len(sys.argv) != 1 and len(sys.argv) != 3:
        print(sys.argv[0] + ": got " + str(len(sys.argv) - 1)
              + "arguments. Expecting 0 or 2:[image-folder] [output-folder]")
        exit()

    if(len(sys.argv) == 3): # one argument
        folderName = sys.argv[1]
        outputFolder = sys.argv[2]
        detections = run_on_folder(folderName, outputFolder)
        print("Total of ", detections, "detections")
    else: # no arguments
        runonVideo()
