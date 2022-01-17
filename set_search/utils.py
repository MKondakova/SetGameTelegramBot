import numpy as np
import cv2 as cv
import random


def draw_contours(image, contours):
    image_with_counters = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        cv.drawContours(image_with_counters, contours, i, color, 2, cv.LINE_8)
    return image_with_counters


def draw_shapes(image, shapes):
    image_with_counters = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for i in range(len(shapes)):
        color = (shapes[i].color.get_color())
        thickness = shapes[i].shading.get_thickness()
        cv.drawContours(image_with_counters, [s.contour for s in shapes], i, color, thickness, cv.LINE_8)
    return image_with_counters


def read_image(path):
    image = cv.imread(path)
    return image


def rgb_to_hsl(color):
    rgb_image = np.uint8([[[color[0], color[1], color[2]]]])
    hsl_image = cv.cvtColor(rgb_image, cv.COLOR_RGB2HSV)
    return hsl_image[0][0]
