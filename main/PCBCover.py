import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from MainSchGen import *
import os
from config_update import config_update
import shutil
from new_cover_main import get_rewards
import time

class MultiAgentA2C:
    def __init__(self, num_agents, num_actions, state_dim, actor_lr=0.001, critic_lr=0.005, gamma=0.99):
        self.num_agents = num_agents
        self.num_actions = num_actions
        self.gamma = gamma

        # Actor and Critic networks for each agent
        self.actors = [self.build_actor(state_dim, num_actions) for _ in range(num_agents)]
        self.critics = [self.build_critic(state_dim) for _ in range(num_agents)]

        self.actor_optimizer = Adam(learning_rate=actor_lr)
        self.critic_optimizer = Adam(learning_rate=critic_lr)

    def build_actor(self, state_dim, action_dim):
        inputs = Input(shape=(state_dim,))
        x = Dense(1024, activation='relu')(inputs)
        x = Dense(1024, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        outputs = Dense(action_dim, activation='softmax')(x)
        model = Model(inputs, outputs)
        return model

    def build_critic(self, state_dim):
        inputs = Input(shape=(state_dim,))
        x = Dense(1024, activation='relu')(inputs)
        x = Dense(1024, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        outputs = Dense(1)(x)
        model = Model(inputs, outputs)
        return model

    def choose_action(self, state):
        actions = []    
        for index, actor in enumerate(self.actors):
            prob = actor.predict(state)[0]
            print(f"Agent {index} action probabilities: {prob}")
            action = np.random.choice(self.num_actions, p=prob)
            actions.append(action)
            print(f"Agent {index} chose action: {action}")
        return actions

    
    def get_trainable_variables(self):
        trainable_variables = []
        for actor, critic in zip(self.actors, self.critics):
            trainable_variables += actor.trainable_variables
            trainable_variables += critic.trainable_variables
        return trainable_variables

    def train(self, state, action, shared_reward, next_state, done):
        for i, (actor, critic) in enumerate(zip(self.actors, self.critics)):
            with tf.GradientTape() as actor_tape, tf.GradientTape() as critic_tape:
                critic_value = critic(state)
                critic_value_next = critic(next_state)
                target = shared_reward + self.gamma * critic_value_next * (1 - int(done))
                delta = target - critic_value

                actor_probs = actor(state)
                action_probs = actor_probs[0, action[i]]
                actor_loss = -tf.math.log(action_probs) * delta
                critic_loss = tf.keras.losses.MSE(critic_value, target)

            actor_grads = actor_tape.gradient(actor_loss, actor.trainable_variables)
            critic_grads = critic_tape.gradient(critic_loss, critic.trainable_variables)

            actor_grads = [tf.clip_by_value(g, -1.0, 1.0) for g in actor_grads if g is not None]
            critic_grads = [tf.clip_by_value(g, -1.0, 1.0) for g in critic_grads if g is not None]

            if actor_grads and critic_grads:
                self.actor_optimizer.apply_gradients(zip(actor_grads, actor.trainable_variables))
                self.critic_optimizer.apply_gradients(zip(critic_grads, critic.trainable_variables))

class ConfigEnvironment:
    def __init__(self):
        self.param_options = {
            "R": [1, 2, 3, 4, 5],
            "L": [1, 2, 3, 4, 5],
            "C": [1, 2, 3, 4, 5],
            "rectifier_diodes": [1, 2, 3, 4, 5],
            "schottky_diodes": [1, 2, 3, 4, 5],
            "zener_diodes": [1, 2, 3, 4, 5],
            "leds": [1, 2, 3, 4, 5],
            "Q_BJT": [1, 2, 3, 4, 5],
            "Q_FET": [1, 2, 3, 4, 5],
            "Q_JFET": [1, 2, 3, 4, 5],
            "Q_MOSFET": [1, 2, 3, 4, 5],
            "Q_IGBT": [1, 2, 3, 4, 5],
            "Branch": [1, 1, 1, 1,1],
        }

        self.state = {param: np.random.choice(options) for param, options in self.param_options.items()}

    def step(self, actions):
        print(f"Current state: {self.state}, actions: {actions}")

        for param, action in actions.items():
            self.state[param] = self.param_options[param][action]

        next_state = self.state

        state_values = [f"{key}={value}" for key, value in next_state.items()]
        print(f"state_values: {state_values}")

        orginal_config_file_path = './ConfigFile.txt'  
        shutil.copy(orginal_config_file_path, case_folder)
        config_file_path = f"{case_folder}/ConfigFile.txt"
        config_update(config_file_path, state_values)
        #调用PCB_case_generate开始生成测试用例
        PCB_case_generate(case_folder,config_file_path)

        #将C:\Users\dell\Desktop\new_result下的NetlistsResults文件夹以及PCBSmith10GenV43.txt文件复制到case_folder文件夹下
        # 目标文件夹路径
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
        time.sleep(10) 

        #base_path为case_folder文件夹下的NetlistsResults文件夹
        base_path = f"{case_folder}/Netlist"
        #bug_file为case_folder文件夹下的PCBSmith10GenV43.txt
        bug_file_path = f"{case_folder}/ResultV43.txt"

        try:
            reward = get_rewards(base_path,bug_file_path)
            print("##############################")
            print("Rewards:", reward)
        except Exception as e:
            print(f"An error occurred while getting fitness_candidate: {e}")
            reward = 0
        print(f"Next state: {next_state}, reward: {reward}")

        return next_state, reward

    def reset(self):
        self.state = {param: np.random.choice(options) for param, options in self.param_options.items()}
        return self.state

    def get_state_vector(self):
        return np.array(list(self.state.values())).reshape(1, -1)

num_parameters = len(ConfigEnvironment().param_options)
num_actions = 5  
state_dim = num_parameters 

actor_lr = 0.001     
critic_lr = 0.005    
gamma = 0.99         

a2c_agents = MultiAgentA2C(num_parameters, num_actions, state_dim, actor_lr, critic_lr, gamma)
env = ConfigEnvironment()
trainable_variables = a2c_agents.get_trainable_variables()
a2c_agents.actor_optimizer.build(trainable_variables)
a2c_agents.critic_optimizer.build(trainable_variables)

def create_case_folder(episode):
    case_base_path = './case_generation'
    case_folder = f"{case_base_path}/case_generation_{episode}"

    if not os.path.exists(case_folder):
        os.makedirs(case_folder)
        
    return case_folder

for episode in range(300):
    state = env.reset()
    state_vector = env.get_state_vector()
    total_reward = 0

    for step in range(10):
        
        new_counter = step + episode * 10    
        case_folder = create_case_folder(new_counter)
        # bug_folder = create_bug_folder(new_counter)
        print("new_counter: ",new_counter)

        actions = a2c_agents.choose_action(state_vector)
        actions_dict = {param: action for param, action in zip(env.param_options.keys(), actions)}
        next_state, reward = env.step(actions_dict)
        next_state_vector = env.get_state_vector()
        total_reward += reward

        time.sleep(10) 
        done = False  
        a2c_agents.train(state_vector, actions, total_reward, next_state_vector, done)
        state_vector = next_state_vector

    print(f"Episode {episode} - Total Reward: {total_reward}")