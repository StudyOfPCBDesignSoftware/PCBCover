def config_update(config_file_path,new_paramer):
    with open(config_file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        for param in new_paramer:
            key, value = param.split('=')
            if key in line.strip():
                indent = line[:line.index(key)]
                lines[i] = '{}{} = {}\n'.format(indent, key, value)

    with open(config_file_path, 'w') as f:
        f.writelines(lines)

