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


    def do_turn(self) -> Action:
        agent = self.get_agent()
        print(agent)
        print(self.get_near_diamonds(self.get_diamonds(),agent[0], agent[1]))   
        return Action.DOWN

    def get_agent(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if 'A' in self.grid[i][j]:
                    return (i,j)

    def get_diamonds(self):
        diamonds = []
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if ('1' in self.grid[i][j]) or ('2' in self.grid[i][j]) or ('3' in self.grid[i][j]) or ('4' in self.grid[i][j]):
                    diamonds.append({self.grid[i][j]: (i,j)})
        return diamonds

    def get_near_diamonds(self, diamonds, x, y):
        near_diamonds = []
        for i in range(len(diamonds)):
            if list(diamonds[i].values())[0][0] <= x+2 and list(diamonds[i].values())[0][0] >= x-2 and list(diamonds[i].values())[0][1] <= y+2 and list(diamonds[i].values())[0][1] >= y-2:
                near_diamonds.append(diamonds[i])
        return near_diamonds

    def is_reachable(self, agent, diamond):
        """check turn, score, walls"""
        pass

    def find_route(self, agent, diamond):
        """return score"""
        pass

    def get_nearest_diamond(self, agent, diamonds):
        pass

    


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
