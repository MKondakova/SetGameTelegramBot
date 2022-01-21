from set_search.data_structures import Card


class SetResult:
    def __init__(self, sets: list[list[Card]], image):
        self.sets = sets
        self.image = image
        self.has_sets = len(sets) > 0
        self.first_unseen_set = 0
        self.color = [s[0].color if s[0].color == s[1].color else None for s in sets]
        self.shading = [s[0].shading if s[0].shading == s[1].shading else None for s in sets]
        self.shapes = [s[0].type if s[0].type == s[1].type else None for s in sets]
        self.amount = [s[0].amount if s[0].amount == s[1].amount else None for s in sets]
        self.is_different = [
            (self.amount[i] is None) * 1 + (self.shapes[i] is None) * 1 + (self.shading[i] is None) * 1 + (
                    self.color[i] is None) * 1 for i in range(len(sets))]
