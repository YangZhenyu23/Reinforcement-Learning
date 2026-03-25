def read_grid_mdp_problem_p1(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    problem = {}
    grid_split = content.split('grid:')
    header = grid_split[0]
    rest = grid_split[1]
    policy_split = rest.split('policy:')
    grid_text = policy_split[0]
    policy_text = policy_split[1]
    for line in header.strip().split('\n'):
        line = line.strip()
        if line.startswith('seed:'):
            problem['seed'] = int(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
    grid = []
    for line in grid_text.strip().split('\n'):
        if line.strip():
            grid.append(line.strip().split())
    problem['grid'] = grid
    policy = []
    for line in policy_text.strip().split('\n'):
        if line.strip():
            policy.append(line.strip().split())
    problem['policy'] = policy
    return problem

def read_grid_mdp_problem_p2(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    problem = {}
    grid_split = content.split('grid:')
    header = grid_split[0]
    rest = grid_split[1]
    policy_split = rest.split('policy:')
    grid_text = policy_split[0]
    policy_text = policy_split[1]
    for line in header.strip().split('\n'):
        line = line.strip()
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1].strip())
    grid = []
    for line in grid_text.strip().split('\n'):
        if line.strip():
            grid.append(line.strip().split())
    problem['grid'] = grid
    policy = []
    for line in policy_text.strip().split('\n'):
        if line.strip():
            policy.append(line.strip().split())
    problem['policy'] = policy
    return problem

def read_grid_mdp_problem_p3(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    problem = {}
    grid_split = content.split('grid:')
    header = grid_split[0]
    grid_text = grid_split[1]
    for line in header.strip().split('\n'):
        line = line.strip()
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1].strip())
    grid = []
    for line in grid_text.strip().split('\n'):
        if line.strip():
            grid.append(line.strip().split())
    problem['grid'] = grid
    return problem