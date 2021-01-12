import cv2
import numpy as np
import imutils


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


def preprocess_image(image):
    image = constrastLimit(image)
    image = LaplacianOfGaussian(image)
    image = binarization(image)
    return image


### Preprocess image
def constrastLimit(image):
    img_hist_equalized = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    channels = cv2.split(img_hist_equalized)
    channels[0] = cv2.equalizeHist(channels[0])
    img_hist_equalized = cv2.merge(channels)
    img_hist_equalized = cv2.cvtColor(img_hist_equalized, cv2.COLOR_YCrCb2BGR)
    return img_hist_equalized


def LaplacianOfGaussian(image):
    LoG_image = cv2.GaussianBlur(image, (3, 3), 0)  # paramter
    gray = cv2.cvtColor(LoG_image, cv2.COLOR_BGR2GRAY)
    LoG_image = cv2.Laplacian(gray, cv2.CV_8U, 3, 3, 2)  # parameter
    LoG_image = cv2.convertScaleAbs(LoG_image)
    return LoG_image


def binarization(image):
    thresh = cv2.threshold(image, 32, 255, cv2.THRESH_BINARY)[1]
    # thresh = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    return thresh


# Find Signs
def removeSmallComponents(image, threshold):
    # find all your connected components (white blobs in your image)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
    sizes = stats[1:, -1]
    nb_components = nb_components - 1

    img2 = np.zeros((output.shape), dtype=np.uint8)
    # for every component in the image, you keep it only if it's above threshold
    for i in range(0, nb_components):
        if sizes[i] >= threshold:
            img2[output == i + 1] = 255
    return img2


def findContour(image):
    # find contours in the thresholded image
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts


def contourIsSign(perimeter, centroid, threshold):
    result = []
    for p in perimeter:
        p = p[0]
        distance = sqrt((p[0] - centroid[0]) ** 2 + (p[1] - centroid[1]) ** 2)
        result.append(distance)
    max_value = max(result)
    signature = [float(dist) / max_value for dist in result]
    # Check signature of contour
    temp = sum((1 - s) for s in signature)
    temp = temp / len(signature)
    if temp < threshold:  # is  the sign
        return True, max_value + 2
    else:  # is not the sign
        return False, max_value + 2


# crop sign
def cropContour(image, center, max_distance):
    width = image.shape[1]
    height = image.shape[0]
    top = max([int(center[0] - max_distance), 0])
    bottom = min([int(center[0] + max_distance + 1), height - 1])
    left = max([int(center[1] - max_distance), 0])
    right = min([int(center[1] + max_distance + 1), width - 1])
    print(left, right, top, bottom)
    return image[left:right, top:bottom]


def cropSign(image, coordinate):
    width = image.shape[1]
    height = image.shape[0]
    top = max([int(coordinate[0][1]), 0])
    bottom = min([int(coordinate[1][1]), height - 1])
    left = max([int(coordinate[0][0]), 0])
    right = min([int(coordinate[1][0]), width - 1])
    return image[top:bottom, left:right]


def findLargestSign(image, contours, threshold, distance_theshold):
    max_distance = 0
    coordinate = None
    sign = None
    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        is_sign, distance = contourIsSign(c, [cX, cY], 1 - threshold)
        if is_sign and distance > max_distance and distance > distance_theshold:
            max_distance = distance
            coordinate = np.reshape(c, [-1, 2])
            left, top = np.amin(coordinate, axis=0)
            right, bottom = np.amax(coordinate, axis=0)
            coordinate = [(left - 2, top - 2), (right + 3, bottom + 1)]
            sign = cropSign(image, coordinate)
    return sign, coordinate


def localization(image, min_size_components, similitary_contour_with_circle):
    original_image = image.copy()

    binary_image = preprocess_image(image)
    binary_image = removeSmallComponents(binary_image, min_size_components)
    binary_image = cv2.bitwise_and(binary_image, binary_image, mask=remove_other_color(image))
    cv2.imshow('b3', binary_image)

    cv2.imshow('BINARY IMAGE', binary_image)
    contours = findContour(binary_image)
    sign, coordinate = findLargestSign(original_image, contours, similitary_contour_with_circle, 15)

    return coordinate, original_image, sign


def remove_other_color(img):
    frame = cv2.GaussianBlur(img, (3, 3), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([100, 128, 0])
    upper_blue = np.array([215, 255, 255])
    # Threshold the HSV image to get only blue colors
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_white = np.array([0, 0, 128], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)
    # Threshold the HSV image to get only blue colors
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([170, 150, 50], dtype=np.uint8)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    mask_1 = cv2.bitwise_or(mask_blue, mask_white)
    mask = cv2.bitwise_or(mask_1, mask_black)

    return mask


def getClassName(classNo):
    if classNo == 0:
        return 'Speed Limit 30 km/h'
    elif classNo == 1:
        return 'Speed Limit 70 km/h'
    elif classNo == 2:
        return 'Stop'
    elif classNo == 3:
        return 'No entry'


def get_prediction(model, img):
    img = img.reshape(1, 32, 32, 1)
    predictions = model.predict(img)

    return model.predict_classes(img) if np.amax(predictions) > threshold else -1
