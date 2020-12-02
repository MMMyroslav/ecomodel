import random
import time


class Ocean:

    def __init__(self, row=35, col=55, prey=250, predator=30, obstacles=75):
        self.numRows = row
        self.numCols = col
        self.size = self.numCols * self.numRows
        self.numPrey = prey
        self.numPredators = predator
        self.numObstacles = obstacles
        self.space = self.__create_ocean_array(self.numCols, self.numRows)

    @staticmethod
    def __create_ocean_array(numCols, numRows):
        return [['.' for _ in range(numCols)] for _ in range(numRows)]

    def get_population(self):
        return int(self.numPrey + self.numPredators + self.numObstacles)

    def __int__(self):
        pass

    def __gt__(self, other):
        pass

    def __del__(self):
        pass

    def get_row(self):
        return self.numRows

    def get_col(self):
        return self.numCols

    def __get_random_coord(self):
        while True:
            rez = Coordinate.lst_key[random.randint(0, self.size - 1)]
            if Coordinate.src_dict[rez] is None:
                Coordinate.src_dict[rez] = 1
                break
        return rez

    def __fill_with_obstacles(self):
        for _ in range(self.numObstacles):
            pos = self.__get_random_coord()
            self.space[pos[0]][pos[1]] = Obstacle(pos)

    def __fill_with_preys(self):
        for _ in range(self.numPrey):
            pos = self.__get_random_coord()
            self.space[pos[0]][pos[1]] = Prey(pos)

    def __fill_with_predators(self):
        for _ in range(self.numPredators):
            pos = self.__get_random_coord()
            self.space[pos[0]][pos[1]] = Predators(pos)

    def fill_water_animals(self):
        self.__fill_with_predators()
        self.__fill_with_preys()
        self.__fill_with_obstacles()

    def __str__(self):
        print()
        print('Prey - {} Predators - {} Obstacles - {}'.
              format(self.numPrey, self.numPredators,
                     self.numObstacles))
        for point in self.space:
            for j in point:
                print('{}'.format(j), end=' ')
            print()
        return '=' * ((self.numCols << 1) - 1)


class Cell:
    water_space = Ocean()

    def __init__(self):
        self.num_cell_y = Cell.water_space.numCols
        self.num_cell_x = Cell.water_space.numRows
        self.current_position = None

    @staticmethod
    def create_life():
        Coordinate.create_keys_coord(Cell.water_space)
        Coordinate.create_src_dict()
        Cell.water_space.fill_water_animals()

    def eat_meat(self):
        pass

    def take_free_position(self):
        pos = True
        while pos:
            pos_x = random.randint(0, self.num_cell_x - 1)
            pos_y = random.randint(0, self.num_cell_y - 1)
            if Coordinate.src_dict[(pos_x, pos_y)] is None:
                pos = (pos_x, pos_y)
                Coordinate.src_dict[(pos_x, pos_y)] = 1
                return pos

    def choose_direction(self):
        combination = []
        food_lst = []

        for point in range(self.current_position[0] - 1,
                           self.current_position[0] + 2):
            if point < 0 or point > self.num_cell_x - 1:
                pass
            else:
                for j in range(self.current_position[1] - 1,
                               self.current_position[1] + 2):
                    if j < 0 or j > self.num_cell_y - 1:
                        pass
                    else:
                        if Coordinate.src_dict[(point, j)] is None:
                            combination.append((point, j))
                        else:
                            if isinstance(
                                    Cell.water_space.space[point][j],
                                    Prey):
                                if not isinstance(
                                        Cell.water_space.space[point][j],
                                        Predators):
                                    food_lst.append((point, j))

        return combination, food_lst

    def set_reproduce_time(self):
        self.time_reproduce = 6

    def increase_life_Pred(self):
        self.time_to_eat = 6

    def reproduce(self, combination):

        if len(combination) <= 1:
            self.set_reproduce_time()
        else:
            step = random.randint(0, len(combination) - 1)
            if isinstance(self, Predators):
                Cell.water_space.space[combination[step][0]][combination[step][1]] = \
                    Predators(combination[step])
            else:
                Cell.water_space.space[combination[step][0]][combination[step][1]] = \
                    Prey(combination[step])

            Coordinate.src_dict[combination[step]] = 1
            self.set_reproduce_time()

    def move_to(self):
        src = self.choose_direction()
        combination = src[0]
        food_lst = src[1]

        if isinstance(self, Predators):
            cur_pos = self.current_position
            check_lst = [(i, j)
                         for i in range(cur_pos[0] - 1, cur_pos[0] + 2) for j
                         in range(cur_pos[1] - 1, cur_pos[1] + 2)]
            interrapt = list(set(food_lst) & set(check_lst))
            if len(interrapt) > 0:
                self.increase_life_Pred()
                dead_fish = interrapt[random.randint(0, len(interrapt)-1)]
                food_lst.remove(dead_fish)
                Coordinate.src_dict[dead_fish] = None
                Cell.water_space.space[dead_fish[0]][dead_fish[1]] = '.'

        if self.time_reproduce == 0:
            self.reproduce(combination)
            return self.current_position
        else:
            if len(combination) < 1:
                return self.current_position
            else:
                step = random.randint(0, len(combination) - 1)
                Coordinate.src_dict[self.current_position] = None
                Cell.water_space.space[self.current_position[0]][self.current_position[1]] = '.'
                self.current_position = combination[step]
                Coordinate.src_dict[self.current_position] = 1
                Cell.water_space.space[self.current_position[0]][self.current_position[1]] = self

                return combination[step]

    @staticmethod
    def lets_go():
        move_lst = []

        for cell in Cell.water_space.space:
            for cells in cell:
                if isinstance(cells, Predators):
                    move_lst.append(cells)
        for fish in move_lst:
            if fish.time_to_eat == 0:
                Coordinate.src_dict[fish.current_position] = None
                Cell.water_space.space[fish.current_position[0]][fish.current_position[1]] = '.'
            else:
                fish.move_to()
                fish.timeToReproduce()
                fish.timeToFeed()

        move_lst = []
        for cell in Cell.water_space.space:
            for cells in cell:
                if not isinstance(cells, Predators):
                    move_lst.append(cells)
        for fish in move_lst:
            if not isinstance(fish, Predators):
                if isinstance(fish, Prey):
                    fish.move_to()
                    fish.timeToReproduce()

        preds = 0
        preys = 0
        for cell in Cell.water_space.space:
            for j in cell:
                if isinstance(j, Predators):
                    preds += 1
                elif isinstance(j, Prey):
                    preys += 1
        Cell.water_space.numPrey = preys
        Cell.water_space.numPredators = preds

    def __del__(self):
        pass

    def __str__(self):
        print()
        print('Prey - {} Predators - {} Obstacles - {}'.
              format(Cell.water_space.numPrey, Cell.water_space.numPredators,
                     Cell.water_space.numObstacles))
        for cell in Cell.water_space.space:
            for j in cell:
                print('{}'.format(j), end=' ')
            print()
        return '=' * ((Cell.water_space.numCols << 1) - 1)


class Obstacle(Cell):

    def __init__(self, coord_obj):
        super(Obstacle, self).__init__()
        self.image = '#'
        self.current_position = coord_obj

    def __str__(self):
        return '{}'.format(self.image)


class Prey(Cell):

    def __init__(self, coord_obj):
        super(Prey, self).__init__()
        self.image = '@'
        self.current_position = coord_obj
        self.time_reproduce = 6

    def timeToReproduce(self):
        self.time_reproduce -= 1

    def __str__(self):
        return '{}'.format(self.image)


class Predators(Prey):

    def __init__(self, coord_obj):
        super(Predators, self).__init__(coord_obj)
        self.image = 'S'
        self.current_position = coord_obj
        self.time_reproduce = 6
        self.time_to_eat = 6

    def timeToFeed(self):
        self.time_to_eat -= 1


class Coordinate:
    lst_key = []
    src_dict = {}

    def __init__(self, obj_water):
        self.src = obj_water

    @staticmethod
    def create_keys_coord(selfie):
        Coordinate.lst_key = [(rows, columns) for rows in range(selfie.get_row())
                              for columns in range(selfie.get_col())]

    @staticmethod
    def create_src_dict():
        Coordinate.src_dict = {lst: None for lst in Coordinate.lst_key}


# ------------------------------------------------------------


a = Cell()
a.create_life()
i = 0
# print(a.water_space)
while i < 1000:
    a.lets_go()
    print(a)
    time.sleep(0.35)
    i += 1
# print(b.lst_key, '\n', b.src_dict)
