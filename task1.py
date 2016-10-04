from functools import total_ordering
from numbers import Number


def read_matrices_from_stdin():
    matrix_count = int(input())
    matrices = []
    for _ in range(matrix_count):
        height, width = [int(x) for x in input().split()]
        island_matrix = []
        for _ in range(height):
            line = [int(x) for x in input().split()]
            island_matrix.append(line)
        matrices.append(island_matrix)
    return matrices


@total_ordering
class Infinity(object):
    def __eq__(self, other):
        return isinstance(other, Infinity)

    def __gt__(self, other):
        return isinstance(other, Number)

    def __repr__(self):
        return 'INFINITY'


# noinspection PyAttributeOutsideInit
class IslandSolver:
    def init_island(self, island_matrix):
        self.width = len(island_matrix[0])
        self.height = len(island_matrix)
        self.island_matrix = island_matrix

    def get_water_level_matrix(self):
        infinity = Infinity()
        water_level_matrix = []
        water_level_matrix.append(self.island_matrix[0][:])
        for i in range(1, self.height - 1):
            water_level_line = []
            water_level_line.append(self.island_matrix[i][0])
            for j in range(1, self.width - 1):
                water_level_line.append(infinity)
            water_level_line.append(self.island_matrix[i][self.width - 1])
            water_level_matrix.append(water_level_line)
        water_level_matrix.append(self.island_matrix[-1][:])
        return water_level_matrix

    def find_min_volume_point(self, active_points):
        min_volume_point = None
        min_volume = None
        for point in active_points:
            if min_volume is None or self.water_level_matrix[i][j] < min_volume:
                i, j = point
                min_volume = self.water_level_matrix[i][j]
                min_volume_point = point
        return min_volume_point

    def get_initial_active_points(self):
        active_points = []
        for j in range(0, self.width):
            active_points.append((0, j))
            active_points.append((self.height - 1, j))
        for i in range(1, self.height - 1):
            active_points.append((i, 0))
            active_points.append((i, self.width - 1))
        return active_points

    def get_adjancent_points(self, center_point):
        i, j = center_point
        adjancent_points = []
        if i - 1 >= 0:
            adjancent_points.append((i - 1, j))
        if i + 1 < self.height:
            adjancent_points.append((i + 1, j))
        if j - 1 >= 0:
            adjancent_points.append((i, j - 1))
        if j + 1 < self.width:
            adjancent_points.append((i, j + 1))
        return adjancent_points

    def get_water_capacity(self):
        water_capacity = 0
        for i in range(self.height):
            for j in range(self.width):
                water_capacity += self.water_level_matrix[i][j] - self.island_matrix[i][j]
        return water_capacity

    def solve(self, island_matrix):
        self.init_island(island_matrix)
        self.water_level_matrix = self.get_water_level_matrix()
        active_points = self.get_initial_active_points()
        while active_points:
            min_volume_point = self.find_min_volume_point(active_points)
            active_points.remove(min_volume_point)
            for adjacent_point in self.get_adjancent_points(min_volume_point):
                i, j = adjacent_point
                min_volume_point_water_level = (self.water_level_matrix[min_volume_point[0]]
                                                [min_volume_point[1]])
                old_adjancent_point_water_level = self.water_level_matrix[i][j]
                new_adjancent_point_water_level = max(
                    self.island_matrix[i][j],
                    min(old_adjancent_point_water_level, min_volume_point_water_level)
                )
                if new_adjancent_point_water_level != old_adjancent_point_water_level:
                    self.water_level_matrix[i][j] = new_adjancent_point_water_level
                    active_points.append(adjacent_point)
        return self.get_water_capacity()


def main():
    island_solver = IslandSolver()
    for matrix in read_matrices_from_stdin():
        water_capacity = island_solver.solve(matrix)
        print(water_capacity)


if __name__ == '__main__':
    main()
