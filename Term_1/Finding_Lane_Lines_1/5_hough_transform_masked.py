import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import sys

np.set_printoptions(threshold=np.nan)

try:
    image = mpimg.imread('test.jpg')
except FileNotFoundError as e:
    print(e)
    sys.exit(1)

gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # 8-bit image

kernel_size = 5  # should be odd numbers
blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

low_threshold = 50
high_threshold = 110
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

# Next we'll create a masked edges image using cv2.fillPoly()
mask = np.zeros_like(edges)
ignore_mask_color = 255

# This time we are defining a four sided polygon to mask
imshape = image.shape
# vertices = np.array([[(left_bottom_y, left_bottom_x), (400, 315), (500, 300), (imshape[1], imshape[0])]], dtype=np.int32)
vertices = np.array([[(50, imshape[0]), (400, 350), (600, 350), (imshape[1], imshape[0])]], dtype=np.int32)
poly = cv2.fillPoly(mask, vertices, ignore_mask_color)
masked_edges = cv2.bitwise_and(edges, poly)

# Parameters for Hough lines
rho = 1
theta = np.pi / 180
threshold = 1
min_line_length = 5
max_line_gap = 1
line_image = np.copy(image) * 0  # create a blank to draw the lines
# See http://docs.opencv.org/3.2.0/dd/d1a/group__imgproc__feature.html#ga8618180a5948286384e3b7ca02f6feeb
lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

# Iterate through the lines and draw a line
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

# Color binary image
color_edges = np.dstack((edges, edges, edges))

# Draw the lines on edge image
lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0)

# Draw the lines on original image
image_lines_edges = cv2.addWeighted(image, 0.8, line_image, 1, 0)

# show images
f = plt.figure()

f.add_subplot(3, 4, 1)
plt.imshow(image)
plt.title('Original image')

f.add_subplot(3, 4, 2)
plt.imshow(blur_gray, cmap='gray')
plt.title('Gaussian blurred gray image')

f.add_subplot(3, 4, 3)
plt.imshow(edges, cmap='Greys_r')
plt.title("Canny edges of Gaussian image")

f.add_subplot(3, 4, 4)
plt.imshow(poly, cmap='Greys_r')
plt.title("Raw mask")

f.add_subplot(3, 4, 5)
plt.imshow(masked_edges, cmap='gray')
plt.title("Masked edges of Hough lines")

f.add_subplot(3, 4, 6)
plt.imshow(lines_edges)
plt.title("Masked Hough transform")

f.add_subplot(3, 4, 7)
plt.imshow(image_lines_edges)
plt.title("Masked Hough transform on original image")

plt.show()
