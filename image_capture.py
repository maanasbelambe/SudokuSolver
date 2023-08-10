import cv2

def capture_image():
    video_capture = cv2.VideoCapture(0)

    cv2.namedWindow("Window")
    image_filename = "sudoku_board.jpg"

    while True:
        ret, frame = video_capture.read()
        #resized_frame = cv2.resize(frame, (frame.shape[1], frame.shape[1]))

        cv2.imshow("Window", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        if key == ord(' '):
            cv2.imwrite(image_filename, frame)
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return image_filename