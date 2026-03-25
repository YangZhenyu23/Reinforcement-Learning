import sys, grader, parse

def policy_evaluation(problem):
    discount = problem['discount']
    noise = problem['noise']
    living_reward = problem['livingReward']
    iterations = problem['iterations']
    grid = problem['grid']
    policy = problem['policy']

    rows = len(grid)
    cols = len(grid[0])

    noise_map = {
        'N': ['N', 'E', 'W'],
        'E': ['E', 'S', 'N'],
        'S': ['S', 'W', 'E'],
        'W': ['W', 'N', 'S']
    }
    deltas = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

    V = [[0.0] * cols for _ in range(rows)]

    def get_next(r, c, d):
        dr, dc = deltas[d]
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nc] == '#':
            return r, c
        return nr, nc

    def render(V):
        lines = []
        for r in range(rows):
            row = ''
            for c in range(cols):
                if grid[r][c] == '#':
                    row += '| ##### |'
                else:
                    row += '|{:>7.2f}|'.format(V[r][c])
            lines.append(row)
        return '\n'.join(lines)

    out = ''
    for k in range(iterations):
        out += 'V^pi_k=' + str(k) + '\n'
        out += render(V)
        if k < iterations - 1:
            out += '\n'
            new_V = [[0.0] * cols for _ in range(rows)]
            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] == '#':
                        continue
                    action = policy[r][c]
                    if action == 'exit':
                        new_V[r][c] = float(grid[r][c])
                    else:
                        dirs = noise_map[action]
                        probs = [1 - 2 * noise, noise, noise]
                        val = 0.0
                        for d, p in zip(dirs, probs):
                            nr, nc = get_next(r, c, d)
                            val += p * (living_reward + discount * V[nr][nc])
                        new_V[r][c] = val
            V = new_V

    return out

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)