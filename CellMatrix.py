from Cell import Cell
import random as rand

class CellMatrix:

    def __init__(self):
        self.cell_matrix = []
        self.dimension = 0

    def __str__(self):
        # The string representation of the cell matrix
        output = ""
        for l in self.cell_matrix:
            for i in l:
                output += f"{i}   "
            if l != self.cell_matrix[len(self.cell_matrix)-1]:
                output += "\n"  
        return output

    def __repr__(self):
        # The string representation of the cell matrix
        output = ""
        for l in self.cell_matrix:
            for i in l:
                output += f"{i}   "
            if l != self.cell_matrix[len(self.cell_matrix)-1]:
                output += "\n"  
        return output

    def init_cell_matrix(self, dimension:int=10):
        # Create a dimension x dimension cell matrix
        self.dimension = dimension
        for i in range(dimension):
            current_cell_list = []

            for j in range(dimension):
                current_cell_list.append(Cell(i, j))

            self.cell_matrix.append(current_cell_list)

    def change_index_state(self, r:int, c:int, state:bool):
        self.cell_matrix[r][c].change_state(state)

    def random_change(self, window,tolerance:int=20):
        # Make tolerance amount of random indicies alive
        [(self.cell_matrix[self.random_ind(window)][self.random_ind(window)].change_state(True)) for i in range(tolerance)]

    def get_alive(self):
        # Returns a list of tuples of (row, col) of all alive cells
        alive_cells = []
        for row, list in enumerate(self.cell_matrix):
            for col, block in enumerate(list):
                if block.is_alive:
                    alive_cells.append((row, col))
        return alive_cells
    
    def reset_cells(self):
        self.cell_matrix = []
        self.init_cell_matrix(self.dimension)
        
    def count_neighbors(self, cell:Cell) -> int:
        # Count and return how many live neighbors a cell has
        living_cells = 0
        for curr_row, curr_col in Cell.surrounding_cells():
            next_row = int(cell.row + curr_row)
            next_col = int(cell.col + curr_col) 

            #if cell.is_alive: print(cell.row, cell.col, next_row, next_col)

            if next_row >= self.dimension or next_col >= self.dimension or next_row < 0 or next_col < 0:
                continue
            if self.cell_matrix[next_row][next_col].is_alive:
                living_cells += 1

        cell.change_neighbors(living_cells)

        return living_cells

    def next_generation(self):
        # Simulate the next generation
        to_apply_list = []
        for row in self.cell_matrix:
            for cell in row:
                living_cells = self.count_neighbors(cell)         
                to_apply_list.append(self.apply_rules(cell))

        for cell, state in to_apply_list:
            if state != None:
                cell.change_state(state)

        return self.cell_matrix

    def apply_rules(self, cell):
        # Apply the Game of Life rules
        to_apply = (cell, None) # tuple (cell, state)
        living_cells = cell.living_neighbors
        if cell.is_alive:
            if living_cells < 2:
                to_apply = (cell, False)
            elif living_cells <= 3:
                to_apply = (cell, None)
            else:
                to_apply = (cell, False)
        if living_cells == 3:
            to_apply = (cell, True)
        else:
            to_apply = (cell, to_apply[1])
 
        
        return to_apply

    def random_ind(self, window):
        # Get a random index within the limits of the matrix
        return rand.randint(0, window-1)
    