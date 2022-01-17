import copy

import cv2 as cv
import numpy as np

from . import constants as const
from . import preproccessing
from .data_structures import Shape
from .utils import draw_contours, rgb_to_hsl


def get_possible_shapes(image):
    blurred_grayscale_image = preproccessing.get_grayscale_blurred_image(image)
    with_thresholding = cv.adaptiveThreshold(blurred_grayscale_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv.THRESH_BINARY, 7, 1)
    if const.DEBUG:
        cv.imwrite("images/debug/blurred_grayscale_image.jpg", blurred_grayscale_image)
        cv.imwrite("images/debug/with_thresholding.jpg", with_thresholding)
    contours, hierarchy = cv.findContours(with_thresholding, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # if const.DEBUG:
    #     cv.imwrite("images/debug/all_contours.jpg", draw_contours(image, contours))
    shapes = preproccessing.filter_shapes(contours, image)
    if const.DEBUG:
        cv.imwrite("images/debug/correct_contours.jpg", draw_contours(copy.copy(image), [s.contour for s in shapes]))
    return shapes


def expand_contour(shape: Shape):
    return change_contour(shape, 1.4)


def shrink_contour(shape: Shape):
    return change_contour(shape, 0.7)


def change_contour(shape: Shape, coefficient):
    moments = cv.moments(shape.contour)
    centroid_x = int(moments['m10'] / moments['m00'])
    centroid_y = int(moments['m01'] / moments['m00'])
    normalized_contour = shape.contour - [centroid_x, centroid_y]
    scaled_normalized_contour = normalized_contour * coefficient
    scaled_contour = scaled_normalized_contour + [centroid_x, centroid_y]
    return scaled_contour.astype('int32')


def get_shapes(shapes, image):
    white = (255, 255, 255)
    black = (0, 0, 0)
    img_height, img_width, _ = image.shape
    i = 0
    result = []
    while i < len(shapes):
        shape = shapes[i]

        outer_contour = expand_contour(shape)
        inner_contour = shrink_contour(shape)
        rectangle_x, rectangle_y, rectangle_w, rectangle_h = cv.boundingRect(outer_contour)
        if rectangle_x < 0 or rectangle_y < 0 or rectangle_x + rectangle_w >= img_width or \
                rectangle_y + rectangle_h >= img_height:
            del shapes[i]
            continue

        # region of an image
        roi = image[rectangle_y:rectangle_y + rectangle_h, rectangle_x:rectangle_x + rectangle_w]
        offset = (-rectangle_x, -rectangle_y)
        mask = np.zeros((rectangle_h, rectangle_w), dtype="uint8")

        cv.drawContours(mask, [inner_contour], 0, white, -1, cv.LINE_8, None, None, offset)
        shape.mean_inner_color = rgb_to_hsl(cv.mean(roi, mask))

        # mean in contour without inner part
        cv.drawContours(mask, [shape.contour], 0, white, -1, cv.LINE_8, None, None, offset)
        cv.drawContours(mask, [inner_contour], 0, black, -1, cv.LINE_8, None, None, offset)
        shape.mean_contour_color = rgb_to_hsl(cv.mean(roi, mask))

        # mean in outer without contour part
        cv.drawContours(mask, [outer_contour], 0, white, -1, cv.LINE_8, None, None, offset)
        cv.drawContours(mask, [shape.contour], 0, black, -1, cv.LINE_8, None, None, offset)
        shape.mean_outer_color = rgb_to_hsl(cv.mean(roi, mask))
        cv.drawContours(mask, [outer_contour], 0, black, -1, cv.LINE_8, None, None, offset)

        shape.brightness_difference = int(shape.mean_contour_color[2]) - shape.mean_inner_color[2]
        # if outer contour darker then inner
        if int(shape.mean_outer_color[2]) - shape.mean_inner_color[2] <= -25:
            del shapes[i]
            continue

        shape.set_shading()
        shape.set_shape_color()
        result.append(shape)
        if const.DEBUG:
            roi_copy = copy.copy(roi)
            cv.drawContours(roi_copy, [inner_contour], 0, (0, 0, 255), 1, cv.LINE_8, None, None, offset) #red inner
            cv.drawContours(roi_copy, [outer_contour], 0, (0, 255, 0), 1, cv.LINE_8, None, None, offset) #green inner
            cv.drawContours(roi_copy, [shape.contour], 0, (255, 0, 0), 1, cv.LINE_8, None, None, offset) #blue contour
            cv.imwrite(f"images/debug/{shape.shading_debug()}.jpg", roi_copy)
        i += 1
    return result


def detect_shape_and_color(image):
    possible_shapes = get_possible_shapes(image)
    shapes = get_shapes(possible_shapes, image)
    return shapes
