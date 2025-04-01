import re

# 计算元件执行覆盖率
def calculate_component_coverage(node_voltages, components):
    """
    计算元件执行覆盖率
    :param node_voltages: 仿真中提取的节点电压数据
    :param components: 元件与其相关节点的字典，每个元件与一个节点列表相关联
    :return: 元件执行覆盖率百分比
    """
    activated_components = 0  # 计数被激活的元件

    for component, associated_nodes in components.items():
        # 检查该元件的所有节点是否都有电压数据
        # print(f"元件 '{component}': {associated_nodes}")
        if all(node in node_voltages for node in associated_nodes):
            activated_components += 1  # 如果所有节点都有电压数据，认为该元件被激活
            # print(f"元件 '{component}' 被激活")

    total_components = len(components)  # 总元件数

    if total_components > 0:
        # 计算元件执行覆盖率
        # print(f"总元件数: {total_components}")
        component_coverage = (activated_components / total_components) * 100
    else:
        component_coverage = 0

    return component_coverage

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

# 从CIR网表文件中提取元件与其相关节点
def extract_components_from_netlist(cir_file):
    """
    从CIR网表文件中提取元件与其相关节点
    :param cir_file: CIR网表文件路径
    :return: 元件与其相关节点的字典，键是元件名，值是节点列表
    """
    components = {}
    
    with open(cir_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 忽略以 . 开头的行（如 .title, .tran, .options）
            if line.strip().startswith(('.', '')):  # 处理网表中的控制指令行
                if line.strip().startswith(('.title', '.TRAN', '.options')):  # 跳过这几行
                    continue
            
            # 匹配每个元件与它连接的两个节点
            match = re.match(r"\s*(\S+)\s+(\S+)\s+(\S+)", line)  # 元件名、节点1、节点2
            if match:
                component = match.group(1).lower()  # 获取元件名称并转小写
                node1 = match.group(2).lower()  # 获取第一个节点并转小写
                node2 = match.group(3).lower()  # 获取第二个节点并转小写

                # 使用集合避免重复节点
                if component not in components:
                    components[component] = {node1, node2}
                else:
                    components[component].update([node1, node2])

    return components

def calculate_component_cover_main(log_file, cir_file):
    # log_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\simresult\\111.log'  # 仿真日志文件路径
    # cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir'  # CIR 网表文件路径

    # 提取仿真日志中的节点电压数据
    node_voltages = extract_node_voltages(log_file)
    # 从网表中提取元件与其相关节点
    components = extract_components_from_netlist(cir_file)

    # 计算元件执行覆盖率
    component_coverage = calculate_component_coverage(node_voltages, components)
    # print(f"元件执行覆盖率: {component_coverage}%")
    return component_coverage

# if __name__ == "__main__":
#     main()
