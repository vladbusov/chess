class game(object):
    def __init__(self):
        self.step = 0
        self.black = True
    def change_side(self):
        if self.black == True:
            self.black = False
        else:
            self.black = True
        self.step = self.step + 1