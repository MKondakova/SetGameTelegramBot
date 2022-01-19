import numpy as np
import cv2 as cv
import random
from set_search import constants as const

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


def rgb_to_hls(color):
    rgb_image = np.uint8([[[color[0], color[1], color[2]]]])
    hls_image = cv.cvtColor(rgb_image, cv.COLOR_BGR2HLS)
    return hls_image[0][0]


def draw_set(cards, image):
    color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
    for card in cards:
        for shape in card.shapes:
            shape_center = (int(shape.min_rect[0][0]), int(shape.min_rect[0][1]))
            cv.circle(image, shape_center, 1, (255, 255, 255), 1)
            cv.circle(image, shape_center, int(const.CIRCLE_RADIUS_COEFFICIENT * shape.min_dimension), color, 2)
    return image

