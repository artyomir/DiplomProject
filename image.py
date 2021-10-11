import numpy as np
import cv2
import easyocr
import glob
import os
import re

def addScale(minTemp, maxTemp, scaleStep, IMAGE_PATH):
    #Добавляет на изображение шкалу с scaleSize линиями и возвращает новое изображение
    img = cv2.imread(IMAGE_PATH)

    #add white bord
    img = cv2.copyMakeBorder(
        img, 0, 0, 0, 35, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # scaleStep = (maxTemp - minTemp)/scaleSize
    scaleSize = int((maxTemp - minTemp)//scaleStep + (maxTemp - minTemp)%scaleStep)
    h, w = img.shape[:2]
    font = cv2.FONT_HERSHEY_PLAIN

    for i in range(1, scaleSize):
        img = cv2.line(img,(0, h//scaleSize*i), (w - 15 - 15 * (i % 2) , h//scaleSize*i), (0,0,0),1)

    for i in range(1, scaleSize + 1):
        # cv2.putText(img, str(maxTemp-scaleStep*i)[0:4], (15, abs(h//scaleSize*i - h//scaleSize//2) + i * scaleSize), font, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, str(maxTemp-scaleStep*i)[0:4], (13, h//scaleSize*i - 2), font, 0.7, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.putText(img, 'C', (35, 14), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img, 'o', (29, 8), font, 0.7, (0, 0, 0), 1, cv2.LINE_AA)

    # for i in range(0, scaleSize + 1):
    #     # img_mof = cv2.line(img,(0,0),(w, h),(0,0,255),1)
    #     img = cv2.line(img,(10, abs(h//scaleSize*i - 1)), (w, abs(h//scaleSize*i - 1)), (0,0,0),1)
    #     cv2.putText(img, str(minTemp+scaleStep*i), (15, abs(h//scaleSize*i - 3)), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

    return img

def cutTermogramm (IMAGE_PATH):
    img = cv2.imread(IMAGE_PATH)
    height, width = img.shape[:2]
    tempBar = img[0:height, 0:width//24]
    thermoImg = img[0:height, width//6:width]

    return tempBar, thermoImg

def resizeImage(IMAGE_PATH, maxHeigh):
    img = cv2.imread(IMAGE_PATH)
    h, w = img.shape[:2]
    img = cv2.resize(img, (int(maxHeigh * w / h), maxHeigh))
    return img

def cleanImage (img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    bg = cv2.morphologyEx(img, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(img, bg, scale=255)
    # return img
    return img

def readTempFromImage (IMAGE_PATH):
    reader = easyocr.Reader(['en'])#, gpu=True)
    result = reader.readtext(IMAGE_PATH)
    tempFromImage = [int(re.findall('\d\d', row[1])[0]) for row in result if re.search('\d\d+', row[1])]
    if len(tempFromImage) == 1:
        return tempFromImage[0]
    else:
        return None

def FindMinMaxTemp (img):
    height, width, sheet = img.shape
    img_topLeft = img[0:35, 35:80]
    img_botLeft = img[height - 35:height, 35:80]

    img_topLeft = cleanImage(img_topLeft)
    img_botLeft = cleanImage(img_botLeft)

    cv2.imwrite(r'TempFiles/topLeft.jpg', img_topLeft)
    cv2.imwrite(r'TempFiles/botLeft.jpg', img_botLeft)

    minT = readTempFromImage(r'TempFiles/topLeft.jpg')
    maxT = readTempFromImage(r'TempFiles/botLeft.jpg')

    return minT, maxT

def MinMaxTempExe (IMAGE_PATH):
    print(IMAGE_PATH.split('\\')[len(IMAGE_PATH.split('\\')) - 1])

    img = cv2.imread(IMAGE_PATH)

    minT, maxT = FindMinMaxTemp(img)

    for i in range(0, 4):
        if minT is None or maxT is None:
            img = np.rot90(img)
            minT, maxT = FindMinMaxTemp(img)

    h, w = img.shape[:2]
    if (minT is None or maxT is None) and  h < w:
        img = np.rot90(img)
    cv2.imwrite(IMAGE_PATH, img)

    print(minT, maxT)

    return minT, maxT

def CutBar(fragmentsAmount, IMAGE_PATH):
    files = glob.glob('TempFiles/BarFragments//*')
    for f in files:
        os.remove(f)
    if fragmentsAmount < 1:
        return
    img = cv2.imread(IMAGE_PATH)
    height, width, sheet = img.shape
    fragmentHeight = height / fragmentsAmount
    for i in range(0, fragmentsAmount):
        start = int(fragmentHeight * i)
        end = int(fragmentHeight + fragmentHeight * i)

        barFragment = img[start: end, 0:width]
        cv2.imwrite('TempFiles/BarFragments/fragment_' + str(i) + '.jpg', barFragment)
#
# img = addScale(10, 'ImageData\\default_bar.jpg', 600)
# cv2.imshow("Line",img)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# #
