from image_capture import *
import cv2
import numpy as np
import imutils

def perspective_transform(image, points):
    target = np.float32([[0, 0], [0, 450], [450, 450], [450, 0]])
    transform_matrix = cv2.getPerspectiveTransform(points.astype(np.float32), target)
    transformed = cv2.warpPerspective(image, transform_matrix, (450, 450))
    return transformed

def preprocess_find_board(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edged = cv2.Canny(bfilter, 30, 180)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contoured_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)
    cv2.imshow("Contours", contoured_image)

    sudoku_approx = None
    largest_area = 0

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        if len(approx) == 4:
            area = cv2.contourArea(contour)
            if area > largest_area:
                sudoku_approx = approx
                largest_area = area
    return perspective_transform(image, sudoku_approx)

image_filename = capture_image()
image = cv2.imread(image_filename)
result = preprocess_find_board(image)
cv2.imshow("Board", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
