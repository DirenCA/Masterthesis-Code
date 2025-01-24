import numpy
import numpy as np
import cv2 as cv
import glob


def get_camera_intrinsics(images):
    # Entferne die 'check'-Bedingung oder setze sie korrekt
    # (Hier entfernt, da sie den Ablauf blockiert)

    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((10 * 7, 3), np.float32)  # Werte nach Schachbrettmuster ändern
    objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2)  # Werte nach Schachbrettmuster ändern

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    for fname in images:
        img = cv.imread(fname)
        img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (10, 7), None)  # Original 7x6

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            cv.drawChessboardCorners(img, (10, 7), corners2, ret)  # Werte nach Schachbrettmuster ändern
            cv.imshow("img", img)
            cv.waitKey(1)

    cv.destroyAllWindows()

    # Kamerakalibrierung
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Berechnung der Reprojection-Error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        mean_error += error

    reprojection_error = mean_error / len(objpoints)

    return ret, mtx, dist, rvecs, tvecs, reprojection_error

# #------------------Entzerrung------------------
# img = cv.imread(r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\IPhoneTiefenkarten\IMG_8350_DepthMap.jpg")
# h,  w = img.shape[:2]
# newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
#
#
# # undistort
# mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
# dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
#
# # crop the image
# # x, y, w, h = roi
# # dst = dst[y:y+h, x:x+w]
# cv.imwrite(r"C:\Users\Diren\Nextcloud\HTW\4.Semester-Masterarbeit\Masterarbeit\Code\calibresultdepth.png", dst)