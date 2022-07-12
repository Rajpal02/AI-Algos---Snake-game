import numpy as np


def dijkstras(snake_pos, food_pos, frame_size_x, frame_size_y):
    # snake_pos is the start node,  food_pos is the goal node

    # scaling down by 10
    snake_pos = np.array(snake_pos)//10
    food_pos = np.array(food_pos)//10
    # length of frame(X axis) is the number of columns
    max_cols = frame_size_x = frame_size_x//10
    # height of frame(Y axis) is the number of rows
    max_rows = frame_size_y = frame_size_y//10

    # converting to (x,y) pairs
    snake_pos = (snake_pos[1], snake_pos[0])
    food_pos = (food_pos[1], food_pos[0])

    # debug statements
    print("Snake Position:", snake_pos)
    print("Food Position:", food_pos)
    print("Frame Size X:", max_cols)
    print("Frame Size Y:", max_rows)

    # dist dict stores the distance of each node from start node
    dist = {}
    # shortestPathSet stores 'true' for a node if it is included in the shortest path tree else 'false'
    shortestPathSet = {}
    # parent dict stores parent of each node in the shortest path tree
    parent = {}

    # set distance of all nodes to infinity
    # set shortestPathSet[node] = false for all nodes initially
    for i in range(max_rows):
        for j in range(max_cols):
            dist[(i, j)] = float('inf')
            shortestPathSet[(i, j)] = False

    # set distance of source node as 0 to start search, set its parent to -1
    dist[snake_pos] = 0.0
    parent[snake_pos] = -1

    # calculate shortest distance from all nodes to goal
    for i in range(max_rows):
        for j in range(max_cols):
            # pick the node closest to goal based on dist values
            node = min_distance_node(
                dist, shortestPathSet, max_rows, max_cols)
            shortestPathSet[node] = True
            neighbours = get_neighbours(node, max_rows, max_cols)
            # update distance for each neighbour
            for n in neighbours:
                if (shortestPathSet[n] == False and dist[node] != float('inf') and dist[node]+get_weight(node, n, food_pos) < dist[n]):
                    parent[n] = node
                    dist[n] = dist[node]+get_weight(node, n, food_pos)

    # printSoln(dist, parent)
    # print(get_path(parent, food_pos, []))
    # print(get_moves(parent, food_pos))

    return get_moves(parent, food_pos)


def min_distance_node(dist, shortestPathSet, grid_len, grid_height):
    min = float('inf')
    for i in range(grid_len):
        for j in range(grid_height):
            # find node not in shortestPathSet and with minimum distance to goal
            if (shortestPathSet[(i, j)] == False and dist[(i, j)] <= min):
                min = dist[(i, j)]
                min_node = (i, j)
    return min_node


def get_neighbours(node, max_rows, max_cols):
    x, y = node
    # grid orientation - (0,0) is the upper left corner and (max_rows, max_cols) is the lower right corner
    # left neighbour = previous column, same row = node+(0,-10)
    # lower neighbour = same column, next row = node+(10,0)
    # right neighbour = next column, same row = node+(0,10)
    # upper neighbour = same column, previous row = node+(-10,0)

    rows = [0, -1, 0, 1]
    cols = [-1, 0, 1, 0]
    neighbours = []
    for i in range(4):
        if (x+rows[i] >= 0 and x+rows[i] < max_rows and y+cols[i] >= 0 and y+cols[i] < max_cols):
            neighbours.append((x+rows[i], y+cols[i]))
    return neighbours


def get_weight(source, dest, goal):
    x1, y1 = source
    x2, y2 = dest
    xg, yg = goal
    # weight is the manhattan distance between curr node and next node + manhattan distance between next node and goal node
    # this ensures that edges closer to goal have less weights as compared to edges away from goal
    weight = (abs(x1 - x2) + abs(y1 - y2)) + (abs(x2 - xg) + abs(y2 - yg))
    return weight


def print_soln(dist, parent):
    print("Vertex \t Distance from Source \t Path")
    for node, distance in dist.items():
        print(node, end='')
        print("\t\t", end='')
        print(distance, end='')
        print("\t\t", end='')
        print(get_path(parent, node, []))
        print(get_moves(parent, node))
        # printPath(parent, node)
        print('')


# method not used, only used for debugging
def print_path(parent, node):
    if (parent[node] == - 1):
        print(node, end='')
        return
    print(node, end='')
    print_path(parent, parent[node])


def get_path(parent, node,  path):
    if (parent[node] == - 1):
        path.append(node)
        return path
    get_path(parent, parent[node], path)
    path.append(node)
    return path


def get_moves(parent, node):
    path = get_path(parent, node, [])
    moves = []
    for i in range(len(path)-1):
        moves.append(get_direction(path[i], path[i+1]))
    return moves


def get_direction(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    # grid orientation - (0,0) is the upper left corner and (max_rows, max_cols) is the lower right corner
    # left neighbour = previous column, same row = node+(0,-10)
    # lower neighbour = same column, next row = node+(10,0)
    # right neighbour = next column, same row = node+(0,10)
    # upper neighbour = same column, previous row = node+(-10,0)

    # node2 is left neighbour of node1
    if y2 == y1-1:
        return 'LEFT'
    # node2 is lower neighbour of node1
    elif x2 == x1+1:
        return 'DOWN'
    # node2 is right neighbour of node1
    elif y2 == y1+1:
        return 'RIGHT'
    # node2 is upper neighbour of node1
    elif x2 == x1-1:
        return 'UP'


dijkstras((100, 50), (500, 300), 720, 480)
