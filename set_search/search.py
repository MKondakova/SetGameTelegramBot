import cv2 as cv
from . import preproccessing
from .utils import draw_contours
from . import constants as const


def get_contours(image):
    blurred_grayscale_image = preproccessing.get_grayscale_blurred_image(image)
    with_thresholding = cv.adaptiveThreshold(blurred_grayscale_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv.THRESH_BINARY, 7, 1)
    if const.DEBUG:
        cv.imwrite("images/debug/blurred_grayscale_image.jpg", blurred_grayscale_image)
        cv.imwrite("images/debug/with_thresholding.jpg", with_thresholding)
    contours, hierarchy = cv.findContours(with_thresholding, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # if const.DEBUG:
    #     cv.imwrite("images/debug/all_contours.jpg", draw_contours(image, contours))
    contours = preproccessing.filter_shapes(contours, image)
    if const.DEBUG:
        cv.imwrite("images/debug/correct_contours.jpg", draw_contours(image, contours))
    return contours


def get_shapes_from_contours(image):
    img_size = image.shape


def detect_shape_and_color(image):
    possible_contours = get_contours(image)
    shapes = get_shapes_from_contours(possible_contours. image)
