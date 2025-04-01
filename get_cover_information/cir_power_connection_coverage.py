import re

def parse_cir_file(cir_file):
    """
    解析 .cir 网表文件，提取电源连接信息。
    """
    power_nodes = set()  # 存储电源节点
    connections = []  # 存储所有连接的节点对（即元件的端口连接）
    
    with open(cir_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()

            # 跳过空行和注释行
            if not line or line.startswith('*'):
                continue

            # 解析元件连接（电阻、电容等）
            match = re.match(r'([RCQVDLICSWX])(\w+)\s+([^\s]+)\s+([^\s]+)\s+([\d\.kMG]*)', line)
            if match:
                node1 = match.group(3)  # 第一个连接节点
                node2 = match.group(4)  # 第二个连接节点
                connections.append((node1, node2))  # 记录连接的节点对
                # 检查节点是否为电源节点（假设电源节点为 "V" 或 "P" 开头）
                if node1.startswith("V") or node1.startswith("P"):  # 电源节点通常以 "V" 或 "P" 开头
                    power_nodes.add(node1)
                if node2.startswith("V") or node2.startswith("P"):
                    power_nodes.add(node2)

    return power_nodes, connections

def dfs(node, visited, graph):
    """
    使用深度优先搜索 (DFS) 遍历图中的所有节点。
    """
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, graph)

def cir_calculate_power_connection_coverage(cir_file):
    """
    根据网表文件计算电源连接覆盖率，检查电源节点是否连通。
    """
    # 获取网表中的所有电源节点和连接
    power_nodes, connections = parse_cir_file(cir_file)

    # 如果没有电源节点，直接返回 0（无电源连接）
    if not power_nodes:
        print("No power nodes found in the circuit.")
        return 0

    # 构建图（邻接表表示法）
    graph = {node: [] for node in power_nodes}
    for node1, node2 in connections:
        if node1 in power_nodes:
            graph[node1].append(node2)
        if node2 in power_nodes:
            graph[node2].append(node1)

    # 检查连通性：从电源节点开始深度优先搜索（DFS）
    visited = set()
    dfs(next(iter(power_nodes)), visited, graph)

    # 如果访问的电源节点数量等于总电源节点数量，说明所有电源节点都是连通的
    if len(visited) == len(power_nodes):
        power_connection_coverage = 100
    else:
        power_connection_coverage = (len(visited) / len(power_nodes)) * 100

    return power_connection_coverage

# # 示例网表文件路径
# cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir'
# #打印cir_file文件中的内容
# with open(cir_file, 'r') as f:
#     print(f.read())

# # 计算电源连接覆盖率
# coverage = cir_calculate_power_connection_coverage(cir_file)

# # 打印结果
# print(f"Power Connection Coverage: {coverage}%")
