import itertools
import random

import numpy as np

'''
class Solution
stores a possible visit order, provides an operation to get the best neighbors by checking all possible 'neighbor'
generated by swapping two elements

Data:
sequence: stores the visit order, a permutation of 1, 2, ..., n

Operations:
def evaluate(landscape): get the cost in given landscape
def find_better_solution(landscape): get the neighbor with smallest cost in given landscape


class Landscape
stores a tsp problem to solve

Data:
map_data: 
map_data[i, j] = 1 if pos(i, j) is a city
                 0 if nothing in pos(i, j)
(distance between two cities is calculated by manhattan method)

map_distance_matrix:
map_distance_matrix[a, b] = the distance between city a and city b

pos_of_city:
pos_of_city[i] = the position of city i in 2 dim
'''


def manhattan_distance(pos_a, pos_b): return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


class Solution:
    sequence = []
    map_cities = 0

    def __init__(self, map_cities, copy_from=None):
        if copy_from is None:
            self.map_cities = map_cities
            self.sequence = [i for i in range(map_cities)]
            random.shuffle(self.sequence)
        else:
            self.sequence = copy_from.sequence.copy()
            self.map_cities = copy_from.map_cities

    def _generate_neighbors(self):
        if self.map_cities <= 15:
            swap_pairs = itertools.combinations(self.sequence, 2)
        else:
            swap_pairs = []
            for i in range(100):
                pair = (random.randint(0, self.map_cities - 1), random.randint(0, self.map_cities - 1))
                swap_pairs.append(pair)
        neighbors = []
        for pair in swap_pairs:
            n_sequence = self.sequence.copy()
            n_sequence[pair[0]] = self.sequence[pair[1]]
            n_sequence[pair[1]] = self.sequence[pair[0]]
            new_neighbor = Solution(map_cities=0, copy_from=self)
            new_neighbor.sequence = n_sequence
            neighbors.append(new_neighbor)
        return neighbors

    def evaluate(self, landscape):
        if landscape.map_cities != self.map_cities:
            print('[E] Solution length invalid')
            return
        total_distance = 0
        for i in range(1, self.map_cities):
            total_distance += landscape.map_distance_matrix[self.sequence[i - 1], self.sequence[i]]
        total_distance += landscape.map_distance_matrix[self.sequence[self.map_cities - 1], self.sequence[0]]
        return total_distance

    def find_better_solution(self, landscape):
        neighbors = self._generate_neighbors()
        best_neighbor = neighbors[0]
        best_neighbor_value = neighbors[0].evaluate(landscape)
        for neighbor in neighbors:
            value = neighbor.evaluate(landscape)
            if value < best_neighbor_value:
                best_neighbor_value = value
                best_neighbor = neighbor
        return best_neighbor


class Landscape:
    map_width = map_cities = 0
    map_data = map_distance_matrix = None

    pos_of_city = []

    def initialize_map(self):
        self.map_data = np.zeros(shape=[self.map_width, self.map_width])
        self.map_distance_matrix = np.zeros(shape=[self.map_cities, self.map_cities])
        self.pos_of_city.clear()

        coordinates = []
        # randomly select cities from all positions (x, y) belongs to R^(WxW)
        for i in range(self.map_width):
            for j in range(self.map_width):
                coordinates.append((i, j))
        for i in range(self.map_cities):
            pos = random.choice(coordinates)
            # cannot select this pos again
            coordinates.remove(pos)
            self.pos_of_city.append(pos)
            self.map_data[pos] = 1
        # generate distance matrix, dis[i, j] = distance between city i and j
        for i in range(self.map_cities):
            for j in range(self.map_cities):
                pos_city_a = self.pos_of_city[i]
                pos_city_b = self.pos_of_city[j]
                self.map_distance_matrix[i, j] = manhattan_distance(pos_city_a, pos_city_b)

    def __init__(self, map_width, map_cities):
        self.map_width = map_width
        self.map_cities = map_cities

        self.initialize_map()