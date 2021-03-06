import copy
import math

import cv2 as cv
import numpy as np

from . import constants as const
from . import preproccessing

from .data_structures import Shape, Card
from .utils import draw_contours, rgb_to_hls


def get_possible_shapes(image):
    blurred_grayscale_image = preproccessing.get_grayscale_blurred_image(image)
    with_thresholding = cv.adaptiveThreshold(blurred_grayscale_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv.THRESH_BINARY, 7, 2)
    if const.DEBUG:
        cv.imwrite(const.DEBUG_PATH + "blurred_grayscale_image.jpg", blurred_grayscale_image)
        cv.imwrite(const.DEBUG_PATH + "with_thresholding.jpg", with_thresholding)
    contours, hierarchy = cv.findContours(with_thresholding, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if const.DEBUG:
        cv.imwrite("images/debug/all_contours.jpg", draw_contours(copy.copy(image), contours))
    shapes = preproccessing.filter_shapes(contours, image)
    return shapes


def expand_contour(shape: Shape):
    return change_contour(shape.contour, shape.min_dimension * 0.2)


def shrink_contour(shape: Shape):
    return change_contour(shape.contour, shape.min_dimension * -0.13)


def change_contour(contour, coefficient):
    new_contour_increments = []
    contour_len = len(contour)
    for i in range(contour_len):
        prev_index = (contour_len + i - 1) % contour_len
        next_index = (i + 1) % contour_len
        prev_point = contour[prev_index][0]
        next_point = contour[next_index][0]
        normalized_perpendicular = get_normalized_perpendicular(prev_point, next_point)
        increment = [[normalized_perpendicular[0] * coefficient, normalized_perpendicular[1] * coefficient]]
        new_contour_increments.append(increment)
    new_contour = contour + np.array(new_contour_increments)
    return new_contour.astype('int32')


def get_normalized_perpendicular(point_a, point_b):
    vector = point_b - point_a
    if math.hypot(vector[0], vector[1]) == 0:
        return vector
    vector = vector / math.hypot(vector[0], vector[1])
    return [vector[1], -vector[0]]


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
        shape.mean_inner_color = rgb_to_hls(cv.mean(roi, mask))

        # mean in contour without inner part
        cv.drawContours(mask, [shape.contour], 0, white, -1, cv.LINE_8, None, None, offset)
        cv.drawContours(mask, [inner_contour], 0, black, -1, cv.LINE_8, None, None, offset)
        shape.mean_contour_color = rgb_to_hls(cv.mean(roi, mask))

        # mean in outer without contour part
        cv.drawContours(mask, [outer_contour], 0, white, -1, cv.LINE_8, None, None, offset)
        cv.drawContours(mask, [shape.contour], 0, black, -1, cv.LINE_8, None, None, offset)
        shape.mean_outer_color = rgb_to_hls(cv.mean(roi, mask))

        # if outer contour darker then inner
        if int(shape.mean_outer_color[1]) - shape.mean_inner_color[1] <= -25:
            del shapes[i]
            continue

        shape.set_shading()
        shape.set_shape_color()
        result.append(shape)
        if const.DEBUG:
            roi_copy = copy.copy(roi)
            cv.drawContours(roi_copy, [inner_contour], 0, (0, 0, 255), 1, cv.LINE_8, None, None, offset)  # red inner
            cv.drawContours(roi_copy, [outer_contour], 0, (0, 255, 0), 1, cv.LINE_8, None, None, offset)  # green inner
            cv.drawContours(roi_copy, [shape.contour], 0, (255, 0, 0), 1, cv.LINE_8, None, None, offset)  # blue contour
            cv.imwrite(f"{const.DEBUG_PATH}{shape}.jpg", roi_copy)
        i += 1
    return result


def filter_inner_shapes(shapes: list[Shape]):
    unique_shapes = []

    for current_shape in shapes:
        is_unique = True

        for other_shape in shapes:
            if current_shape == other_shape:
                continue

            x = int(current_shape.contour[0][0][0])
            y = int(current_shape.contour[0][0][1])

            if cv.pointPolygonTest(other_shape.contour, (x, y), False) > 0:
                is_unique = False
                break

        if is_unique:
            unique_shapes.append(current_shape)

    return unique_shapes


def detect_shape_and_color(image):
    possible_shapes = get_possible_shapes(image)
    shapes = get_shapes(possible_shapes, image)
    shapes = filter_inner_shapes(shapes)
    if const.DEBUG:
        cv.imwrite(const.DEBUG_PATH + "correct_contours.jpg",
                   draw_contours(copy.copy(image), [s.contour for s in shapes]))
    return shapes


def group_shapes_into_cards(shapes: list[Shape], image):
    already_in_card = []
    cards = []

    for i in range(len(shapes)):
        shape = shapes[i]
        is_already_in_card = shape in already_in_card
        shape_center = (int(shape.min_rect[0][0]), int(shape.min_rect[0][1]))
        if const.DEBUG:
            cv.circle(image, shape_center, 1, (255, 255, 255), 1)
            cv.circle(image, shape_center, int(const.CIRCLE_RADIUS_COEFFICIENT * shape.min_dimension), (255, 255, 255), 2)
        for j in range(i+1, len(shapes)):
            another_shape = shapes[j]
            another_shape_center = (int(another_shape.min_rect[0][0]), int(another_shape.min_rect[0][1]))
            difference_x = shape_center[0] - another_shape_center[0]
            difference_y = shape_center[1] - another_shape_center[1]
            distance = math.hypot(difference_x, difference_y)

            if distance < const.CIRCLE_RADIUS_COEFFICIENT * max(shape.min_dimension, another_shape.min_dimension):
                already_in_card.append(another_shape)
                is_already_in_card = True
                Card.add_shapes_to_cards(cards, shape, another_shape)

        if not is_already_in_card:
            cards.append(Card([shape]))
    if const.DEBUG:
        cv.imwrite(const.DEBUG_PATH + "circles.jpg", image)
    for card in cards:
        card.complete_card()
    return cards
