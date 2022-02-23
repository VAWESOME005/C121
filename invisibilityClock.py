import cv2
import time
import numpy as np


# passing the code XVID to create our output as a video with the extension AVI
# to create .mp4 use code as 'm', 'p', '4', 'v'

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')

#parameters in order - "name", "extension", 'fps', and 'window size'

# output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
output_file = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480))

#starts the primary camera (because of 0)
cap = cv2.VideoCapture(0)

# make the code sleep for 2 seconds
time.sleep(2)

bg = 0

for i in range(60):
    ret, bg = cap.read()

#flipping the image along y-axis (axis = 1) as camera creates mirror image (use 0 for horizontal)
bg = np.flip(bg, axis = 1)

while (cap.isOpened()):
    ret, img = cap.read()
    if not ret :
        break
    #to keep image consistent
    img = np.flip(img, axis = 1)
    # converting image from BGR to HSV - hue = color, saturation = purity, value = brightness
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #generating masks to detect the red color - later removing it from the image and showing the background instead
    lower_red = np.array([0,120,50])
    upper_red = np.array([10, 255, 255])

    # used to determine if the elements of the image land between the lower and upper "boundary"
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])

    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2

    #morphology algos removes any unneccesary details such as small black pixels and white boundaries/regions

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8()))

    #selecting only the mask that doesn't have the red color and saving it in mask 2

    mask_2 = cv2.bitwise_not(mask_1)

    #keeping only the part of the images without the red color in result 1

    res_1 = cv2.bitwise_and(img, img, mask = mask_2)

    #bringing the bg image where mask 1 (red) is present

    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)

    # merging both results using addWeighted function

    # paramters - first result, transparency, 2nd result, translucency, gamma (alpha, beta, gamma)
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)

    output_file.write(final_output)

    cv2.imshow('C121', final_output)
    # to display the video - paramter has to be greater than 0 - 0 will display still imgs
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

