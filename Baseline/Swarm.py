import random
from config_update import config_update
import os
import shutil
from glob import glob
from new_cover_main import get_rewards
from bug_counts import bug_counts_main
from MainSchGen import *

def get_bug_number(SOURCE_DIR,DEST_DIR): 

    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR, exist_ok=True)


    # def get_file_and_folder_count(folder_path):
    #     file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    #     folder_count = len([name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))])
    #     return file_count + folder_count  

    # for folder in glob(os.path.join(SOURCE_DIR, "fuzz_*/")):
    #     total_count = get_file_and_folder_count(folder)

    #     if total_count != 7:
    #         folder_name = os.path.basename(folder.rstrip('/'))
    #         shutil.copytree(folder, os.path.join(DEST_DIR, folder_name), dirs_exist_ok=True)

    # bug_number = get_file_and_folder_count(DEST_DIR)
    # return bug_number

def create_case_folder(episode):
    case_base_path = './baseline_case_and_bug_generation'
    case_folder = f"{case_base_path}/Swarm/case_generation/case_generation_{episode}"

    if not os.path.exists(case_folder):
        os.makedirs(case_folder)
        
    return case_folder

# def create_bug_folder(episode):
#     bug_base_path = './baseline_case_and_bug_generation'
#     bug_folder = f"{bug_base_path}/Swarm/bug_generation/bug_generation_{episode}"

#     if not os.path.exists(bug_folder):
#         os.makedirs(bug_folder)
        
#     return bug_folder


def choose_arms(num_selected_arms):
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

    chosen_arms = []
    for i in range(num_selected_arms):
        chosen_arm = random.choice(arm_candidates[i])
        chosen_arms.append(chosen_arm)

    return chosen_arms

def perform_swarm_test(num_tests, num_selected_arms, arm_index_to_params):
    for test_num in range(num_tests):
        case_folder = create_case_folder(test_num)
        # bug_folder = create_bug_folder(test_num)

        selected_arms = choose_arms(num_selected_arms)

        selected_params = [arm_index_to_params[arm] for arm in selected_arms]
        print(f"Test {test_num}: Selected Parameters: {selected_params}")


        orginal_config_file_path = './ConfigFile.txt'  
        shutil.copy(orginal_config_file_path, case_folder)
        config_file_path = f"{case_folder}/ConfigFile.txt"
        config_update(config_file_path, selected_params)
        PCB_case_generate(case_folder,config_file_path)

        # #后续需要修改路径
        # #将C:\Users\dell\Desktop\new_result下的PCBSmith10GenV43.txt文件复制到case_folder文件夹下
        # shutil.copy('C:\\Users\\dell\\Desktop\\new_result\\PCBSmith10GenV43.txt', f"{case_folder}/PCBSmith10GenV43.txt")

        #bug_file为case_folder文件夹下的PCBSmith10GenV43.txt
        bug_file_path = f"{case_folder}/PCBSmith10GenV43.txt"

        try:
            bug_number = bug_counts_main(bug_file_path)
            print("##############################")
            print("bug_number:", bug_number)
        except Exception as e:
            print(f"An error occurred while getting fitness_candidate: {e}")
            bug_number = 0

    return bug_number


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

num_tests = 2000  
num_selected_arms = 13  
perform_swarm_test(num_tests, num_selected_arms, arm_index_to_params)
