from set_search import utils, search
import copy
import cv2 as cv

image = utils.read_image("images\\-2147483648_-244419.jpg")
image = cv.resize(image, (720, 540), interpolation=cv.INTER_AREA)
_ = search.get_contours(copy.copy(image))
