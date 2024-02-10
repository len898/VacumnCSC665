import numpy as np
import random
from matplotlib import pyplot as plt
import time
from prettytable import PrettyTable

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
        return self.grid[y,x] == 1
    
    def get_bound(self):
        return [self.width-1, self.height-1]
    
    def clean_spot(self, x, y):
        self.grid[y,x] = 0
    
    def update_agent_path(self, x, y):
        self.visited[y,x] = 1
    
    def get_stats(self):
        return np.count_nonzero(self.grid)
    
    def visualize(self, prefix, final=False):
        if(self.step % 500 == 0 or self.step == 0 or final):
            
            plt.imshow(self.grid,cmap='Blues' ,interpolation="nearest", vmin=0, vmax=1)
            filepath = prefix + "grid" + str(self.step)
            plt.savefig(filepath, dpi=300)
            plt.clf()
            
            plt.imshow(self.visited, cmap="Reds", interpolation="nearest", vmin=0, vmax=1)
            filepath = prefix + "path" + str(self.step)
            plt.savefig(filepath,dpi=300)
            plt.clf()
            self.step += 1
        self.step += 1
        
    
class RandomAgent():
    def __init__(self, startx, starty):
        self.row = startx
        self.column = starty
        self.filepath = "random_agent/"
    
    def action(self, env):
        action = self.__get_action()
        bounds = env.get_bound()
        if(action == 0):
            #Go left or break if not possible
            if(self.column == 0):
                return -1
            self.column -= 1
        elif(action == 1):
            #Go right or break if not possible
            if(self.column == bounds[0]):
                return -1
            self.column += 1
        elif(action == 2):
            #Go up or break if not possible
            if(self.row == 0):
                return -1
            self.row += 1
        elif(action == 3):
            #Go down or break if not possible
            if(self.row == bounds[1]):
                return -1
            self.row -= 1
        elif(action == 4):
            #Vacumn the current regardless of dirtiness
            env.clean_spot(self.column, self.row)
    
    def __get_action(self):
        return random.randint(0,4)
    
    def visualize_agent_movement(self, env):
        env.update_agent_path(self.column, self.row)
        env.visualize(self.filepath)

class ReflexAgent:
    def __init__(self, startx, starty):
        self.column = startx
        self.row = starty
        self.filepath = "reflex_agent/"
        
    def action(self, env):
        action = self.__get_action(env)
        if(action == 0):
            self.column -= 1
        elif(action == 1):
            self.column += 1
        elif(action == 2):
            self.row -= 1
        elif(action == 3):
            self.row += 1
        elif(action == 4):
            env.clean_spot(self.column, self.row)
        
    def __get_action(self, env):
        #The reflex agent acts if it senses dirt in the current square its standing in
        #Otherwise it will make a random decision, with the limitation that it cannot
        #take an action that would take it out of bounds
        if(env.is_dirty(self.column, self.row)):
            return 4
        
        bounds = env.get_bound()
        while(True):
            act = random.randint(0,3)
            if(act == 0 and self.column != 0):
                return 0
            if(act == 1 and self.column != bounds[0]):
                return 1
            if(act == 2 and self.row != 0):
                return 2
            if(act == 3 and self.row != bounds[1]):
                return 3

    def visualize_agent_movement(self, env):
        env.update_agent_path(self.column, self.row)
        env.visualize(self.filepath)
        
class ModelBasedReflex:
    def __init__(self, startx, starty):
        self.column = startx
        self.row = starty
        self.model = []
        self.model.append([startx, starty])
        self.filepath = "model_reflex_agent/"
    
    def action(self, env):
        action = self.__get_action(env)
        #print(f"Action is {action}")
        if(action == 4):
            env.clean_spot(self.column, self.row)
        elif(action == 0):
            self.column -= 1
            self.model.append([self.column, self.row])
        elif(action == 1):
            self.column += 1
            self.model.append([self.column, self.row])
        elif(action == 3):
            self.row += 1
            self.model.append([self.column, self.row])
        #time.sleep(0.5)
        else:
            return -1
    
    def __get_action(self, env):
        #If the current spot is dirty, then clean
        if(env.is_dirty(self.column, self.row)):
            return 4
        #If we are at the dock, start by going to the right
        if(self.column == 0 and self.row == 0):
            return 1
        bounds = env.get_bound()
        
        if(len(self.model) == (bounds[0] + 1)*(bounds[1] + 1)):
            return -1
        #If we are at the bottom left, finish
        #if(self.column == bounds[0] and self.row == bounds[0]):
        #    return -1
        #If we are not at the border and the last spot was to the left keep moving to the right
        #print(self.model[len(self.model)-1][0])
        #print(self.row)
        if(self.column != bounds[0] and self.model[len(self.model)-2][0] < self.column):
            return 1
        #If we are at the border and were moving to the right, move down
        if(self.column == bounds[0] and self.model[len(self.model)-2][0] < self.column and self.row -1 != bounds[0]):
            return 3
        #If we are at the border and just moved down, move to the left
        if(self.column == bounds[0] and self.model[len(self.model)-2][1] < self.row):
            return 0
        #If we are moving to the left and not at the border keep moving left
        if(self.column != 0 and self.model[len(self.model)-2][0] > self.column):
            return 0
        #If we are at the left hand border and moving left, move down
        if(self.column == 0 and self.model[len(self.model)-2][0] > self.column and self.row -1 != bounds[0]):
            return 3
        #If we are at the left hand border and just moved down, move right
        if(self.column == 0 and self.model[len(self.model)-2][1] < self.row):
            return 1
        
        
    def visualize_agent_movement(self, env, final=False):
        env.update_agent_path(self.column, self.row)
        env.visualize(self.filepath, final)

def random_agent_simulation(leftover5:list, leftover10:list, leftover100:list):
    #We will run the simulations for 3 different sizes but only capture
    #images for the 100X100 run the first time
    for i in range(0, 100):
        ra = RandomAgent(0,0)
        env = Environment(5, 5)
        env.make_dirty(0.1)
        action = 1
        while(action):
            action = ra.action(env)
        leftover5.append(env.get_stats())
        
    for i in range(0, 100):
        ra = RandomAgent(0,0)
        env = Environment(10, 10)
        env.make_dirty(0.1)
        action = 1
        while(action):
            action = ra.action(env)
        leftover10.append(env.get_stats())
        
    for i in range(0, 100):
        ra = RandomAgent(0,0)
        env = Environment(100, 100)
        env.make_dirty(0.1)
        action = 1
        if(i == 1):
            ra.visualize_agent_movement(env)
        while(action):
            action = ra.action(env)
            if(i == 1):
                ra.visualize_agent_movement(env)
        leftover100.append(env.get_stats())

def reflex_agent_simulation(leftover5:list, leftover10:list, leftover100:list):
    #We will run the simulations for 3 different sizes but only capture
    #images for the 100X100 run the first time
    for i in range(0, 100):
        ra = ReflexAgent(0,0)
        env = Environment(5, 5)
        env.make_dirty(0.1)
        for ii in range(0, 20000):
            ra.action(env)
        leftover5.append(env.get_stats())
        
    for i in range(0, 100):
        ra = ReflexAgent(0,0)
        env = Environment(10, 10)
        env.make_dirty(0.1)
        for ii in range(0,20000):
            ra.action(env)
        leftover10.append(env.get_stats())
        
    for i in range(0, 100):
        ra = ReflexAgent(0,0)
        env = Environment(100, 100)
        env.make_dirty(0.1)
        if(i == 1):
            ra.visualize_agent_movement(env)
        for ii in range(0, 20000):
            ra.action(env)
            if(i == 1):
                ra.visualize_agent_movement(env)
        leftover100.append(env.get_stats())
        
def model_reflex_agent_simulation(leftover5:list, leftover10:list, leftover100:list):
    #We will run the simulations for 3 different sizes but only capture
    #images for the 100X100 run the first time
    for i in range(0, 100):
        ra = ModelBasedReflex(0,0)
        env = Environment(5, 5)
        env.make_dirty(0.1)
        for ii in range(0, 20000):
            if(ra.action(env)) == -1:
                break
        leftover5.append(env.get_stats())
        
    for i in range(0, 100):
        ra = ModelBasedReflex(0,0)
        env = Environment(10, 10)
        env.make_dirty(0.1)
        for ii in range(0,20000):
            if(ra.action(env)) == -1:
                break
        leftover10.append(env.get_stats())
        
    for i in range(0, 100):
        ra = ModelBasedReflex(0,0)
        env = Environment(100, 100)
        env.make_dirty(0.1)
        action = 1
        if(i == 1):
            ra.visualize_agent_movement(env)
        for ii in range(0, 20000):
            action = ra.action(env)
            if(i == 1 and action != -1):
                ra.visualize_agent_movement(env)
            elif(i == 1 and action == -1):
                ra.visualize_agent_movement(env, True)
                break
        leftover100.append(env.get_stats())
            

def main():
    #The lists that will be used to determine cleanlienss statistics
    random_agent_dirty_left_5_5 = []
    random_agent_dirty_left_10_10 = []
    random_agent_dirty_left_100_100 = []
    
    reflex_agent_dirty_left_5_5 = []
    reflex_agent_dirty_left_10_10 = []
    reflex_agent_dirty_left_100_100 = []
    
    model_reflex_agent_dirty_left_5_5 = []
    model_reflex_agent_dirty_left_10_10 = []
    model_reflex_agent_dirty_left_100_100 = []
    
    random_agent_simulation(random_agent_dirty_left_5_5, random_agent_dirty_left_10_10, random_agent_dirty_left_100_100)
    reflex_agent_simulation(reflex_agent_dirty_left_5_5, reflex_agent_dirty_left_10_10, reflex_agent_dirty_left_100_100)
    model_reflex_agent_simulation(model_reflex_agent_dirty_left_5_5, model_reflex_agent_dirty_left_10_10, model_reflex_agent_dirty_left_100_100)
    
    pt = PrettyTable()
    pt.field_names = ["Agent","Grid Size", "Operations Limit #", "# Dirty Remaining"]
    pt.add_row(["Random Agent", "5X5", "20000", np.average(random_agent_dirty_left_5_5)])
    pt.add_row(["Reflex Agent", "5X5", "20000", np.average(reflex_agent_dirty_left_5_5)])
    pt.add_row(["Model Reflex Agent", "5X5", "20000", np.average(model_reflex_agent_dirty_left_5_5)])
    
    pt.add_row(["Random Agent", "10X10", "20000", np.average(random_agent_dirty_left_10_10)])
    pt.add_row(["Reflex Agent", "10X10", "20000", np.average(reflex_agent_dirty_left_10_10)])
    pt.add_row(["Model Reflex Agent", "10X10", "20000", np.average(model_reflex_agent_dirty_left_10_10)])
    
    pt.add_row(["Random Agent", "100X100", "20000", np.average(random_agent_dirty_left_100_100)])
    pt.add_row(["Reflex Agent", "100X100", "20000", np.average(reflex_agent_dirty_left_100_100)])
    pt.add_row(["Model Reflex Agent", "100X100", "20000", np.average(model_reflex_agent_dirty_left_100_100)])
    
    print(pt)

    
main()