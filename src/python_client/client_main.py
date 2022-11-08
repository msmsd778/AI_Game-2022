import random
from base import BaseAgent, Action
from MainClass import Node


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
    
    openList = []
    closedList = []
    diamonds = []
    collected_diamonds = '0'
    collected_items = ''
    ignored = []
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
            self.get_keys()
            self.get_diamonds()
            agent = self.get_agent()
            self.closedList = []
            self.openList = []
            diamond_type = ''
            
            nd = self.get_near_diamonds(self.diamonds, agent[0], agent[1])
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
                self.collected_items = self.collected_items + diamond_type
            # print(nd)    
            # print(self.collected_items)
            found = self.A_star(agent, self.dest)
            # print(found)
            # if found:

            #     # self.moved = True
            # print(self.path)
            # print(self.dest)
        
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
                if (('1' in self.grid[i][j]) or ('2' in self.grid[i][j]) or ('3' in self.grid[i][j]) or ('4' in self.grid[i][j])) and (i,j) not in self.ignored:
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
        for i in range(len(diamonds)):  
            dx = abs(x - list(diamonds[i].values())[0][0])
            dy = abs(y - list(diamonds[i].values())[0][1])
            tmp = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
            if tmp < h:
                h = tmp
                coordinate = (list(diamonds[i].values())[0][0],list(diamonds[i].values())[0][1])
                diamond_type = list(diamonds[i].keys())[0]
                
        self.collected_items = self.collected_items + diamond_type
        return coordinate
    
    
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
                elif 'G' in self.grid[i][j]:
                    self.grid_nodes[i][j].door = 'G'
                elif 'R' in self.grid[i][j]:
                    self.grid_nodes[i][j].door = 'R'
                elif 'Y' in self.grid[i][j]:
                    self.grid_nodes[i][j].door = 'Y'
                elif '*' in self.grid[i][j]:
                    self.grid_nodes[i][j].wired = True
                    # self.closedList.append(Node((i,j),2,3))

    def get_keys(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if 'g' in self.grid[i][j]:
                    self.grid_nodes[i][j].key = 'g'
                elif 'r' in self.grid[i][j]:
                    self.grid_nodes[i][j].key = 'r'
                elif 'y' in self.grid[i][j]:
                    self.grid_nodes[i][j].key = 'y'
                    
    
    def calculate_score(self):
        for i in range(len(self.collected_diamonds) - 1):
            if self.collected_diamonds[i] + self.collected_diamonds[i+1] in list(self.DIAMONDS_SCORES.keys()):
                s = s + self.DIAMONDS_SCORES[self.collected_diamonds[i] + self.collected_diamonds[i+1]]
        for i in range(len(self.collected_items)):
            if self.collected_items[i] in list(self.COLLECTABLES_SCORE.keys()):
                    s = s + self.COLLECTABLES_SCORE[self.collected_items[i]]
                    
  
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
                
            
            # for n in self.openList:
            #     print(n.cords , n.f , n.g, n.h)
            # print('dest: ', self.dest)
            # # print('walls', self.walls)
            # print('__________________________')
        if not found:
            for i in range(self.grid_height):
                for j in range(self.grid_width):
                    if i == diamond[0] and j == diamond[1]:
                        self.ignored.append(diamond)
        return found

    
    def heuristic(self, start, goal):
        D = 1
        D2 = 2
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

            
    def get_direction(self, current, next):

        # print('current', current.cords)
        # print('next', next.cords)

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