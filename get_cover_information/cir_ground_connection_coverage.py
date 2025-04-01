#接地连接，即电路中所有需要接地的部分是否都正确连接到地线（GND）。
# 计算重点	确保电路中每个需要接地的元件、节点等都连接到 地线（GND）
import re

def parse_cir_file(cir_file):
    """
    解析 .cir 网表文件，提取接地连接信息。
    """
    ground_nodes = set()  # 存储接地节点
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
                # 检查节点是否为接地节点（假设接地节点为 "0"）
                if node1 == "0":
                    ground_nodes.add(node1)
                if node2 == "0":
                    ground_nodes.add(node2)

    return ground_nodes, connections

def dfs(node, visited, graph):
    """
    使用深度优先搜索 (DFS) 遍历图中的所有节点。
    """
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, graph)

def cir_calculate_ground_connection_coverage_main(cir_file):
    """
    根据网表文件计算接地连接覆盖率，检查接地节点是否连通。
    """
    # 获取网表中的所有接地节点和连接
    ground_nodes, connections = parse_cir_file(cir_file)

    # 如果没有接地节点，直接返回 0（无接地连接）
    if not ground_nodes:
        # print("No ground nodes found in the circuit.")
        return 0

    # 构建图（邻接表表示法）
    graph = {node: [] for node in ground_nodes}
    for node1, node2 in connections:
        if node1 in ground_nodes:
            graph[node1].append(node2)
        if node2 in ground_nodes:
            graph[node2].append(node1)

    # 检查连通性：从接地节点开始深度优先搜索（DFS）
    visited = set()
    dfs(next(iter(ground_nodes)), visited, graph)

    # 如果访问的接地节点数量等于总接地节点数量，说明所有接地节点都是连通的
    if len(visited) == len(ground_nodes):
        ground_connection_coverage = 100
    else:
        ground_connection_coverage = (len(visited) / len(ground_nodes)) * 100

    return ground_connection_coverage

# # 示例网表文件路径
# cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir'
# #打印cir_file文件中的内容
# with open(cir_file, 'r') as f:
#     print(f.read())

# # 计算接地连接覆盖率
# coverage = cir_calculate_ground_connection_coverage_main(cir_file)

# # 打印结果
# print(f"Ground Connection Coverage: {coverage}%")
