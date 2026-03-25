import sys, grader, parse

def value_iteration(problem):
    discount = problem['discount']
    noise = problem['noise']
    living_reward = problem['livingReward']
    iterations = problem['iterations']
    grid = problem['grid']

    rows = len(grid)
    cols = len(grid[0])

    noise_map = {
        'N': ['N', 'E', 'W'],
        'E': ['E', 'S', 'N'],
        'S': ['S', 'W', 'E'],
        'W': ['W', 'N', 'S']
    }
    deltas = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    actions = ['N', 'E', 'S', 'W']

    V = [[0.0] * cols for _ in range(rows)]
    best_actions = [[None] * cols for _ in range(rows)]

    def get_next(r, c, d):
        dr, dc = deltas[d]
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nc] == '#':
            return r, c
        return nr, nc

    def q_value(r, c, action):
        dirs = noise_map[action]
        probs = [1 - 2 * noise, noise, noise]
        val = 0.0
        for d, p in zip(dirs, probs):
            nr, nc = get_next(r, c, d)
            val += p * (living_reward + discount * V[nr][nc])
        return val

    def render_values():
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

    def render_policy():
        lines = []
        for r in range(rows):
            row = ''
            for c in range(cols):
                if grid[r][c] == '#':
                    row += '| # |'
                elif best_actions[r][c] == 'exit':
                    row += '| x |'
                else:
                    row += '| ' + best_actions[r][c] + ' |'
            lines.append(row)
        return '\n'.join(lines)

    out = ''
    for k in range(iterations):
        out += 'V_k=' + str(k) + '\n'
        out += render_values()
        if k > 0:
            out += '\n'
            out += 'pi_k=' + str(k) + '\n'
            out += render_policy()
        if k < iterations - 1:
            out += '\n'
            new_V = [[0.0] * cols for _ in range(rows)]
            new_best = [[None] * cols for _ in range(rows)]
            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] == '#':
                        continue
                    cell = grid[r][c]
                    if cell not in ('_', 'S', '#'):
                        new_V[r][c] = float(cell)
                        new_best[r][c] = 'exit'
                    else:
                        best_val = float('-inf')
                        best_act = None
                        for a in actions:
                            val = q_value(r, c, a)
                            if val > best_val:
                                best_val = val
                                best_act = a
                        new_V[r][c] = best_val
                        new_best[r][c] = best_act
            V = new_V
            best_actions = new_best

    return out

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)