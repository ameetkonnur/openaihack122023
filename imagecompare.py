import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the images
image1 = cv2.imread('image1.png')
image2 = cv2.imread('image2.png')

# Convert the images to grayscale
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Compute the absolute difference between the two images
diff = cv2.absdiff(gray1, gray2)

# Use a threshold to highlight the differences
_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

# Display the original images and the difference
plt.figure(figsize=(10,10))
plt.subplot(131), plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
plt.subplot(132), plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
plt.subplot(133), plt.imshow(thresh, cmap='gray'), plt.title('Differences')
plt.show()