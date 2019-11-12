import numpy as np
import sys
import cv2
import math
from collections import defaultdict

if(len(sys.argv) != 8):
    print(sys.argv[0], ": takes 7 arguments. Not ", len(sys.argv)-1)
    print("Expecting arguments: operation w1 h1 w2 h2 ImageIn ImageOut.")
    print("Example:", sys.argv[0], "e 0.2 0.1 0.8 0.5 fruits.jpg out.png")
    sys.exit()

operation = sys.argv[1]
w1 = float(sys.argv[2])
h1 = float(sys.argv[3])
w2 = float(sys.argv[4])
h2 = float(sys.argv[5])
name_input = sys.argv[6]
name_output = sys.argv[7]

if(w1 < 0 or h1 < 0 or w2 <= w1 or h2 <= h1 or w2 > 1 or h2 > 1) :
    print(" arguments must satisfy 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1")
    sys.exit()

inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
if(inputImage is None):
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

rows, cols, bands = inputImage.shape  # bands == 3
W1 = round(w1*(cols-1))
H1 = round(h1*(rows-1))
W2 = round(w2*(cols-1))
H2 = round(h2*(rows-1))


def gamma(v):
    if v < 0.00304:
        return v * 12.92
    else:
        return ((1.055*math.pow(v, 1/2.4)) - 0.055)


def invgamma(v):
    if v < 0.03928:
        return v/float(12.92)
    else:
        v = (v+0.055)/float(1.055)
        return math.pow(v, 2.4)


linear_transform = [[0.412453, 0.35758, 0.180423],
                    [0.212671, 0.71516, 0.072169],
                    [0.019334, 0.119193, 0.950227]]

linear_transform_2 = [[3.240479, -1.53715, -0.498535],
                      [-0.969256, 1.875991, 0.041556],
                      [0.055648, -0.204043, 1.057311]]

X_w, Y_w, Z_w = 0.95, 1.0, 1.09
u_w = (4*X_w)/(X_w + 15*Y_w + 3*Z_w)
v_w = (9*Y_w)/(X_w + 15*Y_w + 3*Z_w)


# Converts XYZ to Luv
def XYZ_to_Luv(X, Y, Z):
    t = Y / Y_w
    L = 0
    if t > 0.008856:
        L = 116 * math.pow(t, 1/3) - 16
    else:
        L = 903.3 * t
    d = X + 15*Y + 3*Z
    u_prime, v_prime = 0, 0
    if d != 0:
        u_prime = (4 * X)/d
        v_prime = (9 * Y)/d
    u = 13*L*(u_prime - u_w)
    v = 13*L*(v_prime - v_w)
    return L, u, v


# Converts Luv to XYZ
def Luv_to_XYZ(L, u, v):
    u_prime, v_prime = 0, 0
    if L != 0:
        u_prime = (u + (13 * u_w * L))/(13*L)
        v_prime = (v + (13 * v_w * L))/(13*L)
    Y = 0
    if L > 7.9996:
        temp = (L + 16)/116
        Y = Y_w * math.pow(temp, 3)
    else:
        Y = (L/903.3) * Y_w
    X = 0
    Z = 0
    if v_prime != 0:
        X = Y * 2.25 * (u_prime/v_prime)
        Z = (Y * (3 - (0.75 * u_prime) - (5*v_prime)))/v_prime
    return X, Y, Z


Luv = np.zeros([rows, cols, bands], dtype=np.float64)

for i in range(0, rows):
    for j in range(0, cols):
        b, g, r = inputImage[i, j]
        # Convert sRGB to non-linear RGB by diving 255.
        # Convert non-linear RGB to linear RGB by invgamma.
        b_l = invgamma(b/float(255))
        g_l = invgamma(g/float(255))
        r_l = invgamma(r/float(255))
        # Convert linear RGB to XYZ
        x,y,z = np.matmul(linear_transform, [r_l, g_l, b_l])
        #Convert XYZ to Luv
        Luv[i, j] = np.array(XYZ_to_Luv(x,y,z))


output_Luv = np.zeros([rows, cols, bands], dtype=np.float64)
if operation == "s":
    # The stretching should be based on the
    # L values of the pixels in the W1,W2,H1,H2 range.
    # The following code goes over these pixels
    L_min = 100
    L_max = 0
    for i in range(H1, H2):
        for j in range(W1, W2):
            L, u, v = Luv[i, j]
            if L_min > L:
                L_min = L
            if L_max < L:
                L_max = L

    # Now we stretch the Luv image so that all L <= L_min becomes 0
    # and all L >= L_max = 100
    for i in range(0, rows):
        for j in range(0, cols):
            L, u, v = Luv[i, j]
            L_new = 0
            if L <= L_min:
                L_new = 0
            elif L >= L_max:
                L_new = 100
            else:
                L_new = ((L - L_min)*(100))/(L_max - L_min)
            output_Luv[i, j] = [L_new, u, v]
elif operation == "e":
    histogram = defaultdict(int) # Initalize all value to 0
    L_min = 100
    L_max = 0
    # Compute the histogram
    for i in range(H1, H2):
        for j in range(W1, W2):
            L, u, v = Luv[i, j]
            L = int(round(L))
            histogram[L] += 1
            if L_min > L:
                L_min = L
            if L_max < L:
                L_max = L
    f = defaultdict(int)  # Initalize all value to 0
    e = defaultdict(int)  # Initalize all value to 0
    total_count = (H2 - H1)*(W2 - W1)
    # Compute the equalizations
    for i in range(L_min, L_max+1):
        f[i] = histogram[i] + f[i-1]
        e[i] = math.floor(((f[i-1] + f[i])/2) * (101/total_count))
        # print(i, "->", e[i])
    # Equalize the image
    for i in range(0, rows):
        for j in range(0, cols):
            L, u, v = Luv[i, j]
            L = int(round(L))
            L_new = 0
            if L <= L_min:
                L_new = 0
            elif L >= L_max:
                L_new = 100
            else:
                L_new = e[L]
            output_Luv[i, j] = [L_new, u, v]

XYZ = np.zeros([rows, cols, bands], dtype=np.float64)

outputImage = np.zeros([rows, cols, bands], dtype=np.uint8)

for i in range(0, rows):
    for j in range(0, cols):
        L, u, v = output_Luv[i, j]
        # Convert stretched Luv back to XYZ
        X, Y, Z = Luv_to_XYZ(L,u,v)
        # Convert linear XYZ to Linear RGB
        r_l, g_l, b_l = np.matmul(linear_transform_2, [X, Y, Z])
        # Convert linear RGB to non Linear RGB
        if r_l > 1:
            r_l = 1
        if g_l > 1:
            g_l = 1
        if b_l > 1:
            b_l = 1
        if r_l < 0:
            r_l = 0
        if g_l < 0:
            g_l = 0
        if b_l < 0:
            b_l = 0
        r_nl = gamma(r_l)
        g_nl = gamma(g_l)
        b_nl = gamma(b_l)
        XYZ[i,j] = [r_nl, g_nl, b_nl ]
        # Convert non Linear RGB to sRGB
        r, g, b = r_nl*255, g_nl*255, b_nl*255
        outputImage[i, j] = [b, g, r]


cv2.imwrite(name_output, outputImage)
