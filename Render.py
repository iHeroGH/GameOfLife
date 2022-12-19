import pygame
from CellMatrix import CellMatrix

class Render:

    def __init__(self, dimension:int, matrix_window:int, cell_matrix_obj:CellMatrix):
        self.WIDTH, self.HEIGHT = dimension, dimension
        self.cell_matrix_obj = cell_matrix_obj
        self.matrix_window = matrix_window
        self.blocks_matrix = []
        self.motion_blocks = set()
        self.can_move = True

        self.init_screen()
        self.fix_dimensions()
        self.block_size = self.get_block_size()
        self.draw_grid()
        self.prime_colors()
        self.display_loop()

    def init_screen(self):
        self.screen = pygame.display.set_mode(size=(self.WIDTH, self.HEIGHT))
        self.screen.fill((255, 255, 255))       
        pygame.display.set_caption("The Game of Life")

    def fix_dimensions(self):
        if self.WIDTH == 0 or self.HEIGHT == 0:
            self.WIDTH, self.HEIGHT = self.screen.get_size()

    def draw_grid(self):
        for x in range(0, self.WIDTH, self.block_size):
            blocks_list = []

            for y in range(0, self.HEIGHT, self.block_size):
                block = pygame.Rect(x, y, self.block_size, self.block_size)
                blocks_list.append(block)
                pygame.draw.rect(self.screen, (220, 220, 220), block, 1)

            self.blocks_matrix.append(blocks_list)

    def get_block_size(self):
        return min(int(self.WIDTH/self.matrix_window), int(self.HEIGHT/self.matrix_window))
    
    def get_pressed_block(self, x_pos, y_pos):
        # Returns a tuple (block pressed, row, col)
        for row, blocks_list in enumerate(self.blocks_matrix):
            for col, block in enumerate(blocks_list):
                block_x, block_y = block.x, block.y
                if x_pos in [i for i in range(block_x, self.block_size+block_x)] and y_pos in [i for i in range(block_y, self.block_size+block_y)]:
                    return (block, row, col)

    def get_block_index(self, input_block):
        for row, blocks_list in enumerate(self.blocks_matrix):
            for col, block in enumerate(blocks_list):
                if block == input_block:
                    return (row, col)

    def get_cell_at_index(self, row, col):
        return self.cell_matrix_obj.cell_matrix[row][col]

    def get_hashable_block_info(self, block):
        row, col = self.get_block_index(block)
        cell = self.get_cell_at_index(row, col)
        
        return (cell.is_alive, row, col)

    def prime_colors(self, pressed_block=None):
        change_cells = None

        if pressed_block:
            change_cells = [(pressed_block[1], pressed_block[2])]
        
        change_cells = change_cells or self.cell_matrix_obj.get_alive()
        for row, col in change_cells:
            curr_cell = self.get_cell_at_index(row, col)
            alive = curr_cell.is_alive
            if row >= len(self.blocks_matrix) or col >= len(self.blocks_matrix[0]) or row < 0 or col < 0:
                continue
            block = self.blocks_matrix[row][col]
            block_x, block_y = block.x, block.y

            new_block = pygame.Rect(block_x, block_y, self.block_size, self.block_size)
            if alive and pressed_block:
                pygame.draw.rect(self.screen, (255, 255, 255), new_block, 0)
                curr_cell.change_state(False)
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), new_block, 0)
                curr_cell.change_state(True)
            
            pygame.draw.rect(self.screen, (220, 220, 220), new_block, 1)

            self.blocks_matrix[row][col] = new_block

    def reset_screen(self, reset_cells:bool=True):
        self.blocks_matrix = []
        self.motion_blocks = set()
        self.can_move = True
        self.screen.fill((255, 255, 255)) 
        if reset_cells:
            self.cell_matrix_obj.reset_cells()
        self.draw_grid()

    def dispatch_next_generation(self):
        self.cell_matrix_obj.next_generation()
        self.reset_screen(False)
        self.prime_colors()

    def display_loop(self):
        
        pygame.key.set_repeat(100)

        running = True
        while running: # Make sure user hasn't exited
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT: # If top right x button
                    running = False

                if event.type == pygame.KEYDOWN: # If keyboard button
                    if event.key == 27: # If esc key
                        running = False
                    if event.key == 32: # Space
                        self.dispatch_next_generation()
                    if event.key == 8: # Backspace
                        self.reset_screen()

                if event.type == pygame.MOUSEBUTTONDOWN: # If button click 
                    if event.button == 1: # Left click
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        curr_block = self.get_pressed_block(mouse_x, mouse_y)

                        self.motion_blocks.add(self.get_hashable_block_info(curr_block[0]))

                        self.prime_colors(curr_block)

                if event.type == pygame.MOUSEMOTION: # If mouse is moving

                    if pygame.mouse.get_pressed(num_buttons=5)[0]: # Left click
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        curr_block = self.get_pressed_block(mouse_x, mouse_y)
                        
                        self.motion_blocks.add(self.get_hashable_block_info(curr_block[0]))

                        length = len(self.motion_blocks)
                        if length < 2:
                            self.can_move = False
                        elif length == 2:
                            if not self.can_move:
                                self.prime_colors(curr_block)
                                self.can_move = True
                                continue
                        elif length > 2:
                            self.motion_blocks = set()

                        
                        
                        


            pygame.display.flip()