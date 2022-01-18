from set_search import utils, search, constants
import copy

import cv2 as cv

image = utils.read_image("images\\-2147483648_-244419.jpg")
cv.imwrite(constants.DEBUG_PATH + "image.jpg", image)
#image = cv.resize(image, (720, 540), interpolation=cv.INTER_AREA)
shapes = search.detect_shape_and_color(copy.copy(image))
cv.imshow("s", utils.draw_shapes(image, shapes))
cv.waitKey()