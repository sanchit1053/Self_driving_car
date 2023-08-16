from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

        # NOT NEEDED AS REMOVED Q LEARNING
        self.weights = np.random.rand(3,5,5,1)
        self.bias = np.random.rand()
        self.eps = 0.05
        self.xLimit = None
        self.yLimit = None
        self.num_steering = 3
        self.num_acceleration = 5
        self.gamma = 1
        self.learning_rate = 0.1
        self.previous_state = None
        self.previous_action = None
        self.cache = []

    
    # FUNCTION THAT EXTRACTS FEATURES OUT OF THE DATA
    def normalize(self, state):
        newState = np.zeros(shape =(1,5))

        # newState[0][0] = state[0] / 1000
        # newState[0][1] = state[1] / 1000
        # newState[0][2] = state[2] / 40  
        # newState[0][3] = state[3] % 360 - 360
        # newState[0][3] = newState[0][3] / 720
        newState[0][0] = np.sqrt((state[0] - 500)**2 + (state[1])**2) / 783
        angle = np.arctan2((state[1]) , (500 - state[0])) * -180 / 3.1415
        if(state[3] > 180):
            state[3] = state[3] - 360
        newState[0][1] = np.abs(state[3] - angle)
        if newState[0][1] > 180:
            newState[0][1] = 360 - newState[0][1]
        newState[0][1] = newState[0][1]/ 180

        if (state[1] > 150 or state[1] < -150) and state[0] > 250:
            newState[0][2] = state[0]
            newState[0][2] /= 1000
            newState[0][3] = -1 * state[3] / 180
            newState[0][4] = 1
        else:
            newState[0][2] = 0
            newState[0][2] /= 1000
            newState[0][3] = 0
            newState[0][4] = 0
        return newState

    # CALCULATES Q VALUE
    def getQvalue(self, state, action):
        weight = self.weights[action[0], action[1]]
        retval =  state @ weight
        return retval + self.bias

    def prob(self, x):
        return x / (np.sum(x) + 1e-20)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """

        x, y, vel, angle = state

        # print(x, y, vel, angle)
        if y < 10 and y > -10: 
            if (angle <= 2 and angle >= 0) or (angle >= 360 - 2 and angle <= 360):
                return [1,4]
            elif angle >= 0 and angle < 180:
                return [0,2]
            else:
                return [2,2]
        elif y < 0:
            if angle <= 90 + 5 and angle >= 90 - 5:
                return [1,4]
            elif angle >= 90 and angle < 270:
                return [0,2]
            else:
                return [2,2]
        elif y > 0:
            if angle <= 270 + 5 and angle >= 270 - 5:
                return [1,4]
            elif angle >= 90 and angle < 270:
                return [2,2]
            else:
                return [0,2]
        return [0,0]
        


        # CODE TO IMPLEMENT Q LEARNING
        # Replace with your implementation to determine actions to be taken
        
        
        # self.previous_state = state

        # Qvalue = np.zeros(shape=(3,5))
        # for steer in range(3):
        #     for acc in range(5):
        #         Qvalue[steer][acc] = self.getQvalue(state, [steer, acc])
            
        # # print(Qvalue)
        # s, a = np.unravel_index(np.argmax(Qvalue), Qvalue.shape)

        # randomValue = np.random.rand(1)
        # if randomValue > self.eps:
        #     action_steer = s
        #     action_acc = a
        # else:
        #     action_steer = np.random.randint(0,3)
        #     action_acc = np.random.randint(0,5)

        # self.previous_action = [action_steer, action_acc]


        # action = np.array([action_steer, action_acc]) 
        # # print("WIEGHTs", self.weights[s,a]) 
        # # print("action" , action)
        # return action


    # UPDATE THE WEIGHTS AND BIASES NOT NEEDED AS Q LEARNING ReMOVED
    def update(self, state, reward, terminate):
        self.cache.append([self.previous_state, self.previous_action, reward, state])
        Qvalue = np.zeros(shape=(3,5))
        for steer in range(3):
            for acc in range(5):
                Qvalue[steer][acc] = self.getQvalue(state, [steer, acc])
        
        # Qvalue = self.prob(Qvalue)
        s, a = np.unravel_index(np.argmax(Qvalue), Qvalue.shape)

        target = reward + self.gamma * np.max(Qvalue)
        # phi = np.append(self.previous_state, 0).T
        phi = self.previous_state
        previous_qvalue = self.getQvalue(self.previous_state, self.previous_action)
        change = self.learning_rate * (target - previous_qvalue ) * phi.T
        change = np.reshape(change, newshape=(-1,1))
        # print("weights", self.weights[s, a])
        # print(Qvalue)
        # print("NEW", np.max(Qvalue))
        # print("NEW action", [s, a])
        # print("NEW state", state)
        # print("PREV", self.getQvalue(self.previous_state, self.previous_action))
        # print("PREV action", self.previous_action)
        # print("PREV state", self.previous_state)
        # print("target" , target)
        # print("phi", phi)
        # print("previous", self.getQvalue(self.previous_state, self.previous_action))
        # print("weights", self.weights[self.previous_action[0], self.previous_action[1]])
        # print("change", change)
        # t = input()
        self.weights[self.previous_action[0], self.previous_action[1]] += change
        self.bias += self.learning_rate * (target - previous_qvalue ) 

        for _ in range(200):
            previous_state, previous_action, reward, newState  = self.cache[np.random.randint(len(self.cache))]
            Qvalue = np.zeros(shape=(3,5))
            for steer in range(3):
                for acc in range(5):
                    Qvalue[steer][acc] = self.getQvalue(newState, [steer, acc])
            
            # Qvalue = self.prob(Qvalue)

            target = reward + self.gamma * np.max(Qvalue)
            phi = previous_state
            previous_qvalue = self.getQvalue(previous_state, previous_action)
            change = self.learning_rate * (target - previous_qvalue ) * phi.T
            change = np.reshape(change, newshape=(-1,1))
            self.weights[previous_action[0], previous_action[1]] += change
            self.bias += self.learning_rate * (target - previous_qvalue ) 



    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
    
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator

            param_dict = json.load(open(config_filepath, "r"))
            self.xLimit, self.yLimit = param_dict["screen_size"]
            # state = self.normalize(state)

            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)

                # state = self.normalize(state)
                # self.update(state, reward, terminate)

                fpsClock.tick(FPS)
                # print(reward)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break


            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()
        self.pitCenters = None
        self.freeSpace = None

        self.checkLeft = False
        self.checkDown = False
        self.checkUp = False
        self.checkRight = False

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """

        # Replace with your implementation to determine actions to be taken
        x, y, vel, angle = state

        # print(x, y, vel, angle)
        
        angleRange = 1.5
        pitDistance = 25


        if x <= -300 + 10 or x >= 300 - 10 or y < -300 + 10 or y > 300 - 10 or (y <= 10 and y >= -10):
            self.edgeReached = True


        if self.edgeReached:
            if x <= -300 + 10:
                # print("EDGE", x)
                if y < 300 - 10:
                    if angle <= 90 + angleRange and angle >= 90 - angleRange:
                        return [1,4]
                    elif angle >= 90 and angle < 270:
                        return [0,2]
                    else:
                        return [2,2]
                else:
                    if (angle <= angleRange and angle >= 0) or (angle >= 360 - angleRange and angle <= 360):
                        return [1,4]
                    elif angle >= 0 and angle < 180:
                        return [0,2]
                    else:
                        return [2,2]
            elif x < 300 - 10:
                if (angle <= angleRange and angle >= 0) or (angle >= 360 - angleRange and angle <= 360):
                    return [1,4]
                elif angle >= 0 and angle < 180:
                    return [0,2]
                else:
                    return [2,2]
            else:
                if y < 70 and y > -70:
                    if (angle <= angleRange and angle >= 0) or (angle >= 360 - angleRange and angle <= 360):
                        return [1,4]
                    elif angle >= 0 and angle < 180:
                        return [0,2]
                    else:
                        return [2,2]
                elif y < 0:
                    if angle <= 90 + angleRange and angle >= 90 - angleRange:
                        return [1,4]
                    elif angle >= 90 and angle < 270:
                        return [0,2]
                    else:
                        return [2,2]
                elif y > 0:
                    if angle <= 270 + angleRange and angle >= 270 - angleRange:
                        return [1,4]
                    elif angle >= 90 and angle < 270:
                        return [2,2]
                    else:
                        return [0, 2]
        else:
            if self.checkRight:
                # print("RIGHT")
                if (angle <= angleRange and angle >= 0) or (angle >= 360 - angleRange and angle <= 360):
                    return [1,4]
                elif angle >= 0 and angle < 180:
                    return [0,2]
                else:
                    return [2,2]
            elif self.checkDown:
                # print("DOWN")
                if angle <= 90 + angleRange and angle >= 90 - angleRange:
                    return [1,4]
                elif angle >= 90 and angle < 270:
                    return [0,2]
                else:
                    return [2,2]
            elif self.checkUp:
                # print("UP")
                if angle <= 270 + angleRange and angle >= 270 - angleRange:
                    return [1,4]
                elif angle >= 90 and angle < 270:
                    return [2,2]
                else:
                    return [0, 2]
            elif self.checkLeft:
                # print("LEFT")
                if angle <= 180 + angleRange and angle >= 180 - angleRange:
                    return [1,4]
                elif angle >= 0 and angle < 180:
                    return [2,2]
                else:
                    return [0,2]
            else:
                self.checkDown = True
                self.checkUp = True
                self.checkLeft = True
                self.checkRight = True

                for pit in self.pitCenters:
                    if y <= pit[1] + 50 + pitDistance and y >= pit[1] - 50 - pitDistance:
                        if x < pit[0]:
                            self.checkRight = False
                        else:
                            self.checkLeft = False
                    if x <= pit[0] + 50 + pitDistance and x >= pit[0] - 50 - pitDistance:
                        if y < pit[1]:
                            self.checkDown = False
                        else:
                            self.checkUp = False
                
        return [1,0]

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False

            self.pitCenters = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]


            
            
            self.checkDown = False
            self.checkUp = False
            self.checkLeft = False
            self.checkRight = False


            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                self.edgeReached = False
                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
