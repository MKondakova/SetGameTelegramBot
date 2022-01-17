from enum import Enum

import cv2 as cv

from . import constants as const


class ShapeType(Enum):
    OVAL = 1
    SQUIGGLE = 2
    DIAMOND = 3
    ERROR = 4


class Color(Enum):
    GREEN = 1
    RED = 2
    PURPLE = 3

    def get_color(self):
        if self == Color.RED:
            return 0, 0, 255
        elif self == Color.GREEN:
            return 0, 255, 0
        else:
            return 128, 0, 128


class Shading(Enum):
    SOLID = 1
    STRIPED = 2
    OUTLINED = 3

    def get_thickness(self):
        if self == Shading.SOLID:
            return -1
        elif self == Shading.STRIPED:
            return 3
        else:
            return 1


class Shape:
    color = None
    shading = None
    type = None
    mean_inner_color = None
    mean_contour_color = None
    mean_outer_color = None
    brightness_difference = None

    def __init__(self, contour):
        self.contour = contour
        self.min_rect = cv.minAreaRect(contour)
        self.min_dimension = min(self.min_rect[1][0], self.min_rect[1][1])

        area = cv.contourArea(contour)
        self.covering = int(area * 100 / (self.min_rect[1][0] * self.min_rect[1][1]))
        if const.MIN_OVAL_EXTENT <= self.covering <= const.MAX_OVAL_EXTENT:
            self.type = ShapeType.OVAL
        elif const.MIN_SQUIGGLE_EXTENT <= self.covering <= const.MAX_SQUIGGLE_EXTENT:
            self.type = ShapeType.SQUIGGLE
        elif const.MIN_DIAMOND_EXTENT <= self.covering <= const.MAX_DIAMOND_EXTENT:
            self.type = ShapeType.DIAMOND
        else:
            self.type = ShapeType.ERROR

    def set_shape_color(self):
        hue_angle = self.mean_contour_color[0] / 255 * 360
        if const.MIN_GREEN_HUE <= hue_angle <= const.MAX_GREEN_HUE:
            self.color = Color.GREEN
        elif const.MIN_PURPLE_HUE <= hue_angle <= const.MAX_PURPLE_HUE:
            self.color = Color.PURPLE
        else:
            self.color = Color.RED

    def set_shading(self):
        if self.brightness_difference <= const.MAX_OUTLINED_BRIGHTNESS_DIFFERENCE:
            self.shading = Shading.OUTLINED
        elif self.brightness_difference <= const.MAX_STRIPED_BRIGHTNESS_DIFFERENCE:
            self.shading = Shading.STRIPED
        else:
            self.shading = Shading.SOLID

    def __str__(self):
        return f"{self.color} {self.shading} {self.type}"

    def shading_debug(self):
        return f"{self.shading} {self.brightness_difference}"
