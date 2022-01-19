import copy

import cv2 as cv
from . import constants as const
from .data_structures import Shape


def get_grayscale_blurred_image(image):
    blurred_img = cv.GaussianBlur(image, (5, 5), cv.BORDER_DEFAULT)
    grayscale_img = cv.cvtColor(blurred_img, cv.COLOR_BGR2GRAY)
    return grayscale_img


def filter_shapes(contours, image):
    img_copy = copy.copy(image)
    img_size = image.shape
    img_min_dimension = min(img_size[0], img_size[1])

    min_contour_points = img_min_dimension * 0.04
    min_bounds_size = img_min_dimension * 0.03
    min_rect_size = img_min_dimension * 0.025
    max_rect_size = img_min_dimension * 0.19
    min_covering = const.MIN_DIAMOND_EXTENT
    max_covering = const.MAX_OVAL_EXTENT

    possible_shapes = []

    for i in range(len(contours)):
        contour = contours[i]
        if len(contour) < min_contour_points:
            continue
        _, _, rectangle_w, rectangle_h = cv.boundingRect(contour)
        if min(rectangle_w, rectangle_h) < min_bounds_size:
            if const.DEBUG:
                cv.drawContours(img_copy, contours, i, const.SMALL_CONTOUR_BOUNDING, 2, cv.LINE_8)
            continue

        shape = Shape(contour)

        if shape.min_dimension < min_rect_size:
            if const.DEBUG:
                cv.drawContours(img_copy, contours, i, const.SMALL_CONTOUR_MIN_RECT, 2, cv.LINE_8)
            continue
        if shape.min_dimension > max_rect_size:
            if const.DEBUG:
                cv.drawContours(img_copy, contours, i, const.BIG_CONTOUR_MIN_RECT, 2, cv.LINE_8)
            continue

        if shape.covering < min_covering:
            if const.DEBUG:
                cv.drawContours(img_copy, contours, i, const.SMALL_FILLING, 2, cv.LINE_8)
            continue
        if shape.covering > max_covering:
            if const.DEBUG:
                cv.drawContours(img_copy, contours, i, const.BIG_FILLING, 2, cv.LINE_8)
            continue
        if const.DEBUG:
            cv.drawContours(img_copy, contours, i, const.CORRECT_CONTOUR, 2, cv.LINE_8)
        possible_shapes.append(shape)
    if const.DEBUG:
        cv.imwrite("images/debug/filtered_contours.jpg", img_copy)
    return possible_shapes
