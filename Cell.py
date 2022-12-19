class Cell:

    def __init__(self, r, c):
        self.is_alive = False
        self.row = r
        self.col = c
        self.living_neighbors = 0
    
    def change_state(self, new_state:bool):
        #print(self.row, self.col, new_state)
        self.is_alive = new_state
    
    def change_neighbors(self, new_neigh):
        self.living_neighbors = new_neigh

    def __repr__(self):
        return ("1" if self.is_alive else "0")

    @staticmethod
    def surrounding_cells():
        return [
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, 0),
            (1, -1)
        ]
