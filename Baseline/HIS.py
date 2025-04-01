import numpy as np
import random
import shutil
from config_update import config_update
# from get_PSO_case import case_generate
# from ops_folder_generation import create_case_folder, create_bug_folder
from new_cover_main import get_rewards
from bug_counts import bug_counts_main
import os
import  time
from MainSchGen import *

# 假设的适应度函数
def fitness_function(base_path,bug_file_path):

    fitness_value = get_rewards(base_path,bug_file_path)
    
    return fitness_value

class Particle:
    def __init__(self, num_selected_arms):
        self.position = np.array([random.randint(0, len(arm_candidates[i])-1) for i in range(num_selected_arms)])
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([random.random() for _ in range(num_selected_arms)])

    def update_velocity(self, gbest_position):
        w = 0.5  # 惯性权重
        c1 = 1  # 个体学习因子
        c2 = 2  # 社会学习因子

        for i in range(len(self.position)):
            r1, r2 = random.random(), random.random()
            cognitive_velocity = c1 * r1 * (self.pbest_position[i] - self.position[i])
            social_velocity = c2 * r2 * (gbest_position[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive_velocity + social_velocity

    def update_position(self, arm_candidates):
        for i in range(len(self.position)):
            self.velocity[i] = max(min(self.velocity[i], len(arm_candidates[i]) - 1), -len(arm_candidates[i]) + 1)
            self.position[i] = int(max(0, min(len(arm_candidates[i])-1, self.position[i] + self.velocity[i])))

    def get_parameters(self, arm_index_to_params, arm_candidates):
        return [arm_index_to_params[arm_candidates[i][int(self.position[i])]] for i in range(len(self.position))]

class PSO:
    def __init__(self, fitness_function, num_selected_arms, num_particles):
        self.fitness_function = fitness_function
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.randint(0, len(arm_candidates[i])-1) for i in range(num_selected_arms)])
        self.particles = [Particle(num_selected_arms) for _ in range(num_particles)]

    def run(self, num_iterations, arm_index_to_params, arm_candidates):
        for iteration in range(num_iterations):
            print(f"Generation {iteration + 1}/{num_iterations}")
            counter = 0
            for particle in self.particles:

                #新增一个计数器，从1开始，每次循环加1，当计数器等于粒子数量时，说明已经遍历完所有粒子               
                counter += 1
                new_counter = counter + iteration * 10
                case_folder = create_case_folder(new_counter)
                
                parameters = particle.get_parameters(arm_index_to_params, arm_candidates)

                orginal_config_file_path = './ConfigFile.txt'  
                shutil.copy(orginal_config_file_path, case_folder)
                config_file_path = f"{case_folder}/ConfigFile.txt"
                config_update(config_file_path, parameters)
                # 调用PCB_case_generate开始生成测试用例
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
                time.sleep(10) 

                #base_path为case_folder文件夹下的NetlistsResults文件夹
                base_path = f"{case_folder}/NetlistsResults"
                #bug_file为case_folder文件夹下的PCBSmith10GenV43.txt
                bug_file_path = f"{case_folder}/PCBSmith10GenV43.txt"

                try:
                    fitness_candidate = self.fitness_function(base_path,bug_file_path)
                    print("##############################")
                    print("Rewards:", fitness_candidate)
                except Exception as e:
                    print(f"An error occurred while getting fitness_candidate: {e}")
                    fitness_candidate = 0

                # fitness_candidate = self.fitness_function(parameters)

                print(f"  Particle Position: {particle.position}")
                print(f"  Parameters: {parameters}")
                print(f"  Fitness: {fitness_candidate}")

                if particle.pbest_value > fitness_candidate:
                    particle.pbest_value = fitness_candidate
                    particle.pbest_position = particle.position

                if self.gbest_value > fitness_candidate:
                    self.gbest_value = fitness_candidate
                    self.gbest_position = particle.position

            for particle in self.particles:
                particle.update_velocity(self.gbest_position)
                particle.update_position(arm_candidates)

            print(f"Best position in this generation: {self.gbest_position}")
            print(f"Best fitness in this generation: {self.gbest_value}\n")

# 定义每组参数的可选项
arm_candidates = [
    [0, 1, 2, 3 ,4],
    [5, 6, 7, 8, 9],
    [10, 11, 12, 13 ,14],
    [15, 16, 17, 18, 19],
    [20, 21, 22, 23 ,24],
    [25, 26, 27, 28, 29],
    [30, 31, 32, 33 ,34],
    [35, 36, 37, 38, 39],
    [40, 41, 42, 43 ,44],
    [45, 46, 47, 48, 49],
    [50, 51, 52, 53 ,54],
    [55, 56, 57, 58, 59],
    [60, 61, 62, 63 ,64],
]

# 定义参数映射字典
arm_index_to_params = {
        0: "R = 1",
        1: "R = 2",
        2: "R = 3",
        3: "R = 4",
        4: "R = 5",
        5: "L = 1",
        6: "L = 2",
        7: "L = 3",
        8: "L = 4",
        9: "L = 5",
        10: "C = 1",
        11: "C = 2",
        12: "C = 3",
        13: "C = 4",
        14: "C = 5",
        15: "rectifier_diodes = 1",
        16: "rectifier_diodes = 2",
        17: "rectifier_diodes = 3",
        18: "rectifier_diodes = 4",
        19: "rectifier_diodes = 5",
        20: "schottky_diodes = 1",
        21: "schottky_diodes = 2",
        22: "schottky_diodes = 3",
        23: "schottky_diodes = 4",
        24: "schottky_diodes = 5",
        25: "zener_diodes = 1",
        26: "zener_diodes = 2",
        27: "zener_diodes = 3",
        28: "zener_diodes = 4",
        29: "zener_diodes = 5",
        30: "leds = 1",
        31: "leds = 2",
        32: "leds = 3",
        33: "leds = 4",
        34: "leds = 5",
        35: "Q_BJT = 1",
        36: "Q_BJT = 2",
        37: "Q_BJT = 3",
        38: "Q_BJT = 4",
        39: "Q_BJT = 5",
        40: "Q_FET = 1",
        41: "Q_FET = 2",
        42: "Q_FET = 3",
        43: "Q_FET = 4",
        44: "Q_FET = 5",
        45: "Q_JFET = 1",
        46: "Q_JFET = 2",
        47: "Q_JFET = 3",
        48: "Q_JFET = 4",
        49: "Q_JFET = 5",
        50: "Q_MOSFET = 1",
        51: "Q_MOSFET = 2",
        52: "Q_MOSFET = 3",
        53: "Q_MOSFET = 4",
        54: "Q_MOSFET = 5",
        55: "Q_IGBT = 1",
        56: "Q_IGBT = 2",
        57: "Q_IGBT = 3",
        58: "Q_IGBT = 4",
        59: "Q_IGBT = 5",
        60: "Branch = 1",
        61: "Branch = 1",
        62: "Branch = 1",
        63: "Branch = 1",
        64: "Branch = 1",
    }

def create_case_folder(episode):
    case_base_path = './baseline_case_and_bug_generation'
    case_folder = f"{case_base_path}/PSO/case_generation/case_generation_{episode}"

    if not os.path.exists(case_folder):
        os.makedirs(case_folder)
        
    return case_folder

def main():
    num_selected_arms = 13  # 总共需要选择的参数组数
    num_particles = 10  # 粒子数量
    num_iterations = 300  # 迭代次数

    pso = PSO(fitness_function, num_selected_arms, num_particles)
    pso.run(num_iterations, arm_index_to_params, arm_candidates)

    print("最优参数索引:", pso.gbest_position)
    optimal_params = [arm_index_to_params[arm_candidates[i][int(pso.gbest_position[i])]] for i in range(num_selected_arms)]
    print("映射后的最优参数:", optimal_params)

if __name__ == '__main__':
    main()
