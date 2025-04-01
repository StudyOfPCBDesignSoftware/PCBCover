#节点仿真执行覆盖率
from PyLTSpice import RawRead
import numpy as np
import re

# 读取 .raw 文件并提取数据
def extract_spice_data(raw_file):
    """
    使用 PyLTSpice 解析 .raw 文件并提取节点数据
    """
    # 加载 .raw 文件
    raw_data = RawRead(raw_file)
    
    # 获取所有节点名称
    node_names = raw_data.get_trace_names()
    # print(f"节点名称: {node_names}")

    # 获取节点电压
    node_voltages = {}
    for node in node_names:
        node_voltages[node] = raw_data.get_trace(node)
        
    return node_voltages

# 读取网表文件并提取节点名称
import re

# 读取网表文件并提取节点名称
import re
from PyLTSpice import RawRead
import numpy as np

# 读取 .raw 文件并提取数据
def extract_spice_data(raw_file):
    """
    使用 PyLTSpice 解析 .raw 文件并提取节点数据
    """
    # 加载 .raw 文件
    raw_data = RawRead(raw_file)
    
    # 获取所有节点名称
    node_names = raw_data.get_trace_names()
    # print(f"节点名称: {node_names}")

    # 获取节点电压
    node_voltages = {}
    for node in node_names:
        node_voltages[node] = raw_data.get_trace(node)
        
    return node_voltages

# 读取网表文件并提取节点名称
import re
from PyLTSpice import RawRead
import numpy as np

# 读取 .raw 文件并提取数据
def extract_spice_data(raw_file):
    """
    使用 PyLTSpice 解析 .raw 文件并提取节点数据
    """
    # 加载 .raw 文件
    raw_data = RawRead(raw_file)
    
    # 获取所有节点名称
    node_names = raw_data.get_trace_names()
    # print(f"节点名称: {node_names}")

    # 获取节点电压
    node_voltages = {}
    for node in node_names:
        node_voltages[node] = raw_data.get_trace(node)
        
    return node_voltages

# 读取网表文件并提取节点名称
# 读取网表文件并提取节点名称
def extract_netlist_nodes(cir_file):
    """
    提取网表文件中的所有节点名称，仅提取以 Net- 开头的节点，排除元件和其他非节点名称。
    """
    netlist_nodes = set()  # 使用集合去重

    with open(cir_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 提取以 "Net-" 开头的节点名称
            matches = re.findall(r'\bNet-[\w\-_]+\b', line)  # 匹配以 "Net-" 开头的节点
            
            # 排除电压值和电流值等非节点项
            for match in matches:
                # 如果包含数字或是某些特殊字符，排除掉
                if re.match(r'^[\w\-_]+$', match):
                    netlist_nodes.add(match)
            
            # 你可以添加更多规则来排除元件等非节点名称
            # 例如排除以数字或其他不合理的节点（如电流、电压等）
    
    return list(netlist_nodes)  # 返回去重后的节点列表


# 示例：获取节点电压数据并计算节点覆盖率
def calculate_extract_netlist_nodes_main(raw_file, cir_file):
    # raw_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\simresult\\111.raw'  # 替换为你自己的路径
    # cir_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\Netlist\\5.cir' # CIR 网表文件路径

    # 提取仿真数据
    node_data = extract_spice_data(raw_file)

    # 假设网表中有 100 个节点
    total_nodes = extract_netlist_nodes(cir_file)
    # print(f"提取的节点名称: {total_nodes}")
    # print(f"总节点数: {len(total_nodes)}")

    # 计算节点覆盖率
    node_coverage = ((len(node_data) -1) / (len(total_nodes)*2)) * 100  # 修改为总节点数的长度
    # print(f"节点覆盖率: {node_coverage}%")
    return node_coverage

# if __name__ == "__main__":
#     main()
