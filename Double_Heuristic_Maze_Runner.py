import random

# Directions: up, right, down, left
DIRS = [(-1,0), (0,1), (1,0), (0,-1)]
DIR_NAMES = ['U', 'R', 'D', 'L']

def generate_maze(width, height):
    maze = [['#']*width for _ in range(height)]
    def carve(x, y):
        maze[y][x] = '.'
        dirs = DIRS[:]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == '#':
                maze[y+dy][x+dx] = '.'
                carve(nx, ny)
    carve(1, 1)
    maze[1][1] = 'S'
    maze[height-2][width-2] = 'G'
    return maze

def print_maze(maze, player_pos, ai_pos):
    rendered = [row[:] for row in maze]
    px, py = player_pos
    ax, ay = ai_pos
    if (py, px) != (ay, ax):
        rendered[py][px] = 'P'
        rendered[ay][ax] = 'A'
    else:
        rendered[py][px] = '*'
    print('\n'.join(''.join(row) for row in rendered))
    print()

def neighbors(maze, x, y):
    nb = []
    for dx, dy in DIRS:
        nx, ny = x+dx, y+dy
        if maze[ny][nx] in ('.', 'G'):
            nb.append((nx, ny))
    return nb

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# Heuristic 1: Greedy Manhattan Distance
def ai_greedy(maze, pos, goal):
    options = neighbors(maze, *pos)
    best = min(options, key=lambda n: manhattan(n, goal))
    return best

# Heuristic 2: Wall Follower (Left-hand rule)
def ai_wall_follower(maze, pos, direction_idx, visited, goal):
    # Get current facing, try left, forward, right, back
    for i in [3, 0, 1, 2]:  # left, forward, right, back
        ndir = (direction_idx + i) % 4
        dx, dy = DIRS[ndir]
        nx, ny = pos[0] + dx, pos[1] + dy
        if maze[ny][nx] in ('.', 'G'):
            return (nx, ny), ndir
    # Fallback: don't move
    return pos, direction_idx

def find_goal(maze):
    for y, row in enumerate(maze):
        for x, v in enumerate(row):
            if v == 'G':
                return (x, y)

def play():
    width, height = 15, 11
    maze = generate_maze(width, height)
    player_pos = [1, 1]
    ai_pos = [1, 1]
    goal = find_goal(maze)
    ai_dir_idx = 1  # Initially facing right
    visited = set()
    print("Choose AI Heuristic: 1 - Greedy Manhattan, 2 - Wall Follower")
    ai_heur = input("Enter 1 or 2: ").strip()
    print_maze(maze, player_pos, ai_pos)
    while True:
        # Player move
        move = input("Move (WASD): ").upper()
        dx, dy = 0, 0
        if move == 'W': dx, dy = 0, -1
        elif move == 'S': dx, dy = 0, 1
        elif move == 'A': dx, dy = -1, 0
        elif move == 'D': dx, dy = 1, 0
        else:
            print("Invalid move.")
            continue
        nx, ny = player_pos[0]+dx, player_pos[1]+dy
        if maze[ny][nx] in ('.', 'G'):
            player_pos = [nx, ny]
        else:
            print("Blocked!")
        if tuple(player_pos) == goal:
            print_maze(maze, player_pos, ai_pos)
            print("You win!")
            break
        # AI move
        if ai_heur == '1':
            ai_pos = list(ai_greedy(maze, tuple(ai_pos), goal))
        else:
            (ax, ay), ai_dir_idx = ai_wall_follower(maze, tuple(ai_pos), ai_dir_idx, visited, goal)
            ai_pos = [ax, ay]
        if tuple(ai_pos) == goal:
            print_maze(maze, player_pos, ai_pos)
            print("AI wins!")
            break
        print_maze(maze, player_pos, ai_pos)

if __name__ == "__main__":
    play()