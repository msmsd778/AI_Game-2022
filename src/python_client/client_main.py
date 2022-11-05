import random
from base import BaseAgent, Action
from MainClass import Node


class Agent(BaseAgent):

    SCORE_DIAMOND = [
        ('11', 50),
        ('12', 200),
        ('13', 100),
        ('14', 0),
        ('21', 100),
        ('22', 50),
        ('23', 200),
        ('24', 100),
        ('31', 50),
        ('32', 100),
        ('33', 50),
        ('34', 200),
        ('41', 250),
        ('42', 59),
        ('43', 100),
        ('44', 50),
    ]

    openList = []
    closedList = []
    cost_grid = []
    diamonds = []
    walls = []
    moved = False
    path = []

    def do_turn(self) -> Action:
        
        agent = self.get_agent()
        self.diamonds = []
        self.get_diamonds()
        if self.moved == False:
            self.path = []
            self.get_diamonds()
            nd = self.get_near_diamonds(self.diamonds, agent[0], agent[1])
            print(nd)
            if len(nd) == 0:
                # print('hello')
                dest = self.get_nearest_diamond(self.diamonds)
            else:
                dest = nd[0]  # calculate sequence later!           
            found = self.A_star(agent, dest)
            if found:
                self.moved = True
        if len(self.path) == 0:
            return Action.NOOP       
        
        x = self.path.pop(0)
        return x


        # return Action.DOWN

    def get_agent(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if 'A' in self.grid[i][j]:
                    return (i,j)

    def get_diamonds(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if ('1' in self.grid[i][j]) or ('2' in self.grid[i][j]) or ('3' in self.grid[i][j]) or ('4' in self.grid[i][j]):
                    self.diamonds.append({self.grid[i][j]: (i,j)})
    
    def get_near_diamonds(self, diamonds, x, y):
        near_diamonds = []
        for i in range(len(diamonds)):
            if list(diamonds[i].values())[0][0] <= x+2 and list(diamonds[i].values())[0][0] >= x-2 and list(diamonds[i].values())[0][1] <= y+2 and list(diamonds[i].values())[0][1] >= y-2:
                near_diamonds.append(diamonds[i])
        return near_diamonds
    
    def get_barriers(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if 'W' in self.grid[i][j]:
                    self.walls.append((i,j))

    # def is_reachable(self, agent, diamond):
    #     """check turn, score, walls"""
        

    # def find_route(self, agent, diamond):
        # """return score"""
        # start = (0,0)
        # end = (self.grid_height-1, self.grid_width-1)
        # self.openSet.append(start)
        # if len(self.openSet) > 0:
        #     #keep going
        #     winner = 0
        #     for i in range(i, len(self.openSet)):
        #         if self.openSet[i].f < self.openSet[winner].f:
        #             winner = i
                    
        #     current = self.openSet[winner]
                    
        #     if current == end:
        #         return Action.NOOP
        #     else:
        #         closedSet.append(current)
        #         # Done coding from A* video until Part 1 min 25
            
        # else:
        #     #no solution
        #     pass

    def get_nearest_diamond(self, diamonds):
        '''implemented with diagonal distance as the heuristic function'''
        x = self.get_agent()[0]
        y = self.get_agent()[1]
        D = 1
        D2 = 2
        h = 2**32
        for i in range(len(diamonds)):  
            dx = abs(x - list(diamonds[i].values())[0][0])
            dy = abs(y - list(diamonds[i].values())[0][1])
            tmp = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
            if tmp < h:
                h = tmp
                coordinate = (list(diamonds[i].values())[0][0],list(diamonds[i].values())[0][1])
        return coordinate

    def A_star(self, agent, diamond):
        currentNode = Node(agent, 0, 0)
        self.openList.append(currentNode)
        found = False

        for wall in self.walls:
            self.closedList.append(Node(wall, 1,2))

        while len(self.openList) != 0 and not found:
            min_f = 1000
            min_node = None
            for node in self.openList:
                if node.f <= min_f:
                    min_f = node.f
                    min_node = node

            self.path.append(self.get_direction(currentNode, min_node))
            currentNode = min_node
            self.openList.remove(min_node)
            self.closedList.append(min_node)

            if currentNode.cords == diamond:
                found = True
                break
            
            neighbors = []
            for i in range(currentNode.cords[0] - 1, currentNode.cords[0] +1):
                if i < 0 or i > self.grid_height:
                    continue
                for j in range(currentNode.cords[1] -1 , currentNode.cords[1] +1):
                    if j < 0 or j > self.grid_width:
                        continue
                    if (i,j) == currentNode.cords:
                        continue
                    
                    if abs(currentNode.cords[0] - i) == 0 and abs(currentNode.cords[1] - j) == 1:
                        neighbors.append(Node((i,j), currentNode.g + 1, self.heuristic(currentNode, diamond)))
                    elif abs(currentNode.cords[0] - i) == 1 and abs(currentNode.cords[1] - j) == 0:
                        neighbors.append(Node((i,j), currentNode.g + 1, self.heuristic(currentNode, diamond)))
                    else:
                        neighbors.append(Node((i,j), currentNode.g + 2, self.heuristic(currentNode, diamond)))

                for n in neighbors:
                    if n in self.closedList and n in self.openList:
                        continue
                    self.openList.append(n)
        return found

    
    def heuristic(self, start, goal):
        D = 1
        D2 = 2
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
            
    def get_direction(self, current, next):
        if next.cords[0] - current.cords[0] == 1 and next.cords[1] - current.cords[1] == 0:
            return Action.DOWN
        if next.cords[0] - current.cords[0] == -1 and next.cords[1] - current.cords[1] == 0:
            return Action.UP
        if next.cords[0] - current.cords[0] == 0 and next.cords[1] - current.cords[1] == 1:
            return Action.RIGHT
        if next.cords[0] - current.cords[0] == 0 and next.cords[1] - current.cords[1] == -1:
            return Action.LEFT
        if next.cords[0] - current.cords[0] == 1 and next.cords[1] - current.cords[1] == 1:
            return Action.DOWN_RIGHT
        if next.cords[0] - current.cords[0] == 1 and next.cords[1] - current.cords[1] == -1:
            return Action.DOWN_LEFT
        if next.cords[0] - current.cords[0] == -1 and next.cords[1] - current.cords[1] == 1:
            return Action.UP_RIGHT
        if next.cords[0] - current.cords[0] == -1 and next.cords[1] - current.cords[1] == -1:
            return Action.UP_LEFT


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)


# These are bullshit. I was trying to implement the a* in a seprate part but I regretted
# Real shit is in "find route" function. Focus on that!

# class AStarGraph(object):
#     def __init__(self):
#         self.barriers = Agent.get_barriers
    
#     def heuristic(self, start, goal):
#         D = 1
#         D2 = 2
#         dx = abs(start[0] - goal[0])
#         dy = abs(start[1] - goal[1])
#         return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    
#     def get_vertex_neighbors(self, pos):
#         n = []
#         for dx, dy, in [(1, 0), (-1, 0), (0, -1), (1, 1)]:
#             x2 = pos[0] + dx
#             y2 = pos[1]+ dy
#             if x2 < 0 or x2 > 5 or y2 > 5