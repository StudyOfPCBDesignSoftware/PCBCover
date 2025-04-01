#元件类型覆盖率计算：统计网表中实际使用的元件实例数（如 R1, C1 等），并与元件库中定义的元件总数进行比较。
import re

# 假设一个简单的元件库，包括一些典型的元件类型
component_library = {
    'R': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6','R7','R8'],  # 电阻
    'C': ['C1', 'C2', 'C3', 'C4', 'C5'],  # 电容
    'L': ['L1', 'L2'],  # 电感
    'Q': ['Q1', 'Q2', 'Q3'],  # 晶体管（BJT）
    'M': ['M1', 'M2'],  # MOSFET（场效应管）
    'D': ['D1', 'D2', 'D3'],  # 二极管
    'VD': ['VD1', 'VD2'],  # 变压器（Voltage-controlled Diode）
    'V': ['V1'],  # 电源（DC）
    'ACV': ['V2'],  # 交流电源
    'P': ['P1'],  # 光电二极管等
    'IC': ['IC1', 'IC2', 'IC3'],  # 集成电路（如运算放大器）
    'X': ['X1', 'X2'],  # 子电路（Subcircuit）
    'SW': ['SW1'],  # 开关
    'SRC': ['SRC1'],  # 电流源
    'GND': ['GND'],  # 地
    # 可能还会有更多的电路元件类型
}


def parse_cir_file(cir_file):
    """
    解析 .cir 网表文件，提取元件信息。
    """
    used_components = set()  # 存储使用的元件类型

    with open(cir_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith('*') or not line:  # 跳过注释行或空行
                continue

            # 匹配元件类型和名称
            match = re.match(r'([RCQVD])(\w+)', line)
            if match:
                component_type = match.group(1)  # 电阻（R）、电容（C）、晶体管（Q）等
                component_name = match.group(2)
                used_components.add(component_type)  # 添加使用的元件类型

    return used_components

def calculate_component_type_coverage_main(cir_file):
    """
    根据网表文件计算元件覆盖率。
    """
    used_components = parse_cir_file(cir_file)

    # 计算元件库中的元件类型数
    total_component_types = len(component_library)

    # 计算网表中使用的元件类型数
    covered_component_types = len(used_components)

    # 元件类型覆盖率
    component_type_coverage = (covered_component_types / total_component_types) * 100

    return component_type_coverage

# # 示例网表文件路径
# cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir'
# #打印cir_file文件中的内容
# with open(cir_file, 'r') as f:
#     print(f.read())

# # 计算元件覆盖率
# coverage = calculate_component_coverage(cir_file)

# # 打印结果
# print(f"Component Coverage: {coverage}%")
