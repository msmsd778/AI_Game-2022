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
    diamonds = []
    # walls = []
    # moved = False
    path = []
    dest = ()
    grid_nodes = list()
    direction = []

    def do_turn(self) -> Action:
        
        
        



        if len(self.direction) == 0:
            self.path = []
            self.grid_nodes = []
            self.diamonds = []
            self.create_grid_nodes()
            self.get_barriers()
            self.get_diamonds()
            agent = self.get_agent()

            self.closedList = []
            self.openList = []

            nd = self.get_near_diamonds(self.diamonds, agent[0], agent[1])
            if len(nd) == 0:
                self.dest = self.get_nearest_diamond(self.diamonds)
            else:
                self.dest = list(nd[0].values())[0]  # calculate sequence later!
                           
            found = self.A_star(agent, self.dest)
            print(found)
            # if found:

            #     # self.moved = True
            # print(self.path)
            # print(self.dest)

       
        
        
        x = self.direction.pop(0)
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

    def create_grid_nodes(self):

        self.grid_nodes = [None] * self.grid_height
        
        for i in range(self.grid_height):
            self.grid_nodes[i] = [None] * self.grid_width

        for i in range(self.grid_height):
            for j in range(self.grid_width):
                self.grid_nodes[i][j] = Node((i,j), 0, 0)
                
    
    def get_barriers(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if 'W' in self.grid[i][j]:
                    self.grid_nodes[i][j].is_wall = True
                    # self.closedList.append(Node((i,j),2,3))


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

        currentNode = self.grid_nodes[agent[0]][agent[1]]
        self.openList.append(currentNode)
        found = False
        
        

        while len(self.openList) != 0 and not found:
            min_node = self.openList[0]
            for node in self.openList:
                if node.f <= min_node.f:
                    min_node = node


            # if currentNode.cords != min_node.cords: 
            #     d = self.get_direction(currentNode, min_node)
            #     print(d)
            #     self.path.append(d)
            currentNode = min_node
            self.openList.remove(currentNode)
            self.closedList.append(currentNode)

            if currentNode.cords == diamond:
                found = True
                # find the path here!
                self.path = []
                temp = currentNode
                self.path.append(temp)
                while(temp.previous):
                    self.path.append(temp.previous)
                    temp = temp.previous

                self.find_direction()
                break
            
            neighbors = []
            for i in range(currentNode.cords[0] - 1, currentNode.cords[0] +2):
                if i < 0 or i > self.grid_height -1:
                    continue
                for j in range(currentNode.cords[1] -1 , currentNode.cords[1] +2):
                    if j < 0 or j > self.grid_width -1 :
                        continue
                    if (i,j) == currentNode.cords:
                        continue
                    
                    neighbors.append(self.grid_nodes[i][j])

                    # if abs(currentNode.cords[0] - i) == 0 and abs(currentNode.cords[1] - j) == 1:
                    #     # node = self.grid_nodes[i][j]
                    #     node.g = currentNode.g + 1
                    #     # node.h = self.heuristic((i,j), diamond)
                    #     # node.f = self.g + self.h
                    # elif abs(currentNode.cords[0] - i) == 1 and abs(currentNode.cords[1] - j) == 0:
                    #     # neighbors.append(self.grid_nodes[i][j], currentNode.g + 1, self.heuristic((i,j), diamond)))
                    #     # node = self.grid_nodes[i][j]
                    #     node.g = currentNode.g + 1
                    #     # node.h = self.heuristic((i,j), diamond)
                    #     # node.f = self.g + self.h
                    # else:
                    #     # neighbors.append(self.grid_nodes[i][j], currentNode.g + 2, self.heuristic((i,j), diamond)))
                    #     # node = self.grid_nodes[i][j]
                    #     node.g = currentNode.g + 2
                        # node.h = self.heuristic((i,j), diamond)
                        # node.f = self.g + self.h

            for n in neighbors:
                tempG = 0

                if abs(currentNode.cords[0] - n.cords[0]) == 0 and abs(currentNode.cords[1] - n.cords[1]) == 1:
                        tempG = currentNode.g + 1                       
                elif abs(currentNode.cords[0] - n.cords[0]) == 1 and abs(currentNode.cords[1] - n.cords[1]) == 0:
                        tempG = currentNode.g + 1                       
                else:
                        tempG = currentNode.g + 2



                if n not in self.closedList and not n.is_wall:
                    if n in self.openList:
                        if tempG < n.g:
                            n.g = tempG
                    else:
                        n.g = tempG
                        self.openList.append(n)

                    n.h = self.heuristic(n.cords, diamond)
                    n.f = n.g + n.h
                    n.previous = currentNode

                # for c in self.closedList:
                #     if n.cords == c.cords:
                #         ok = False
                #         break
                # for o in self.openList:
                #     if n.cords == o.cords:
                #         if n.g < o.g:
                #             o.g = n.g
                #         ok = False
                #         break
                # for w in self.walls:
                #     if n.cords == w:
                #         ok = False
                #         break
                # if ok:
                
            
            for n in self.openList:
                print(n.cords , n.f , n.g, n.h)
            print('dest: ', self.dest)
            # print('walls', self.walls)
            print('__________________________')
        return found

    
    def heuristic(self, start, goal):
        D = 1
        D2 = 2
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

            
    def get_direction(self, current, next):

        print('current', current.cords)
        print('next', next.cords)

        if next.cords[0] - current.cords[0] == 1 and next.cords[1] - current.cords[1] == 0:
            return Action.DOWN
        elif next.cords[0] - current.cords[0] == -1 and next.cords[1] - current.cords[1] == 0:
            return Action.UP
        elif next.cords[0] - current.cords[0] == 0 and next.cords[1] - current.cords[1] == 1:
            return Action.RIGHT
        elif next.cords[0] - current.cords[0] == 0 and next.cords[1] - current.cords[1] == -1:
            return Action.LEFT
        elif next.cords[0] - current.cords[0] == 1 and next.cords[1] - current.cords[1] == 1:
            return Action.DOWN_RIGHT
        elif next.cords[0] - current.cords[0] == 1 and next.cords[1] - current.cords[1] == -1:
            return Action.DOWN_LEFT
        elif next.cords[0] - current.cords[0] == -1 and next.cords[1] - current.cords[1] == 1:
            return Action.UP_RIGHT
        elif next.cords[0] - current.cords[0] == -1 and next.cords[1] - current.cords[1] == -1:
            return Action.UP_LEFT
        else:
            return Action.NOOP

    def find_direction(self):
        for i in range(len(self.path) - 1, 0, -1):
            self.direction.append(self.get_direction(self.path[i], self.path[i-1]))


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
