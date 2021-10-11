import numpy as np
import glob
import cv2
from PIL import Image, ImageFilter, ImageEnhance

def recolor(img, IMAGE_PATH):
    colorsImg = Image.open(IMAGE_PATH)
    data = np.array(img)
    colorsData = np.array(colorsImg)

    print(colorsData[0][0])

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    r2, g2, b2 = int(colorsData[0][0][0]), int(colorsData[0][0][1]), int(colorsData[0][0][2])

    for row in colorsData:
        r1, g1, b1 = int(row[0][0]), int(row[0][1]), int(row[0][2])
        mask = (abs(red - r1) < 30) & (abs(green - g1) < 30) & (abs(blue - b1) < 30)
        data[:, :, :3][mask] = [r2, g2, b2]

    return Image.fromarray(data)

def recoloeScale(value, IMAGE_PATH, IMAGE_SAVE_PATH):
    img = cv2.imread(IMAGE_PATH)
    height, width, sheet = img.shape
    fragmentHeight = height / value
    for i in range(1, value - 1):
        start = int(fragmentHeight * i)
        end = int(fragmentHeight + fragmentHeight * i)
        barFragment = img[start: end, 0:width]
        cv2.imwrite('TempFiles/BarFragments/fragment_' + str(i) + '.jpg', barFragment)

def recolorImage(value ,IMAGE_PATH, IMAGE_SAVE_PATH):
    img = cv2.imread(IMAGE_PATH)
    ksize = (10, 10)
    img = cv2.blur(img, ksize)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_res = hsv_img.copy()

    # value = value - 2
    lower_white = np.array([0, 0, 51])
    upper_white = np.array([255, 79, 255])
    mask = cv2.inRange(hsv_res, lower_white, upper_white)
    mask = mask / 255
    mask = mask.astype(np.bool)
    hsv_res[:, :, :3][mask] = [0, 80, 255]

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([255, 255, 50])
    mask = cv2.inRange(hsv_res, lower_black, upper_black)
    mask = mask / 255
    mask = mask.astype(np.bool)
    hsv_res[:, :, :3][mask] = [255, 255, 0]
    value = value - 2
    for i in range(0, value):
        max_value = 140
        lower = (i * max_value // value, 80, 50)
        upper = ((i + 1) * max_value // value, 255, 255)
        mask = cv2.inRange(hsv_img, lower, upper)
        mask = mask/255
        mask = mask.astype(np.bool)
        hsv_res[:, :, :3][mask] = [i * max_value // value, 255, 255]

    res = cv2.cvtColor(hsv_res, cv2.COLOR_HSV2BGR)
    cv2.imwrite(IMAGE_SAVE_PATH, res)

def recoloeScale(value, IMAGE_PATH, IMAGE_SAVE_PATH):
    img = cv2.imread(IMAGE_PATH)
    ksize = (5, 5)
    img = cv2.blur(img, ksize)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    height, width, sheet = hsv_img.shape
    fragmentHeight = int(height / value)
    max_value = 140
    hsv_img[0: fragmentHeight, 0: width] = (0, 80, 255)
    hsv_img[fragmentHeight * (value - 1): fragmentHeight + fragmentHeight * (value - 1), 0: width] = (255, 255, 0)

    value = value - 2
    for i in range(0, value):
        start = fragmentHeight * (i + 1)
        end = fragmentHeight + fragmentHeight * (i + 1)
        hsv_img[start: end, 0: width] = (i * max_value // value, 255, 255)

        result_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
        cv2.imwrite(IMAGE_SAVE_PATH, result_img)

def recolorExe(IMAGE_PATH, IMAGE_PATH_SAVE):
    value = len(glob.glob('TempFiles/BarFragments/*'))
    recolorImage(value, IMAGE_PATH, IMAGE_PATH_SAVE)

