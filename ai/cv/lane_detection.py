import cv2
import time
import utils
import numpy as np


curveList = []
avgVal = 10
initialTrackBarVals = [70, 155, 60, 227]


def getLaneCurve(img, display=1):
    imgResult = img.copy()

    # #### STEP 1
    imgThresOtsu = utils.tresholding_otsu(img)

    # #### STEP 2
    hT, wT, c = img.shape
    # points = utils.valTrackbars()
    points = utils.calculate_points(wT, hT, *initialTrackBarVals)
    imgWarp = utils.wrapImg(imgThresOtsu, points, wT, hT)
    # imgWarpPoints = utils.drawPoints(imgCopy, points)

    # #### STEP 3
    middlePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    # #### STEP 4
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)

    curve = int(sum(curveList) // len(curveList))

    # #### STEP 5
    frame = None
    if display != 0:
        imgInvWarp = utils.wrapImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(
                imgResult, (w * x + int(curve // 50), midY - 10), (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2
            )
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        # cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3)
        frame = imgResult
    if display == 1:
        imgStacked = utils.stackImages(1, ([img, imgThresOtsu, imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
        frame = imgStacked
    elif display == 2:
        cv2.imshow('Resutlt', imgResult)
        frame = imgStacked

    return frame, curve


if __name__ == '__main__':
    cap = cv2.VideoCapture('data/output.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # out = cv2.VideoWriter('data/result.mp4', fourcc, 20.0, (320*3, 2*240))

    # utils.initializeTracebars(initialTrackBarVals)

    frameCounter = 0
    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        succes, img = cap.read()
        if img is None:
            break
        time.sleep(1 / 40)
        frame, curve = getLaneCurve(img, 1)
        # out.write(frame)  # frameBuf.array
        cv2.waitKey(1)

    # out.release()
    cv2.destroyAllWindows()
