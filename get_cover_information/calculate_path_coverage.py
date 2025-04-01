#路径覆盖率
import re

# 从仿真日志中提取节点电压数据
def extract_node_voltages(log_file):
    """
    从仿真日志中提取节点的电压信息
    :param log_file: 仿真日志文件路径
    :return: 节点名与电压数据的字典
    """
    node_voltages = {}

    with open(log_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 查找每一行的节点电压数据，假设日志格式类似于：
            # net-_d3-k_ 0.000258873
            match = re.match(r"([a-zA-Z0-9\-_]+)\s+([+-]?\d*\.\d+|\d+)", line)
            if match:
                node = match.group(1)  # 获取节点名称
                voltage = float(match.group(2))  # 获取电压值
                node_voltages[node] = voltage

    return node_voltages

# 从CIR网表文件中提取路径（节点对）
def extract_paths_from_netlist(cir_file):
    """
    从CIR网表文件中提取路径，每个路径由两个节点构成
    :param cir_file: CIR网表文件路径
    :return: 路径列表，每个路径为一个节点对
    """
    paths = []
    with open(cir_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 查找每一行定义的节点对，例如 C1 Net-_D3-K_ Net-_C1-Pad2_
            # 忽略XQ元件类型，只提取以 "Net-" 开头的节点
            match = re.match(r"\s*(\S+)\s+(\S+)\s+(\S+)", line)  # 元件名、节点1、节点2
            if match:
                component = match.group(1)  # 获取元件名称（例如 C1, R1 等）
                node1 = match.group(2).lower()  # 获取第一个节点，并转为小写
                node2 = match.group(3).lower()  # 获取第二个节点，并转为小写

                # 如果元件是XQ类型，跳过此元件
                if component.lower().startswith('xq'):
                    continue

                # 只添加以 "Net-" 开头的有效路径（两个节点）
                if node1.startswith('net-') and node2.startswith('net-') and node1 != node2:
                    paths.append((node1, node2))

    # 打印提取的路径（用于调试）
    # print(f"提取的路径: {paths}")
    return paths

# 计算路径覆盖率
def calculate_path_coverage(node_voltages, paths):
    """
    计算路径覆盖率
    :param node_voltages: 仿真中提取的节点电压数据
    :param paths: 电路中定义的路径列表，每个路径由两个节点构成，如 [("Net1", "Net2"), ("Net2", "Net3")]
    :return: 路径覆盖率百分比
    """
    activated_paths = 0  # 计数被激活的路径

    for path in paths:
        node1, node2 = path
        # 检查路径中的两个节点是否都在仿真数据中有电压
        if node1 in node_voltages and node2 in node_voltages:
            activated_paths += 1  # 如果这两个节点都有电压数据，认为这条路径被激活

    total_paths = len(paths)  # 总路径数
    if total_paths > 0:
        # 计算路径覆盖率
        path_coverage = (activated_paths / total_paths) * 100
    else:
        path_coverage = 0

    return path_coverage

# 示例：计算路径覆盖率
def calculate_path_coverage_main(log_file, cir_file):
    # log_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\simresult\\111.log'  # 仿真日志文件路径
    # cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir'  # CIR 网表文件路径

    # 提取仿真日志中的节点电压数据
    node_voltages = extract_node_voltages(log_file)

    # 从网表中提取路径
    paths = extract_paths_from_netlist(cir_file)

    # 计算路径覆盖率
    path_coverage = calculate_path_coverage(node_voltages, paths)
    # print(f"路径覆盖率: {path_coverage}%")
    return path_coverage

# if __name__ == "__main__":
#     main()
