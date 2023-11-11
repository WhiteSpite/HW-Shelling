from random import choice, shuffle
import matplotlib.pyplot as plt
import numpy as np


GRID_WIDTH = 100
GRID_HEIGHT = 100
NUMBER_OF_RED_CELLS = 4500
NUMBER_OF_BLUE_CELLS = 4500
NUMBER_OF_MIGRATIONS = 100
CELL_MIGRATIONS_PER_SNAPSHOT = 5
PAUSE_DURATION_BETWEEN_SNAPSHOTS = 0.5
CELLS_AROUND_FOR_HAPPINESS = 4
CELL_RADIUS = 2.5


class Cell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.neighbors = []
        self.type = type   # red, blue or empty
    
    def is_happy(self):
        if len(self.neighbors) >= CELLS_AROUND_FOR_HAPPINESS:
            return True
        else:
            return False
        

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.total = width * height
        self.empty_cells = {}
        self.red_cells = {}
        self.blue_cells = {}
        self.color_cells_dicts = [self.red_cells, self.blue_cells]
        self.unhappy_cells = []

    def fill_grid(self, red_cells_num, blue_cells_num):
        empty_cells_num = self.total - red_cells_num - blue_cells_num
        red_types_pull = ['red' for _ in range(red_cells_num)]
        blue_types_pull = ['blue' for _ in range(blue_cells_num)]
        empty_types_pull = ['empty' for _ in range(empty_cells_num)]
        types_pull = red_types_pull + blue_types_pull + empty_types_pull

        for x in range(1, self.width + 1):
            for y in range(1, self.height + 1):
                type = choice(types_pull)
                types_pull.remove(type)
                self.__dict__[type + '_cells'][x, y] = Cell(x, y, type)

    def identify_neighbors(self):
        for cells_dict in self.color_cells_dicts:
            for cell in cells_dict.values():
                cell.neighbors = []
                for y in range(cell.y - 1, cell.y + 2):
                    for x in range(cell.x - 1, cell.x + 2):
                        position = (x, y)
                        if position in cells_dict and cells_dict[position] != cell:
                            cell.neighbors.append(cells_dict[position])

    def identify_unhappy_cells(self):
        self.unhappy_cells = []
        for cells_dict in self.color_cells_dicts:
            for cell in cells_dict.values():
                if not cell.is_happy():
                    self.unhappy_cells.append(cell)
        
    def cells_migrate(self):
        empty_cells = list(self.empty_cells.values())
        shuffle(empty_cells)
        shuffle(self.unhappy_cells)
        
        for empty_cell, unhappy_cell in zip(empty_cells, self.unhappy_cells):
            self.__dict__[unhappy_cell.type + '_cells'][empty_cell.x, empty_cell.y] = unhappy_cell
            self.empty_cells[unhappy_cell.x, unhappy_cell.y] = empty_cell
            del self.__dict__[unhappy_cell.type + '_cells'][unhappy_cell.x, unhappy_cell.y]
            del self.empty_cells[empty_cell.x, empty_cell.y]          
            unhappy_cell.x, empty_cell.x = empty_cell.x, unhappy_cell.x
            unhappy_cell.y, empty_cell.y = empty_cell.y, unhappy_cell.y
    
    def cicle(self, migrations_num):
        update_plot(self.red_cells, self.blue_cells)
        for migration_num in range(migrations_num):
            self.identify_neighbors()
            self.identify_unhappy_cells()
            self.cells_migrate()
            if migration_num % CELL_MIGRATIONS_PER_SNAPSHOT == 0:
                update_plot(self.red_cells, self.blue_cells)
            

def update_plot(red_cells, blue_cells):
    red_x = []
    red_y = []
    blue_x = []
    blue_y = []
    
    for position in red_cells:
        red_x.append(position[0])
        red_y.append(position[1])
    for position in blue_cells:
        blue_x.append(position[0])
        blue_y.append(position[1])
    
    sc_red.set_offsets(np.column_stack((red_x, red_y)))
    sc_blue.set_offsets(np.column_stack((blue_x, blue_y)))
    plt.pause(PAUSE_DURATION_BETWEEN_SNAPSHOTS)


           
plt.ion()
fig, ax = plt.subplots()
sc_red = ax.scatter((1, GRID_WIDTH), (1, GRID_HEIGHT), c='red', s=CELL_RADIUS)          
sc_blue = ax.scatter((1, GRID_WIDTH), (1, GRID_HEIGHT), c='blue', s=CELL_RADIUS)           

grid = Grid(GRID_WIDTH, GRID_HEIGHT)
grid.fill_grid(NUMBER_OF_RED_CELLS, NUMBER_OF_BLUE_CELLS)
grid.cicle(NUMBER_OF_MIGRATIONS)

plt.ioff()
plt.show()
