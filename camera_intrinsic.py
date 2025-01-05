import numpy
import numpy as np
import cv2 as cv
import glob

check = False

if not check:
    # images = glob.glob(r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\Chesspattern\OpenCV/*.jpg") #Quelle der Daten: https://github.com/opencv/opencv/tree/05b15943d6a42c99e5f921b7dbaa8323f3c042c6/samples/data
    images = glob.glob(r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\Chesspattern\My/*.jpg")

    # Quelle: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((5 * 3, 3), np.float32)
    objp[:, :2] = np.mgrid[0:5, 0:3].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    for fname in images:
        img = cv.imread(fname)
        img = cv.rotate(img,
                        cv.ROTATE_90_COUNTERCLOCKWISE)  # Quelle: https://github.com/nkmk/python-snippets/blob/addd28bee31e97b299383a57ffbddba49e03794c/notebook/opencv_rotate.py#L1-L20
        img = cv.resize(img, (640, 480))
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (5, 3), None)  # original 7 ,6

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            cv.drawChessboardCorners(img, (5, 3), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)

    cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # mtx =numpy.asarray(mtx)
    check = True
    print(mtx)
else:
    pass
