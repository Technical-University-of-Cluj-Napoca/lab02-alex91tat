from collections import deque
import sys

def read_maze(filename: str) -> list[list[str]]:
    maze = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        maze.append(line.strip())

    return maze

def find_start_and_target(maze: list[list[str]]) -> list[tuple[int, int]]:
    start = end = None
    for r, row in enumerate(maze):
        for c, value in enumerate(row):
            if value == 'S':
                start = (r, c)
            elif value == 'T':
                end = (r, c)

    return [start, end]

def get_neighbors(maze: list[list[str]], position: tuple[int, int]) -> list[tuple[int, int]]:
    neighbors = []
    direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dire in direction:
        row, column = position[0] + dire[0], position[1] + dire[1]
        if 0 <= row < len(maze) and 0 <= column < len(maze[row]) and maze[row][column] != '#':
            neighbors.append((row, column))

    return neighbors

def bfs(maze: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current_node, path = queue.popleft()

        if current_node == target:
            return path
        
        for neighbor in get_neighbors(maze, current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    return None

def dfs(maze: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
    stack = [(start,[start])]
    visited = {start}
    
    while stack:
        current_node, path = stack.pop()
        
        if current_node == target:
            return path
        
        for neighbor in get_neighbors(maze, current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                stack.append((neighbor, new_path))
        
    return None

def print_maze_with_path(maze: list[list[str]], path: list[tuple[int, int]]) -> None:
    RED = "\033[91m"
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"

    maze_copy = [list(row) for row in maze]
    for r, c in path:
        if maze_copy[r][c] == 'S':
            maze_copy[r][c] = f"{GREEN}S{RESET}"
        elif maze_copy[r][c] == 'T':
            maze_copy[r][c] = f"{YELLOW}T{RESET}"
        else:
            maze_copy[r][c] = f"{RED}*{RESET}"

    for row in maze_copy:
        print(''.join(row))

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.exit(1)

    algorithm_name = sys.argv[1].lower()
    file_name = sys.argv[2]

    try:
        maze = read_maze(file_name)
        start, target = find_start_and_target(maze)

        if start is None:
            print("error: could not find Start")
            sys.exit(1)
        if target is None:
            print("error: could not find Target")
            sys.exit(1)

    except FileNotFoundError:
        print("error: file not found")
        sys.exit(1)
    except Exception as e:
        print("error occurred reading the maze")
        sys.exit(1)


    path = None
    if algorithm_name == 'bfs':
        path = bfs(maze, start, target)
    elif algorithm_name == 'dfs':
        path = dfs(maze, start, target)
    else:
        print("error: unknown algorithm")
        sys.exit(1)

    if path:
        print_maze_with_path(maze, path)
    else:
        print("no path found from Start to Target.")