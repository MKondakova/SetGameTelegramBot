from enum import IntFlag

import cv2 as cv

from . import constants as const


class ShapeType(IntFlag):
    OVAL = 1
    SQUIGGLE = 2
    DIAMOND = 3

    def __str__(self):
        if self == ShapeType.OVAL:
            return "овалы"
        elif self == ShapeType.DIAMOND:
            return "ромбы"
        else:
            return "волны"


class Color(IntFlag):
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

    def __str__(self):
        if self == Color.RED:
            return "красный"
        elif self == Color.GREEN:
            return "зеленый"
        else:
            return "фиолетовый"


class Shading(IntFlag):
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

    def __str__(self):
        if self == Shading.SOLID:
            return "закрашенные"
        elif self == Shading.STRIPED:
            return "заштрихованные"
        else:
            return "пустые"


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
            self.type = ShapeType.DIAMOND

    def set_shape_color(self):
        hue_angle = self.mean_contour_color[0]
        if const.MIN_GREEN_HUE <= hue_angle <= const.MAX_GREEN_HUE:
            self.color = Color.GREEN
        elif const.MIN_PURPLE_HUE <= hue_angle <= const.MAX_PURPLE_HUE:
            self.color = Color.PURPLE
        else:
            self.color = Color.RED

    def set_shading(self):
        self.brightness_difference = int(self.mean_outer_color[1]) - self.mean_inner_color[1]
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

    def color_debug(self):
        return f"{self.mean_contour_color}, {self.color}"

    def __eq__(self, other):
        if isinstance(other, Shape):
            return self.min_dimension == other.min_dimension


class Card:
    shapes = []
    amount = None
    type = None
    color = None
    shading = None

    def __init__(self, shapes=None):
        if shapes is None:
            shapes = []
        self.shapes = shapes

    @staticmethod
    def add_shapes_to_cards(cards, shape1: Shape, shape2: Shape):
        for card in cards:
            if shape1 in card.shapes:
                card.shapes.append(shape2)
                return
            elif shape2 in card.shapes:
                card.shapes.append(shape1)
                return
        cards.append(Card([shape1, shape2]))

    def __str__(self):
        return f"{len(self.shapes)}:{[s.__str__() for s in self.shapes]}"

    def complete_card(self):
        self.amount = len(self.shapes)
        self.type = self.shapes[0].type
        if not all(s.type == self.type for s in self.shapes):
            raise Exception("Different shapes detected")
        self.color = self.shapes[0].color
        if not all(s.color == self.color for s in self.shapes):
            raise Exception("Different colors detected")
        self.shading = self.shapes[0].shading
        if not all(s.shading == self.shading for s in self.shapes):
            raise Exception("Different shadings detected")
