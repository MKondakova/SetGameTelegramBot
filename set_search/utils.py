import numpy as np
import cv2 as cv
import random


def draw_contours(image, contours):
    image_with_counters = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        cv.drawContours(image_with_counters, contours, i, color, 2, cv.LINE_8)
    return image_with_counters


def read_image(path):
    image = cv.imread(path)
    return image
