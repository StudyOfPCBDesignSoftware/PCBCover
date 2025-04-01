#连接覆盖率的定义连接覆盖率 主要衡量的是电路中所有 元件引脚之间的连接 是否 完整且被仿真工具考虑。如果某个元件的引脚未与任何其他元件连接或遗漏了连接，这将影响电路的正常工作，也可能导致仿真错误。
#计算方式
#所有元件的连接：首先，您需要提取 网表中所有元件 的连接信息。每个元件通常有两个或更多引脚，每个引脚连接到电路中的 其他元件 或 节点（如电源、地线等）。
#确保每个连接都被定义：接下来，您需要确保每个元件的连接在网表文件中被完整定义，并没有遗漏任何连接。
#计算连接覆盖率：
#如果网表中 所有定义的连接 都被列出并且没有遗漏，则 连接覆盖率 为 100%。
#如果某些连接被遗漏或未正确定义，则连接覆盖率低于 100%。

import re

def parse_cir_file(cir_file):
    """
    解析 .cir 网表文件，提取节点对（即连接的节点）。
    """
    connections = []  # 存储所有连接的节点对
    nodes = set()     # 存储所有节点

    with open(cir_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()

            # 跳过空行和注释行
            if not line or line.startswith('*'):
                continue

            # 解析元件连接（两个节点之间的连接）
            match = re.match(r'([RCQVDLICSWX])(\w+)\s+([^\s]+)\s+([^\s]+)\s+([\d\.kMG]*)', line)
            if match:
                node1 = match.group(3)  # 第一个连接节点
                node2 = match.group(4)  # 第二个连接节点
                connections.append((node1, node2))  # 记录连接的节点对
                nodes.add(node1)  # 添加节点1
                nodes.add(node2)  # 添加节点2

    return connections, nodes

def dfs(node, visited, graph):
    """
    使用深度优先搜索 (DFS) 遍历图中的所有节点。
    """
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, graph)

def cir_calculate_connection_coverage_main(cir_file):
    """
    根据网表文件计算连接覆盖率，检查所有节点是否连通。
    """
    # 获取网表中的所有连接和节点
    connections, nodes = parse_cir_file(cir_file)

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
        connection_coverage = 100
    else:
        connection_coverage = (len(visited) / len(nodes)) * 100

    return connection_coverage

    # # 示例网表文件路径
    # cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir'
    # #打印cir_file文件中的内容
    # with open(cir_file, 'r') as f:
    #     print(f.read())

    # # 计算并打印连接覆盖率
    # coverage = cir_calculate_connection_coverage_main(cir_file)
    # print(f"Connection Coverage: {coverage}%")