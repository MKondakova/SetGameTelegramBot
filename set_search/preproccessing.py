import cv2 as cv
from . import constants as const


def get_grayscale_blurred_image(image):
    blurred_img = cv.GaussianBlur(image, (5, 5), cv.BORDER_DEFAULT)
    grayscale_img = cv.cvtColor(blurred_img, cv.COLOR_BGR2GRAY)
    return grayscale_img


def filter_shapes(contours, image):
    img_size = image.shape
    img_min_dimension = min(img_size[0], img_size[1])

    min_contour_points = img_min_dimension * 0.04
    min_bounds_size = img_min_dimension * 0.03
    min_rect_size = img_min_dimension * 0.025
    max_rect_size = img_min_dimension * 0.19
    min_filling = const.MIN_DIAMOND_EXTENT
    max_filling = const.MAX_OVAL_EXTENT

    possible_shapes = []

    for i in range(len(contours)):
        contour = contours[i]
        if len(contour) < min_contour_points:
            continue
        bounding_rect = cv.boundingRect(contour)
        if bounding_rect[2] < min_bounds_size and bounding_rect[3] < min_bounds_size:
            if const.DEBUG:
                cv.drawContours(image, contours, i, const.SMALL_CONTOUR_BOUNDING, 2, cv.LINE_8)
            continue

        min_rect = cv.minAreaRect(contour)

        if min_rect[1][0] < min_rect_size or min_rect[1][1] < min_rect_size:
            if const.DEBUG:
                cv.drawContours(image, contours, i, const.SMALL_CONTOUR_MIN_RECT, 2, cv.LINE_8)
            continue
        if min_rect[1][0] > max_rect_size and min_rect[1][1] > max_rect_size:
            if const.DEBUG:
                cv.drawContours(image, contours, i, const.BIG_CONTOUR_MIN_RECT, 2, cv.LINE_8)
            continue

        area = cv.contourArea(contour)
        filling = area / min_rect[1][0] / min_rect[1][1]
        if filling < min_filling:
            if const.DEBUG:
                cv.drawContours(image, contours, i, const.SMALL_FILLING, 2, cv.LINE_8)
            continue
        if filling > max_filling:
            if const.DEBUG:
                cv.drawContours(image, contours, i, const.BIG_FILLING, 2, cv.LINE_8)
            continue
        if const.DEBUG:
            cv.drawContours(image, contours, i, const.CORRECT_CONTOUR, 2, cv.LINE_8)
        possible_shapes.append(contour)
    if const.DEBUG:
        cv.imwrite("images/debug/filter_contours.jpg", image)
    return possible_shapes
