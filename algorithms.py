import random
import heapq
from collections import deque

# ===================================================================================
# PHAN 1: CAC THIET LAP CO BAN VA LOGIC SINH ME CUNG
# ===================================================================================

# Kich thuoc me cung (so hang, so cot)
ROWS, COLS = 10, 10

# Huong: (dx, dy, tuong hien tai, tuong doi dien)
# Tuong: 0: tren, 1: phai, 2: duoi, 3: trai
DIRS = [(0, -1, 3, 1), (1, 0, 2, 0), (0, 1, 1, 3), (-1, 0, 0, 2)]

def in_bounds(x, y):
    """Kiem tra mot o co nam trong gioi han me cung khong"""
    return 0 <= x < ROWS and 0 <= y < COLS

def generate_maze_recursive(x, y, maze, visited):
    """Ham de quy de sinh me cung"""
    visited[x][y] = True
    dirs_shuffled = DIRS[:]
    random.shuffle(dirs_shuffled)
    for dx, dy, wall, opposite in dirs_shuffled:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and not visited[nx][ny]:
            maze[x][y][wall] = False
            maze[nx][ny][opposite] = False
            generate_maze_recursive(nx, ny, maze, visited)

def create_new_maze():
    """Tao ra mot me cung moi hoan chinh voi diem bat dau/ket thuc ngau nhien"""
    maze = [[[True, True, True, True] for _ in range(COLS)] for _ in range(ROWS)]
    visited = [[False] * COLS for _ in range(ROWS)]
    start_gen_x, start_gen_y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
    generate_maze_recursive(start_gen_x, start_gen_y, maze, visited)
    
    start_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    while True:
        end_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if end_pos != start_pos: 
            break
    return maze, start_pos, end_pos

# ===================================================================================
# PHAN 2: CAC THUAT TOAN TIM DUONG (DA CHUYEN THANH GENERATOR)
# ===================================================================================

class Node:
    """Lop dai dien cho mot o trong qua trinh tim kiem"""
    def __init__(self, position, parent=None):
        self.position, self.parent, self.g, self.h, self.f = position, parent, 0, 0, 0
    def __lt__(self, other): 
        return self.f < other.f

def manhattan_distance(p1, p2):
    """Tinh khoang cach Manhattan (heuristic cho A*)"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(node_pos, maze):
    """Lay cac o hang xom hop le (khong co tuong chan)"""
    x, y = node_pos
    neighbors = []
    directions = [(-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)] # Len, Phai, Xuong, Trai
    for dx, dy, wall_idx in directions:
        if not maze[x][y][wall_idx]:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny): 
                neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(current_node):
    """Xay dung lai duong di tu node ket thuc nguoc ve node bat dau"""
    path = []
    while current_node:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1] # Dao nguoc de co duong di tu start -> end

# Moi ham thuat toan se `yield` de co the truc quan hoa tung buoc
def a_star_animated(maze, start, goal):
    start_node = Node(start)
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()
    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)
        if current_node.position == goal:
            path = reconstruct_path(current_node)
            yield closed_set, path
            return
        yield closed_set, None
        for neighbor_pos in get_neighbors(current_node.position, maze):
            if neighbor_pos in closed_set: continue
            neighbor_node = Node(neighbor_pos, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = manhattan_distance(neighbor_pos, goal)
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            if any(n.position == neighbor_pos and neighbor_node.g >= n.g for n in open_list):
                continue
            heapq.heappush(open_list, neighbor_node)
    yield closed_set, None # Khong tim thay

def bfs_animated(maze, start, goal):
    queue = deque([Node(start)])
    visited = {start}
    parent_map = {start: None}
    while queue:
        current_node = queue.popleft()
        if current_node.position == goal:
            path = []
            pos = goal
            while pos is not None:
                path.append(pos)
                pos = parent_map[pos]
            yield visited, path[::-1]
            return
        yield visited, None
        for neighbor_pos in get_neighbors(current_node.position, maze):
            if neighbor_pos not in visited:
                visited.add(neighbor_pos)
                parent_map[neighbor_pos] = current_node.position
                queue.append(Node(neighbor_pos))
    yield visited, None # Khong tim thay

def dfs_animated(maze, start, goal):
    stack = [Node(start)]
    visited = set()
    parent_map = {start: None}
    while stack:
        current_node = stack.pop()
        if current_node.position in visited: continue
        visited.add(current_node.position)
        if current_node.position == goal:
            path = []
            pos = goal
            while pos is not None:
                path.append(pos)
                pos = parent_map[pos]
            yield visited, path[::-1]
            return
        yield visited, None
        for neighbor_pos in reversed(get_neighbors(current_node.position, maze)):
            if neighbor_pos not in visited:
                parent_map[neighbor_pos] = current_node.position
                stack.append(Node(neighbor_pos))
    yield visited, None # Khong tim thay
