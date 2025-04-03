# 1. Tool Introduction

Defects in printed circuit board (PCB) design toolchains can lead to functional errors. If such defective PCBs are applied in safety-critical domains such as aerospace or healthcare, they may cause serious consequences. Therefore, ensuring the reliability of PCB design toolchains is of vital importance.

Existing testing methods mainly rely on manually designed test cases or randomly generated circuits based on fixed configurations. These methods lack effective guidance for generating high-quality test samples, resulting in limited defect-triggering capability.

Addressing the limitations of current methods in defect detection mainly involves two key challenges:

- How to evaluate the effectiveness of parameter configurations  
- How to efficiently search for optimal configurations in a large parameter space

To address these challenges, we propose an automated testing approach named **PCBCover**. This method integrates coverage feedback with an A2C-based reinforcement learning algorithm to automatically generate schematics, significantly enhancing the defect-triggering capability of the generated circuits (test cases).

**PCBCover** consists of three core components:

- **Coverage extraction module**
- **A2C-based dynamic configuration search module**
- **Differential testing-based defect detection module**

To quantify the effectiveness of parameter configurations, PCBCover defines two types of coverage metrics — **static (netlist)** and **dynamic (simulation)** — and uses them as reward signals to guide the generator toward discovering configurations with a higher likelihood of triggering defects.

---

# 2. Project Structure

The project contains the following three subdirectories:

### 1. `Baseline` Folder

Contains baseline algorithm implementations used for comparison with PCBCover, including:

- `HIS`
- `RECORD`
- `Swarm`

> 🔹 **Note**: For the default method (`PCBSmith`), please download it separately.

---

### 2. `get_cover_information` Folder

Contains scripts for extracting:

- **Netlist coverage**
- **Simulation coverage**

---

### 3. `main` Folder

Main execution directory. Key files include:

- `PCBCover`: The main execution file
- `config_update`: Responsible for updating configuration files
