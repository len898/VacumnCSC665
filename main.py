import numpy as np
import random
from matplotlib import pyplot as plt
import time

class Environment():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((self.width, self.height))
        self.visited = np.zeros((width, height))
        self.step = 0
    
    def make_dirty(self, dirt_percent):
        num_dirty = (self.width * self.height) * dirt_percent
        while(num_dirty > 0):
            x = random.randint(0,self.width -1)
            y = random.randint(0,self.height -1)
            if(self.grid[x,y] == 0):
                self.grid[x,y] = 1
                num_dirty -= 1
    
    def is_dirty(self, x, y):
        return self.grid[x,y] == 1
    
    def get_bound(self):
        return [self.width-1, self.height-1]
    
    def clean_spot(self, x, y):
        self.grid[x,y] = 0
    
    def update_agent_path(self, x, y):
        self.visited[x,y] = 1
    
    def get_stats(self):
        return np.count_nonzero(self.grid)
    
    def visualize(self):
        if(self.step % 100 == 0 or self.step == 0):
            plt.imshow(self.grid,cmap='Blues' ,interpolation="nearest")
            filepath = "random_agent/grid" + str(self.step)
            plt.savefig(filepath, dpi=300)
            plt.clf()
            
            plt.imshow(self.visited, cmap="Reds", interpolation="nearest")
            filepath = "random_agent/path" + str(self.step)
            plt.savefig(filepath,dpi=300)
            plt.clf
            self.step += 1
        self.step += 1
        
    
class RandomAgent():
    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
    
    def action(self, env):
        action = self.__get_action()
        bounds = env.get_bound()
        if(action == 0):
            #Go left or break if not possible
            if(self.x == 0):
                return -1
            self.x -= 1
        elif(action == 1):
            #Go right or break if not possible
            if(self.x == bounds[0]):
                return -1
            self.x += 1
        elif(action == 2):
            #Go up or break if not possible
            if(self.y == 0):
                return -1
            self.y += 1
        elif(action == 3):
            #Go down or break if not possible
            if(self.y == bounds[1]):
                return -1
            self.y += 1
        elif(action == 4):
            #Vacumn the current regardless of dirtiness
            env.clean_spot(self.x, self.y)
    
    def __get_action(self):
        return random.randint(0,4)
    
    def visualize_agent_movement(self, env):
        env.update_agent_path(self.x, self.y)
        env.visualize()

class ReflexAgent:
    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
        
    def action(self, env):
        action = self.__get_action(env)
        if(action == 0):
            self.x -= 1
        elif(action == 1):
            self.x += 1
        elif(action == 2):
            self.y -= 1
        elif(action == 3):
            self.y += 1
        elif(action == 4):
            env.clean_spot(self.x, self.y)
        
    def __get_action(self, env):
        if(env.is_dirty(self.x, self.y)):
            print("dirty")
            return 4
        
        bounds = env.get_bound()
        while(True):
            act = random.randint(0,3)
            if(act == 0 and self.x != 0):
                return 0
            if(act == 1 and self.x != bounds[0]):
                return 1
            if(act == 2 and self.y != 0):
                return 2
            if(act == 3 and self.y != bounds[1]):
                return 3

    def visualize_agent_movement(self, env):
        env.update_agent_path(self.x, self.y)
        env.visualize()
        
class ModelBasedReflex:
    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
        self.model = []
        self.model.append([startx, starty])
    
    def action(self, env):
        if(env.is_dirty(self.x, self.y)):
            return 4
        
        return self.__get_action(env)
    
    def __get_action(self, env):
        #If we are at the dock, start by going to the right
        if(self.x == 0 and self.y == 0):
            return 1
        bounds = env.get_bound()
        # Need to calculate which direction we are going
        # 6 Cases
        # Moving left
        if(self.x != 0 and self.x != bounds[0] and model[len(model)-1][0])
        # Moving Right
        # Right Border
        # Left Border
          

def main():
    # ra = RandomAgent(0, 0)
    # env = Environment(100,100)
    # env.make_dirty(0.1)
    # while(True):    
    #     act = ra.action(env)
    #     ra.visualize_agent_movement(env)
    #     if(act == -1):
    #         break
    ra = ReflexAgent(0, 0)
    env = Environment(100, 100)
    env.make_dirty(0.1)
    for i in range(0, 10000):
        ra.action(env)
        ra.visualize_agent_movement(env)
    
main()