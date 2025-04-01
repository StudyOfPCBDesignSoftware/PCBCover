#元件实例覆盖率：定义：衡量的是 网表中实际使用的元件实例（例如 R1、C1、Q1 等）与 元件库中所有元件实例（例如 R1、R2、R3、C1、C2 等）的比例。这个计算衡量的是您设计中的元件 具体实例 是否得到了全面使用。
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
    解析 .cir 网表文件，提取元件实例。
    """
    used_components = set()  # 存储使用的元件实例

    with open(cir_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()

            # 跳过空行和注释行
            if not line or line.startswith('*'):
                continue

            # 解析元件实例
            match = re.match(r'([RCQVDLICSWX])(\w+)\s+([^\s]+)\s+([^\s]+)\s+([\d\.kMG]*)', line)
            if match:
                component_name = match.group(2)  # 元件实例名称（如R1, C1）
                used_components.add(component_name)  # 记录使用的元件实例

    return used_components

def calculate_component_coverage_cir_main(cir_file):
    """
    根据网表文件计算元件覆盖率。
    """
    used_components = parse_cir_file(cir_file)

    # 计算元件库中的元件实例数
    total_components = sum(len(component_library[comp_type]) for comp_type in component_library)

    # 计算网表中使用的元件实例数
    covered_components = len(used_components)

    # 计算元件覆盖率
    component_coverage = (covered_components / total_components) * 100 if total_components > 0 else 0

    return component_coverage

# # 示例网表文件路径
# cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir'
# #打印cir_file文件中的内容
# with open(cir_file, 'r') as f:
#     print(f.read())

# # 计算元件覆盖率
# coverage = calculate_component_coverage_cir_main(cir_file)

# # 打印结果
# print(f"Component Coverage: {coverage}%")
