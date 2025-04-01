#节点电压覆盖率（Node Voltage Coverage） 是指电路中 每个节点的电压 是否都被定义并计算。通常，在电路仿真中，我们会计算每个节点的电压，确保电路中每个节点的电压都得到了验证。
import re

def parse_cir_file(cir_file):
    """
    解析 .cir 网表文件，提取节点信息。
    """
    nodes = set()  # 存储所有节点
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
                nodes.add(node1)  # 添加节点1
                nodes.add(node2)  # 添加节点2

    return nodes, connections

def dfs(node, visited, graph):
    """
    使用深度优先搜索 (DFS) 遍历图中的所有节点。
    """
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, graph)

def cir_calculate_node_coverage_main(cir_file):
    """
    根据网表文件计算节点覆盖率，检查所有节点是否连通。
    """
    # 获取网表中的所有连接和节点
    nodes, connections = parse_cir_file(cir_file)

    # 构建图（邻接表表示法）
    graph = {node: [] for node in nodes}
    for node1, node2 in connections:
        graph[node1].append(node2)
        graph[node2].append(node1)  # 因为是无向图，反向连接也需要加入

    # 检查连通性：从任意一个节点开始深度优先搜索（DFS）
    visited = set()
    dfs(next(iter(nodes)), visited, graph)

    # 如果访问的节点数量等于总节点数量，说明所有节点都是连通的
    if len(visited) == len(nodes):
        node_coverage = 100
    else:
        node_coverage = (len(visited) / len(nodes)) * 100

    return node_coverage

# # 示例网表文件路径
# cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir'
# #打印cir_file文件中的内容
# with open(cir_file, 'r') as f:
#     print(f.read())

# # 计算节点覆盖率
# coverage = cir_calculate_node_coverage_main(cir_file)

# # 打印结果
# print(f"Node Coverage: {coverage}%")
