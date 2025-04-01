import numpy as np
import random
from collections import deque
import tensorflow as tf

from config_update import config_update
from new_cover_main import get_rewards
import shutil
import time
import os   
from MainSchGen import *

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
    
    def _build_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model


    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.target_model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
 
class SimpleEnv:
    def __init__(self):

        self.R_param_settings = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}
        self.L_param_settings = {6: 1, 7: 2, 8: 3, 9: 4, 10: 5}
        self.C_param_settings = {11: 1, 12: 2, 13: 3, 14: 4, 15: 5}
        self.rectifier_diodes_param_settings = {16: 1, 17: 2, 18: 3, 19: 4, 20: 5}  
        self.schottky_diodes_param_settings = {21: 1, 22: 2, 23: 3, 24: 4, 25: 5}
        self.zener_diodes_param_settings = {26: 1, 27: 2, 28: 3, 29: 4, 30: 5}
        self.leds_param_settings = {31: 1, 32: 2, 33: 3, 34: 4, 35: 5}
        # self.Q_BJT_param_settings = {36: 1, 37: 2, 38: 3, 39: 4, 40: 5}
        # self.Q_FET_param_settings = {41: 1, 42: 2, 43: 3, 44: 4, 45: 5}
        # self.Q_JFET_param_settings = {46: 1, 47: 2, 48: 3, 49: 4, 50: 5}
        # self.Q_MOSFET_param_settings = {51: 1, 52: 2, 53: 3, 54: 4, 55: 5}
        # self.Q_IGBT_param_settings = {56: 1, 57: 2, 58: 3, 59: 4, 60: 5}
        # self.Branch_param_settings = {61: 1, 62: 1, 63: 1, 64: 1, 65: 1}
        self.state = None

    def reset(self):
        self.state = [random.choice(list(self.R_param_settings.keys())),
                      random.choice(list(self.L_param_settings.keys())),
                      random.choice(list(self.C_param_settings.keys())),
                      random.choice(list(self.rectifier_diodes_param_settings.keys())),
                      random.choice(list(self.schottky_diodes_param_settings.keys())),
                      random.choice(list(self.zener_diodes_param_settings.keys())),
                      random.choice(list(self.leds_param_settings.keys())),
                    #   random.choice(list(self.Q_BJT_param_settings.keys())),
                    #   random.choice(list(self.Q_FET_param_settings.keys())),
                    #   random.choice(list(self.Q_JFET_param_settings.keys())),
                    #   random.choice(list(self.Q_MOSFET_param_settings.keys())),
                    #   random.choice(list(self.Q_IGBT_param_settings.keys())),
                    #   random.choice(list(self.Branch_param_settings.keys())),
                        ]
        
        return np.array(self.state).reshape(1, 7)

    def step(self, action):

        super_new_state = [
            f"expr.binary={self.R_param_settings[self.state[0]]}",
            f"expr.binary={self.L_param_settings[self.state[1]]}",
            f"expr.binary={self.C_param_settings[self.state[2]]}",
            f"expr.binary={self.rectifier_diodes_param_settings[self.state[3]]}",
            f"expr.binary={self.schottky_diodes_param_settings[self.state[4]]}",
            f"expr.binary={self.zener_diodes_param_settings[self.state[5]]}",
            f"expr.binary={self.leds_param_settings[self.state[6]]}",
            # f"expr.binary={self.Q_BJT_param_settings[self.state[7]]}",
            # f"expr.binary={self.Q_FET_param_settings[self.state[8]]}",
            # f"expr.binary={self.Q_JFET_param_settings[self.state[9]]}",
            # f"expr.binary={self.Q_MOSFET_param_settings[self.state[10]]}",
            # f"expr.binary={self.Q_IGBT_param_settings[self.state[11]]}",
            # f"expr.binary={self.Branch_param_settings[self.state[12]]}",

        ]

        orginal_config_file_path = './ConfigFile.txt'  
        shutil.copy(orginal_config_file_path, case_folder)
        config_file_path = f"{case_folder}/ConfigFile.txt"
        config_update(config_file_path, super_new_state)
        #调用PCB_case_generate开始生成测试用例
        PCB_case_generate(case_folder,config_file_path)

        # #将C:\Users\dell\Desktop\new_result下的NetlistsResults文件夹以及PCBSmith10GenV43.txt文件复制到case_folder文件夹下
        # # 目标文件夹路径
        # dest_folder = f"{case_folder}/NetlistsResults"

        # # 如果目标文件夹已存在，先删除它
        # if os.path.exists(dest_folder):
        #     shutil.rmtree(dest_folder)  # 删除文件夹及其内容
        # print("#################11111111111#############")
        # # 然后再复制
        # shutil.copytree('C:\\Users\\dell\\Desktop\\new_result\\NetlistsResults', dest_folder)
        # print("################2222222222222##############")
        # #将C:\Users\dell\Desktop\new_result下的PCBSmith10GenV43.txt文件复制到case_folder文件夹下
        # shutil.copy('C:\\Users\\dell\\Desktop\\new_result\\PCBSmith10GenV43.txt', f"{case_folder}/PCBSmith10GenV43.txt")
        # # time.sleep(10) 

        # #base_path为case_folder文件夹下的NetlistsResults文件夹
        # base_path = f"{case_folder}/NetlistsResults"
        # #bug_file为case_folder文件夹下的PCBSmith10GenV43.txt
        # bug_file_path = f"{case_folder}/PCBSmith10GenV43.txt"


        try:
            reward = get_rewards(base_path,bug_file_path)
            print("##############################")
            print("Rewards:", reward)
        except Exception as e:
            print(f"An error occurred while getting fitness_candidate: {e}")
            reward = 0

        print("########################################")
        print(reward)
        print(self.state)
        print(super_new_state)
        print(action)
        print("########################################")
        done = False  # Assuming task is not episodic
        return np.array(self.state).reshape(1, 7), reward, done

def create_case_folder(episode):
    case_base_path = './baseline_case_and_bug_generation'
    case_folder = f"{case_base_path}/RECCORD/case_generation/case_generation_{episode}"

    if not os.path.exists(case_folder):
        os.makedirs(case_folder)
        
    return case_folder

if __name__ == '__main__':
    env = SimpleEnv()
    state_size = 7  # Binary and Signed parameters
    action_size = 5**7  # 3 options for expr.binary * 3 options for expr.signed
    agent = DQNAgent(state_size, action_size)
    batch_size = 7

    EPISODES = 1000  # Adjust this value as needed
    for e in range(EPISODES):

        state = env.reset()

        for time in range(10):  # Adjust the maximum number of steps as needed
            new_counter = time + e * 10
            case_folder = create_case_folder(new_counter)
            # bug_folder = create_bug_folder(new_counter)
            print("new_counter: ",new_counter)

            action = agent.act(state)
            next_state, reward, done = env.step(action)
            reward = float(reward)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

    print("Training finished.")
