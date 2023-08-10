from image_capture import *
import cv2
import numpy as np

def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return threshold

def find_contours(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #loop through contours to find rectangular one => should fix inconsistencies
    sudoku_contour = max(contours, key=cv2.contourArea)
    epsilon = 0.1 * cv2.arcLength(sudoku_contour, True)
    sudoku_approx = cv2.approxPolyDP(sudoku_contour, epsilon, True)
    return sudoku_approx

def perspective_transform(image, points):
    target = np.float32([[0, 0], [0, 450], [450, 450], [450, 0]])
    transform_matrix = cv2.getPerspectiveTransform(points.astype(np.float32), target)
    transformed = cv2.warpPerspective(image, transform_matrix, (450, 450))
    return transformed

image_filename = capture_image()
image = cv2.imread(image_filename)
preprocess = preprocess(image)

sudoku_contour = find_contours(preprocess)

if sudoku_contour.shape[0] != 4:
    raise ValueError("Sudoku contour is not a quadrilateral with 4 points.")

sudoku_board = perspective_transform(image, sudoku_contour.reshape(4, 2))

cv2.imshow("Original Image", image)
cv2.imshow("Preprocessed Image", preprocess)
cv2.imshow("Sudoku Board", sudoku_board)
cv2.waitKey(0)
cv2.destroyAllWindows()
