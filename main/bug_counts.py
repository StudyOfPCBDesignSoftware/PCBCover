#txt文件路径为C:\Users\dell\Desktop\zhaoxu\CIR\PCBSmith10GenV43.txt，读取这个·txt文件，统计有多少failed字样

# bug_file = 'C:\\Users\\dell\\Desktop\\zhaoxu\\CIR\\PCBSmith10GenV43.txt'
def bug_counts_main(bug_file):
    with open(bug_file, 'r') as f:
        lines = f.readlines()
        failed_count = 0

        for line in lines:
            if 'failed' in line:
                failed_count += 1

        # print(f"Failed count: {failed_count}")
    
    return failed_count
