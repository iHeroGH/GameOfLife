import random as rand
from CellMatrix import CellMatrix
from Render import Render


"""
Rules

if alive:
    Less than 2: dies
    2, 3: lives
    More than 3: dies

if dead:
    3: lives

"""
window = 50
cell_matrix_obj = CellMatrix()
cell_matrix_obj.init_cell_matrix(window+10)
cell_matrix = cell_matrix_obj.cell_matrix

# cell_matrix_obj.random_change(window)

# cell_matrix_obj.change_index_state(1, 4, True)
# cell_matrix_obj.change_index_state(1, 5, True)
# cell_matrix_obj.change_index_state(1, 6, True)

# cell_matrix_obj.change_index_state(3, 2, True)
# cell_matrix_obj.change_index_state(4, 2, True)
# cell_matrix_obj.change_index_state(5, 2, True)

# cell_matrix_obj.change_index_state(4, 6, True)
# cell_matrix_obj.change_index_state(3, 6, True)
# cell_matrix_obj.change_index_state(5, 6, True)

# cell_matrix_obj.change_index_state(6, 3, True)
# cell_matrix_obj.change_index_state(6, 4, True)
# cell_matrix_obj.change_index_state(6, 5, True)


render = Render(700, window, cell_matrix_obj)


