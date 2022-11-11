import random
from base import BaseAgent, Action
from MainClass import Node
from itertools import permutations
import math

class Agent(BaseAgent):

    DIAMOND_SCORES = {
        '01': 50,
        '02': 0,
        '03': 0,
        '04': 0,
        '11': 50,
        '12': 200,
        '13': 100,
        '14': 0,
        '21': 100,
        '22': 50,
        '23': 200,
        '24': 100,
        '31': 50,
        '32': 100,
        '33': 50,
        '34': 200,
        '41': 250,
        '42': 50,
        '43': 100,
        '44': 50,
    }
    
    COLLECTABLES_SCORE = {
        '*': -20,
        'g': 10,
        'r': 10,
        'y': 10
    }
    
    count = 0
    openList = []
    closedList = []
    diamonds = []
    collected_diamonds = '0'
    collected_items = ''
    ignored = []
    keys = []
    path = []
    dest = ()
    grid_nodes = list()
    direction = []
    collected_keys = []
    total_clusters = []
    clustering_ignored = []
    clustered = False
    clusters_scores = []
    cluster_centers = []
    clusters_distance = []
    x = []
    ratios = []

    def do_turn(self) -> Action:
        
        if len(self.direction) == 0:
            self.path = []
            self.grid_nodes = []
            self.diamonds = []
            self.closedList = []
            self.openList = []
            diamond_type = ''

            self.create_grid_nodes()
            agent = self.get_agent()
            self.get_diamonds()
            self.get_items()
            if not self.clustered:
                self.clustering()
                self.clustered = True
                for i in self.total_clusters:
                    self.clusters_scores.append(self.cluster_max_score(i))
                    self.cluster_centers.append(self.find_center(i))

            if len(self.clusters_scores) > 0:
                self.ratios = self.distance_to_center()

            if len(self.diamonds) == 0:
                pass

            
            
            if len(self.x) == 0 and len(self.ratios) != 0:  
                idx = self.ratios.index(max(self.ratios)) # find the index of max ratio
                self.x = self.clusters_scores.pop(idx)[0]
                self.cluster_centers.pop(idx)
                self.ratios.pop(idx)
            if len(self.x) > 0:
                i = self.x.pop(0)
                self.dest = i[1]            
                found = self.A_star(agent, self.dest)
            else:
                if len(self.keys) > 0:
                    self.dest = self.keys.pop(0)
                    found = self.A_star(agent, self.dest)
                else:
                    return Action.NOOP
            if not found and self.dest not in self.ignored:
                self.ignored.append(self.dest)

        try:
            x = self.direction.pop(0)
            return x
        except:
            return Action.NOOP
        

    def get_agent(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if 'A' in self.grid[i][j]:
                    return (i,j)

    def get_diamonds(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if (('1' in self.grid[i][j]) or ('2' in self.grid[i][j]) or ('3' in self.grid[i][j]) or ('4' in self.grid[i][j])) and ((i,j) not in self.ignored):
                    self.diamonds.append({self.grid[i][j]: (i,j)})
    
    
    def get_near_diamonds(self, diamonds, x, y):
        near_diamonds = []
        for i in range(len(diamonds)):
            if list(diamonds[i].values())[0][0] <= x+2 and list(diamonds[i].values())[0][0] >= x-2 and list(diamonds[i].values())[0][1] <= y+2 and list(diamonds[i].values())[0][1] >= y-2:
                near_diamonds.append(diamonds[i])
        return near_diamonds


    def get_nearest_key(self, keys):
        '''implemented with diagonal distance as the heuristic function'''
        x = self.get_agent()[0]
        y = self.get_agent()[1]
        D = 1
        D2 = 2
        h = 2**32
        coordinate = list(keys[0].values())[0]
        for i in range(len(keys)):  
            dx = abs(x - list(keys[i].values())[0][0])
            dy = abs(y - list(keys[i].values())[0][1])
            tmp = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
            if tmp < h:
                h = tmp
                coordinate = list(keys[i].values())[0]
                
        return coordinate
    
    
    def get_nearest_for_cluster(self, diamonds, beginning, initialization):
        '''implemented with diagonal distance as the heuristic function'''
        x = beginning[0]
        y = beginning[1]
        D = 1
        D2 = 2
        h = 2**32
        coordinate = []
        for i in range(len(diamonds)):
            dx = abs(x - diamonds[i][0])
            dy = abs(y - diamonds[i][1])
            tmp = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
            if not initialization: 
                if tmp < h and tmp <= 2:
                    h = tmp
                    coordinate = diamonds[i]
            else:
                if tmp < h:
                    h = tmp
                    coordinate = diamonds[i]
        return coordinate
    
    
    def clustering(self):
        cords = None
        tmp1 = []
        for i in self.diamonds:
            tmp1.append(list(i.values())[0])
            
        while(len(self.diamonds) != len(self.clustering_ignored)):
            cluster = []
            tmp2 = []
            for element in tmp1:
                if element not in self.clustering_ignored and element not in self.ignored:
                    tmp2.append(element)
            cords = self.get_nearest_for_cluster(tmp2, self.get_agent(), True)
            cluster.append(cords)
            self.clustering_ignored.append(cords)
            tmp2.remove(cords)
            
            for i in range(3):
                cords = self.get_nearest_for_cluster(tmp2, cords, False)
                if not cords:
                    break
                cluster.append(cords)
                self.clustering_ignored.append(cords)
                tmp2.remove(cords)
           
            self.total_clusters.append(cluster)
    
    
    
    def cluster_max_score(self, cords_list):
        sequence = []
        for i in cords_list:                                # find the diamond type of each coordinate
            for j in range(len(self.diamonds)):
                if list(self.diamonds[j].values())[0] == i:
                        sequence.append([list(self.diamonds[j].keys())[0], list(self.diamonds[j].values())[0]])
                
        perm = list(permutations(sequence))
        my_max = 0
        selected_perm = []
        for j in perm:
            cord_seq = []
            s = 0
            for i in range(len(j) - 1):
                if str(j[i][0]) + str(j[i+1][0]) in list(self.DIAMOND_SCORES.keys()):
                    s = s + self.DIAMOND_SCORES[str(j[i][0]) + str(j[i+1][0])]
                    cord_seq.append(j[i][1])
            if s >= my_max:
                my_max = s
                selected_perm = j
                
        return [list(selected_perm), my_max]

    
    def find_center(self, cords):
        x = y = 0
        for i in cords:
                x = x + i[0]
                y = y + i[1]
        x = x / len(cords)
        y = y / len(cords)
        return [x, y]
    
    
    
    def distance_to_center(self):
        distances = []
        ratios = []
        for i in self.cluster_centers:
            distances.append(math.dist(self.get_agent(), i))
        for i in range(len(distances)):
            if distances[i] == 0:
                continue
            ratios.append(self.clusters_scores[i][1] / distances[i])
        return ratios
    
    
    def create_grid_nodes(self):
        self.grid_nodes = [None] * self.grid_height
        for i in range(self.grid_height):
            self.grid_nodes[i] = [None] * self.grid_width

        for i in range(self.grid_height):
            for j in range(self.grid_width):
                self.grid_nodes[i][j] = Node((i,j), 0, 0)
                
    
    
    def get_items(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if 'W' in self.grid[i][j]:
                    self.grid_nodes[i][j].is_wall = True
                elif '*' in self.grid[i][j]:
                    self.grid_nodes[i][j].is_wired = True
                elif 'G' in self.grid[i][j] and 'G' not in self.collected_keys:
                    self.grid_nodes[i][j].door = 'G'
                    self.grid_nodes[i][j].is_door = True
                elif 'R' in self.grid[i][j] and 'R' not in self.collected_keys:
                    self.grid_nodes[i][j].door = 'R'
                    self.grid_nodes[i][j].is_door = True
                elif 'Y' in self.grid[i][j] and 'Y' not in self.collected_keys:
                    self.grid_nodes[i][j].door = 'Y'
                    self.grid_nodes[i][j].is_door = True
                elif 'g' in self.grid[i][j]:
                    self.grid_nodes[i][j].key = 'g'
                    self.keys.append((i,j))
                elif 'r' in self.grid[i][j]:
                    self.grid_nodes[i][j].key = 'r'
                    self.keys.append((i,j))
                elif 'y' in self.grid[i][j]:
                    self.keys.append((i,j))
                    self.grid_nodes[i][j].key = 'y'

    
    def calculate_score(self):
        s = 0
        for i in range(len(self.collected_diamonds) - 1):
            if str(self.collected_diamonds[i]) + str(self.collected_diamonds[i+1]) in list(self.DIAMOND_SCORES.keys()):
                s = s + self.DIAMOND_SCORES[str(self.collected_diamonds[i]) + str(self.collected_diamonds[i+1])]
        for i in range(len(self.collected_items)):
            if str(self.collected_items[i]) in list(self.COLLECTABLES_SCORE.keys()):
                    s = s + self.COLLECTABLES_SCORE[str(self.collected_items[i])]
        return s
                    
  
    def A_star(self, agent, diamond):
        currentNode = self.grid_nodes[agent[0]][agent[1]]
        self.openList.append(currentNode)
        found = False 

        while len(self.openList) != 0 and not found:
            min_node = self.openList[0]
            for node in self.openList:
                if node.f <= min_node.f:
                    min_node = node


            currentNode = min_node
            self.openList.remove(currentNode)
            self.closedList.append(currentNode)

            if currentNode.cords == diamond:
                found = True
                self.path = []
                temp = currentNode
                self.path.append(temp)
                self.check_key(temp)
                while(temp.previous):
                    self.check_key(temp.previous)
                    self.path.append(temp.previous)
                    temp = temp.previous
                for node in self.path:
                    print(node.cords)

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


            for n in neighbors:
                tempG = 0

                if n.is_wired:
                    tempG = currentNode.g + 20
                elif abs(currentNode.cords[0] - n.cords[0]) == 0 and abs(currentNode.cords[1] - n.cords[1]) == 1:
                        tempG = currentNode.g + 1                       
                elif abs(currentNode.cords[0] - n.cords[0]) == 1 and abs(currentNode.cords[1] - n.cords[1]) == 0:
                        tempG = currentNode.g + 1                       
                else:
                        tempG = currentNode.g + 2



                if n not in self.closedList and not n.is_wall and not n.is_door:
                    if n in self.openList:
                        if tempG < n.g:
                            n.g = tempG
                    else:
                        n.g = tempG
                        self.openList.append(n)

                    n.h = self.heuristic(n.cords, diamond)
                    n.f = n.g + n.h
                    n.previous = currentNode

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

    def check_key(self, node):
        if node.key and node.key.upper() not in self.collected_keys:
            self.collected_keys.append(node.key.upper())
            self.ignored = []
            self.cluster_centers = []
            self.clustering_ignored = []
            self.clusters_scores = []
            self.clusters_distance = []
            self.total_clusters = []
            self.clustered = False


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
    