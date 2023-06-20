from heapq import *

cols, rows = 23, 13
TILE = 50

grid = ['88888888888888888888888',
        '88888888888888888888888',
        '33333333333333333333333',
        '19919919911991991991991',
        '19919919911991991991991',
        '19919919911991991991991',
        '19919911111991991991991',
        '19919919911991111991991',
        '11111119911991111991111',
        '19919919919999911991991',
        '19919919919999911111991',
        '19919919919999919911991',
        '19919911111111119911991']

grid = [[int(char) for char in string] for string in grid]


class path_finder:
    def __init__(self):
        pass

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def final_path_detector(self):
        """
        calculates the shortest distance between from the starting path to reach the target point
        :return: the path in which the agv runs
        """
        try:
            graph = {}
            for y, row in enumerate(grid):
                for x, col in enumerate(row):
                    graph[(x, y)] = graph.get((x, y), []) + self.get_next_nodes(x, y)

            # BFS settings
            #agvs = int(input("ENTER THE NO OF AGVS : "))

            endx = int(input("X : "))
            endy = int(input("Y : "))
            startx = int(input("SX : "))
            starty = int(input("SY : "))
            start = (startx, starty)
            goal = (endx, endy)
            queue = []
            heappush(queue, (0, start))
            cost_visited = {start: 0}
            visited = {start: None}
            while True:
                # Dijkstra logic
                if queue:
                    cur_cost, cur_node = heappop(queue)
                    if cur_node == goal:
                        queue = []
                        continue

                    next_nodes = graph[cur_node]
                    for next_node in next_nodes:
                        neigh_cost, neigh_node = next_node
                        new_cost = cost_visited[cur_node] + neigh_cost

                        if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                            priority = new_cost + self.heuristic(neigh_node, goal)
                            heappush(queue, (priority, neigh_node))
                            cost_visited[neigh_node] = new_cost
                            visited[neigh_node] = cur_node

                path_head, path_segment = cur_node, cur_node
                found_path = []
                while path_segment:
                    path_segment = visited[path_segment]
                    found_path.append(path_segment)
                # found path is reversed in order to arrange the data points in particular order to find the path to
                # reach the target position
                found_path.reverse()
                if found_path[-1] in [(endx, endy - 1), (endx, endy + 1),  (endx-1, endy), (endx+1, endy)]:
                    final_path = found_path[1:]
                    print("EXECUTING PATH : ", final_path)
                    break
                        # Final path in which the agv runs
            return final_path

        except Exception as e:
            print("FINAL PATH DETECTOER", e)
