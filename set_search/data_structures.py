from . import constants as const


class Shape:
    color = None
    shading = None
    type = None

    def __init__(self, contour, extent):
        self.contour = contour
        if const.MIN_OVAL_EXTENT <= extent <= const.MAX_OVAL_EXTENT:
            self.type = const.OVAL_TYPE
        elif const.MIN_SQUIGGLE_EXTENT <= extent <= const.MAX_SQUIGGLE_EXTENT:
            self.type = const.SQUIGGLE_TYPE
        elif const.MIN_DIAMOND_EXTENT <= extent <= const.MAX_DIAMOND_EXTENT:
            self.type = const.DIAMOND_TYPE
        else:
            self.type = const.ERROR_TYPE
