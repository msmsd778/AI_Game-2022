import random
from base import BaseAgent, Action
from MainClass import Node
from itertools import permutations


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
    path = []
    dest = ()
    grid_nodes = list()
    direction = []
    collected_keys = []
    total_clusters = []
    clustering_ignored = []
    clustered = False

    def do_turn(self) -> Action:
        # self.count += 1
        # if self.count == 1:
        #     self.create_grid_nodes()
        #     self.get_items()
        
        if len(self.direction) == 0:
            self.path = []
            self.grid_nodes = []
            self.diamonds = []
            # self.ignored = []
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
                    print(self.cluster_max_score(i)) # to be saved somewhere
            
            
            if len(self.diamonds) == 0:
                return Action.NOOP

            nd = self.get_near_diamonds(self.diamonds, agent[0], agent[1])
            # print(self.ignored)
            if len(nd) == 0:
                self.dest = self.get_nearest_diamond(self.diamonds)
                for i in self.diamonds:
                    if list(i.values())[0] == self.dest:
                        diamond_type = list(i.keys())[0]
            else:
                if len(nd) > 1:
                    tmp_dict = dict()
                    for i in range(len(nd)):
                        tmp_dict[list(nd[i].values())[0]] = self.heuristic(self.get_agent(), list(nd[i].values())[0])
                        
                    tmp_dict = dict(sorted(tmp_dict.items(), key=lambda item: item[1]))
                    self.dest = list(tmp_dict)[0]
                    for i in range(len(nd)):
                        if list(nd[i].values())[0] == self.dest:
                            diamond_type = list(nd[i].keys())[0]
                else:
                    self.dest = list(nd[0].values())[0] # calculate sequence later!
                    diamond_type = list(nd[0].keys())[0]
                self.collected_items = self.collected_items + diamond_type   #not here: diamond might not be accessible
            found = self.A_star(agent, self.dest)
            if not found and self.dest not in self.ignored:
                # print(self.dest)
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


    def get_nearest_diamond(self, diamonds):
        '''implemented with diagonal distance as the heuristic function'''
        x = self.get_agent()[0]
        y = self.get_agent()[1]
        D = 1
        D2 = 2
        h = 2**32
        diamond_type = ''
        coordinate = list(diamonds[0].values())[0]
        for i in range(len(diamonds)):  
            dx = abs(x - list(diamonds[i].values())[0][0])
            dy = abs(y - list(diamonds[i].values())[0][1])
            tmp = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
            if tmp < h:
                h = tmp
                coordinate = list(diamonds[i].values())[0]
                diamond_type = list(diamonds[i].keys())[0]
                
        self.collected_items = self.collected_items + diamond_type
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
                if tmp < h and tmp <= 3:
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
        for i in cords_list:
            for j in range(len(self.diamonds)):
                if list(self.diamonds[j].values())[0] == i:
                        sequence.append(list(self.diamonds[j].keys())[0])
                
        perm = list(permutations(sequence))
        my_max = 0
        selected_perm = []
        for j in perm:
            s = 0
            for i in range(len(j) - 1):
                if str(j[i]) + str(j[i+1]) in list(self.DIAMOND_SCORES.keys()):
                    s = s + self.DIAMOND_SCORES[str(j[i]) + str(j[i+1])]
            if s >= my_max:
                my_max = s
                selected_perm = j
                
        return selected_perm, my_max

    
    
            
    
    def create_grid_nodes(self):
        self.grid_nodes = [None] * self.grid_height
        for i in range(self.grid_height):
            self.grid_nodes[i] = [None] * self.grid_width

        for i in range(self.grid_height):
            for j in range(self.grid_width):
                self.grid_nodes[i][j] = Node((i,j), 0, 0)
                
    
    # def get_keys(self):
    #     for i in range(self.grid_height):
    #         for j in range(self.grid_width):
    #             if 'g' in self.grid[i][j]:
    #                 self.grid_nodes[i][j].key = 'g'
    #             elif 'r' in self.grid[i][j]:
    #                 self.grid_nodes[i][j].key = 'r'
    #             elif 'y' in self.grid[i][j]:
    #                 self.grid_nodes[i][j].key = 'y'
    
    def get_items(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if 'W' in self.grid[i][j]:
                    self.grid_nodes[i][j].is_wall = True
                elif '*' in self.grid[i][j]:
                    self.grid_nodes[i][j].wired = True
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
                elif 'r' in self.grid[i][j]:
                    self.grid_nodes[i][j].key = 'r'
                elif 'y' in self.grid[i][j]:
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
                while(temp.previous):
                    self.check_key(temp.previous)
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
            # for i in range(self.grid_height):
            #     for j in range(self.grid_width):
            #         if self.grid_nodes[i][j].door == node.key.upper():
            #             self.grid_nodes[i][j].door = ''
            #             self.grid_nodes[i][j].is_door = False


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
    
# import math
# import random
# import matplotlib.pyplot as plt

# #First function to optimize
# # def heuristic(x):
# #     value = -x**2
# #     return value

# #Second function to optimize
# def function2(x):
#     value = -(x-2)**2
#     return value

# #Function to find index of list
# def index_of(a,list):
#     for i in range(0,len(list)):
#         if list[i] == a:
#             return i
#     return -1

# #Function to sort by values
# def sort_by_values(list1, values):
#     sorted_list = []
#     while(len(sorted_list)!=len(list1)):
#         if index_of(min(values),values) in list1:
#             sorted_list.append(index_of(min(values),values))
#         values[index_of(min(values),values)] = math.inf
#     return sorted_list

# #Function to carry out NSGA-II's fast non dominated sort
# def fast_non_dominated_sort(values1, values2):
#     S=[[] for i in range(0,len(values1))]
#     front = [[]]
#     n=[0 for i in range(0,len(values1))]
#     rank = [0 for i in range(0, len(values1))]

#     for p in range(0,len(values1)):
#         S[p]=[]
#         n[p]=0
#         for q in range(0, len(values1)):
#             if (values1[p] > values1[q] and values2[p] > values2[q]) or (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
#                 if q not in S[p]:
#                     S[p].append(q)
#             elif (values1[q] > values1[p] and values2[q] > values2[p]) or (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
#                 n[p] = n[p] + 1
#         if n[p]==0:
#             rank[p] = 0
#             if p not in front[0]:
#                 front[0].append(p)

#     i = 0
#     while(front[i] != []):
#         Q=[]
#         for p in front[i]:
#             for q in S[p]:
#                 n[q] =n[q] - 1
#                 if( n[q]==0):
#                     rank[q]=i+1
#                     if q not in Q:
#                         Q.append(q)
#         i = i+1
#         front.append(Q)

#     del front[len(front)-1]
#     return front

# #Function to calculate crowding distance
# def crowding_distance(values1, values2, front):
#     distance = [0 for i in range(0,len(front))]
#     sorted1 = sort_by_values(front, values1[:])
#     sorted2 = sort_by_values(front, values2[:])
#     distance[0] = 4444444444444444
#     distance[len(front) - 1] = 4444444444444444
#     for k in range(1,len(front)-1):
#         distance[k] = distance[k]+ (values1[sorted1[k+1]] - values2[sorted1[k-1]])/(max(values1)-min(values1))
#     for k in range(1,len(front)-1):
#         distance[k] = distance[k]+ (values1[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
#     return distance

# #Function to carry out the crossover
# def crossover(a,b):
#     r=random.random()
#     if r>0.5:
#         return mutation((a+b)/2)
#     else:
#         return mutation((a-b)/2)

# #Function to carry out the mutation operator
# def mutation(solution):
#     mutation_prob = random.random()
#     if mutation_prob <1:
#         solution = min_x+(max_x-min_x)*random.random()
#     return solution

# #Main program starts here
# pop_size = 20
# max_gen = 921

# #Initialization
# min_x=-55
# max_x=55
# solution=[min_x+(max_x-min_x)*random.random() for i in range(0,pop_size)]
# gen_no=0
# while(gen_no<max_gen):
#     heuristic_values = [heuristic(solution[i])for i in range(0,pop_size)]
#     function2_values = [function2(solution[i])for i in range(0,pop_size)]
#     non_dominated_sorted_solution = fast_non_dominated_sort(heuristic_values[:],function2_values[:])
#     print("The best front for Generation number ",gen_no, " is")
#     for valuez in non_dominated_sorted_solution[0]:
#         print(round(solution[valuez],3),end=" ")
#     print("\n")
#     crowding_distance_values=[]
#     for i in range(0,len(non_dominated_sorted_solution)):
#         crowding_distance_values.append(crowding_distance(heuristic_values[:],function2_values[:],non_dominated_sorted_solution[i][:]))
#     solution2 = solution[:]
#     #Generating offsprings
#     while(len(solution2)!=2*pop_size):
#         a1 = random.randint(0,pop_size-1)
#         b1 = random.randint(0,pop_size-1)
#         solution2.append(crossover(solution[a1],solution[b1]))
#     heuristic_values2 = [heuristic(solution2[i])for i in range(0,2*pop_size)]
#     function2_values2 = [function2(solution2[i])for i in range(0,2*pop_size)]
#     non_dominated_sorted_solution2 = fast_non_dominated_sort(heuristic_values2[:],function2_values2[:])
#     crowding_distance_values2=[]
#     for i in range(0,len(non_dominated_sorted_solution2)):
#         crowding_distance_values2.append(crowding_distance(heuristic_values2[:],function2_values2[:],non_dominated_sorted_solution2[i][:]))
#     new_solution= []
#     for i in range(0,len(non_dominated_sorted_solution2)):
#         non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i] ) for j in range(0,len(non_dominated_sorted_solution2[i]))]
#         front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
#         front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
#         front.reverse()
#         for value in front:
#             new_solution.append(value)
#             if(len(new_solution)==pop_size):
#                 break
#         if (len(new_solution) == pop_size):
#             break
#     solution = [solution2[i] for i in new_solution]
#     gen_no = gen_no + 1

# #Lets plot the final front now
# heuristic = [i * -1 for i in heuristic_values]
# function2 = [j * -1 for j in function2_values]
# plt.xlabel('Function 1', fontsize=15)
# plt.ylabel('Function 2', fontsize=15)
# plt.scatter(heuristic, function2)
# plt.show()