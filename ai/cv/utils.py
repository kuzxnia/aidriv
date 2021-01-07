import cv2
import numpy as np


def tresholding_otsu(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img_gray, (9, 9), 0)
    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)
    return mask


def tresholding_white_yellow(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    lower = np.uint8([0, 200, 0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    # yellow color mask
    lower = np.uint8([10, 0, 100])
    upper = np.uint8([40, 255, 255])
    yellow_mask = cv2.inRange(image, lower, upper)
    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    return mask


def wrapImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    if inv:
        pts1, pts2 = pts2, pts1
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWrap = cv2.warpPerspective(img, matrix, (w, h))
    return imgWrap


def empty(a):
    pass


def initializeTracebars(initializeTracbarVals, wT=320, hT=240):
    cv2.namedWindow('Trackbars')
    cv2.resizeWindow("Trackbars", wT , hT // 2)
    cv2.createTrackbar("Width Top", "Trackbars", initializeTracbarVals[0], wT // 2, empty)
    cv2.createTrackbar("Height Top", "Trackbars", initializeTracbarVals[1], hT, empty)
    cv2.createTrackbar("Width Bottom", "Trackbars", initializeTracbarVals[2], wT // 2, empty)
    cv2.createTrackbar("Height Bottom", "Trackbars", initializeTracbarVals[3], hT, empty)


def valTrackbars(wT=320, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")

    return calculate_points(wT, hT, widthTop, heightTop, widthBottom, heightBottom)


def calculate_points(wT=320, hT=240, *cords):
    widthTop, heightTop, widthBottom, heightBottom = cords

    return np.float32([
        (widthTop, heightTop), (wT - widthTop, heightTop), (widthBottom, heightBottom), (wT - widthBottom, heightBottom)
    ])


def drawPoints(img, points):
    for x in range(4):
        cv2.circle(
            img,
            (int(points[x][0]), int(points[x][1])),
            15,
            (0, 0, 255),
            cv2.FILLED
        )
    return img


def getHistogram(img, minPer=0.1, display=False, region=1):
    if region == 1:
        histValues = np.sum(img, axis=0)
    else:
        histValues = np.sum(img[img.shape[0] // region:, :], axis=0)

    maxValue = np.max(histValues)
    minValue = minPer * maxValue

    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))

    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(histValues):
            cv2.line(imgHist, (x, img.shape[0]), (x, img.shape[0] - int(intensity // 255 // region)), (255, 0, 255), 1)
            cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return basePoint, imgHist
    return basePoint


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


