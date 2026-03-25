import os, sys
def read_graph_search_problem(file_path):
    class Problem:
        pass

    problem = Problem()

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    
    problem.start_state = lines[0].split(':', 1)[1].strip()
    problem.goal_states = lines[1].split(':', 1)[1].strip().split()
    problem.goal_state = problem.goal_states[0] if problem.goal_states else ''

    
    problem.graph = {}
    problem.heuristics = {}
    problem.edge_costs = {}

    for line in lines[2:]:
        parts = line.split()
        if len(parts) == 2:
            node, h = parts
            problem.heuristics[node] = float(h)
            problem.graph.setdefault(node, [])
        elif len(parts) == 3:
            src, dst, cost = parts
            problem.graph.setdefault(src, []).append(dst)
            problem.graph.setdefault(dst, [])
            problem.edge_costs[(src, dst)] = float(cost)

    
    problem.h = problem.heuristics
    return problem

def read_8queens_search_problem(file_path):
    class Problem:
        pass

    problem = Problem()

    with open(file_path, 'r', encoding='utf-8') as f:
        board = [line.strip().split() for line in f if line.strip()]

    problem.board = board
    problem.n = len(board)

    # queen_rows[col] = row index of queen in that column, or -1.
    queen_rows = [-1] * problem.n
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell.lower() == 'q':
                queen_rows[c] = r

    problem.queen_rows = queen_rows
    problem.queens = [(r, c) for c, r in enumerate(queen_rows) if r != -1]
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')