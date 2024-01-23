from parts.arrows.single_arrow import Arrow


class Arrows:
    def __init__(self):
        self.arrows_list = []
        self.should_check_collisions = True

    def add_arrow(self, raven_position):
        self.should_check_collisions = True
        self.arrows_list.append(Arrow(raven_position))

    def on_move_arrows(self, raven_position):
        if self.should_check_collisions == False:
            return False
        is_hit = False
        new_arrow_list = []
        for arr in self.arrows_list:
            if type(arr) == Arrow and not arr.get_is_aget_is_arrow_out_of_bound():
                arr.move_arrow()
                if arr.get_did_arrow_hit(raven_position):
                    is_hit = True
                new_arrow_list.append(arr)
        self.arrows_list = new_arrow_list
        if is_hit:
            self.should_check_collisions = False
            self.arrows_list = []
        return is_hit

    def render_arrows(self, screen):
        for arrow in self.arrows_list:
            if type(arrow) == Arrow:
                screen.blit(arrow.arrow_img, arrow.current_position)

    def reset(self):
        self.arrows_list = []
        self.should_check_collisions = True
