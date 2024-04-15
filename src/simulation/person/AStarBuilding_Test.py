from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def main():

    matrix = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    grid = Grid(matrix=matrix)
    start = grid.node(1, 1)
    end = grid.node(4, 3)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    for node in path:
        print(node.x, node.y)


if __name__ == '__main__':
    main()
