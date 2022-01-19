import copy

import numpy as np

from set_search import search, utils
from set_search.data_structures import Card
import cv2 as cv
from set_search import constants as const

def find_sets(cards: list[Card]):
    sets = []
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            for k in range(j + 1, len(cards)):
                if ((cards[i].color + cards[j].color + cards[k].color) % 3 == 0) and (
                        (cards[i].shading + cards[j].shading + cards[k].shading) % 3 == 0) and (
                        (cards[i].type + cards[j].type + cards[k].type) % 3 == 0) and (
                        (cards[i].amount + cards[j].amount + cards[k].amount) % 3 == 0):
                    sets.append([cards[i], cards[j], cards[k]])
    return sets


def get_sets(image):
    #image = utils.read_image("images\\-2147483648_-244419.jpg")
    image = np.frombuffer(image, dtype=np.int8)
    image = cv.imdecode(image, cv.IMREAD_COLOR) # нормально

    cv.imwrite(const.DEBUG_PATH + "image.jpg", image)
    image_w, image_h, _ = image.shape
    # if image_w > 1500:
    #     new_size = (int(image_h * 0.5), int(image_w * 0.5))
    #     image = cv.resize(image, new_size, interpolation=cv.INTER_AREA)
    shapes = search.detect_shape_and_color(copy.copy(image))
    cards = search.group_shapes_into_cards(shapes, copy.copy(image))
    sets = find_sets(cards)
    result = []
    for i in range(len(sets)):
        cards = sets[i]
        result.append(utils.draw_set(cards, copy.copy(image)))
        cv.imwrite(f"{const.DEBUG_PATH}image{i}.jpg", image)
    return result


