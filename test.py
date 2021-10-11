import matplotlib.pyplot as plt
import cv2
import numpy as np

def highLiteDiaposone(minTemp, maxTemp, fromTemp, toTemp, IMAGE_PATH): #25 33


    img = cv2.imread(IMAGE_PATH)
    ksize = (10, 10)
    img = cv2.blur(img, ksize)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_res = hsv_img.copy()

    if (maxTemp - toTemp <= .5):
        lower_white = np.array([0, 0, 51])
        upper_white = np.array([255, 79, 255])
        mask = cv2.inRange(hsv_res, lower_white, upper_white)
        mask = mask / 255
        mask = mask.astype(np.bool)
        hsv_res[:, :, :3][mask] = [0, 0, 255]

    if (fromTemp - minTemp <= .5):
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([255, 255, 50])
        mask = cv2.inRange(hsv_res, lower_black, upper_black)
        mask = mask / 255
        mask = mask.astype(np.bool)
        hsv_res[:, :, :3][mask] = [0, 80, 255]



    value = 20
    x = maxTemp - minTemp
    y = 0
    z = toTemp - minTemp
    a = fromTemp - minTemp
    m = 140
    l = m - int(m * z / x)
    u = m - int(m * a / x)

    lower = (l , 80, 50)
    upper = (u , 255, 255)
    mask = cv2.inRange(hsv_res, lower, upper)
    mask = mask / 255
    mask = mask.astype(np.bool)
    hsv_res[:, :, :3][mask] = [0, 0, 255]

    res = cv2.cvtColor(hsv_res, cv2.COLOR_HSV2RGB)
    plt.subplot(1, 1, 1)
    plt.imshow(res)
    plt.show()
    res = cv2.cvtColor(hsv_res, cv2.COLOR_HSV2BGR)
    # cv2.imwrite(IMAGE_SAVE_PATH, res)


def recolorImage(value ,IMAGE_PATH, IMAGE_SAVE_PATH):
    img = cv2.imread(IMAGE_PATH)
    ksize = (5, 5)
    img = cv2.blur(img, ksize)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_res = hsv_img.copy()

    lower_white = np.array([0, 0, 51])
    upper_white = np.array([20, 79, 255])
    mask = cv2.inRange(hsv_res, lower_white, upper_white)
    mask = mask / 255
    mask = mask.astype(np.bool)
    hsv_res[:, :, :3][mask] = [0, 80, 255]

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([50, 255, 50])
    mask = cv2.inRange(hsv_res, lower_black, upper_black)
    mask = mask / 255
    mask = mask.astype(np.bool)
    hsv_res[:, :, :3][mask] = [255, 255, 0]
    max_value = 130

    for i in range(0, value):
        print(i)
        lower = (i * max_value // value, 80, 50)
        upper = ((i + 1) * max_value // value, 255, 255)
        mask = cv2.inRange(hsv_img, lower, upper)
        mask = mask/255
        mask = mask.astype(np.bool)
        hsv_res[:, :, :3][mask] = [i * max_value//value, 255, 255]
        cv2.imshow('Result', cv2.cvtColor(hsv_res, cv2.COLOR_HSV2BGR))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    res = cv2.cvtColor(hsv_res, cv2.COLOR_HSV2BGR)
    cv2.imwrite(IMAGE_SAVE_PATH, res)

    res = cv2.cvtColor(hsv_res, cv2.COLOR_HSV2RGB)
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(res)
    plt.show()

def recoloeScaleTest(value, IMAGE_PATH, IMAGE_SAVE_PATH):
    img = cv2.imread(IMAGE_PATH)
    ksize = (5, 5)
    img = cv2.blur(img, ksize)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    height, width, sheet = hsv_img.shape
    fragmentHeight = int(height / value)
    max_value = 140
    hsv_img[0: fragmentHeight, 0: width] = (0, 0, 255)
    hsv_img[fragmentHeight * (value - 1): fragmentHeight + fragmentHeight * (value - 1), 0: width] = (255, 255, 0)

    value = value - 2
    for i in range(0, value):
        start = fragmentHeight * (i + 1)
        end = fragmentHeight + fragmentHeight * (i + 1)
        hsv_img[start: end, 0: width] = (i * max_value // value, 255, 255)

        result_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
        cv2.imwrite(IMAGE_SAVE_PATH, result_img)
        result_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
        # cv2.imwrite('TempFiles/BarFragments/fragment_' + str(i) + '.jpg', barFragment)
        # plt.subplot(1, 1, 1)
        # plt.imshow(result_img)
        # plt.show()


highLiteDiaposone(25, 33, 27, 32, 'ProjectData/original_image.jpg')