import random
from base import BaseAgent, Action


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

    openSet = []
    closedSet = []
    cost_grid = []
    diamonds = dict()
    walls = []

    def do_turn(self) -> Action:
        # agent = self.get_agent()
        # print(agent)
        # print(self.get_near_diamonds(self.get_diamonds(),agent[0], agent[1]))   
        return Action.DOWN

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

    def is_reachable(self, agent, diamond):
        """check turn, score, walls"""
        

    def find_route(self, agent, diamond):
        """return score"""
        start = (0,0)
        end = (self.grid_height-1, self.grid_width-1)
        self.openSet.append(start)
        if len(self.openSet) > 0:
            #keep going
            winner = 0
            for i in range(i, len(self.openSet)):
                if self.openSet[i].f < self.openSet[winner].f:
                    winner = i
                    
            current = self.openSet[winner]
                    
            if current == end:
                return Action.NOOP
            else:
                closedSet.append(current)
                # Done coding from A* video until Part 1 min 25
            
        else:
            #no solution
            pass

    def get_nearest_diamond(self, agent, diamonds):
        #implemented with diagonal distance as the heuristic function
        x = self.get_agent[0]
        y = self.get_agent[1]
        D = 1
        D2 = 2
        h = 2**32
        for i in range(len(diamonds)):  
            dx = abs(x - list(l[i].values())[0][0])
            dy = abs(y - list(l[i].values())[0][1])
            tmp = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
            if tmp < h:
                h = tmp
                coordinate = (list(l[i].values())[0][0],list(l[i].values())[0][1])
        return coordinate


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