import sys, parse, grader

def count_attacks(queen_rows):
    attacks = 0
    n = len(queen_rows)
    for c1 in range(n):
        r1 = queen_rows[c1]
        for c2 in range(c1 + 1, n):
            r2 = queen_rows[c2]
            if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                attacks += 1
    return attacks

def better_board(problem):
    n = problem.n
    queen_rows = problem.queen_rows[:]
    best_attacks = count_attacks(queen_rows)
    best_col, best_row = -1, -1
    for c in range(n):
        original_row = queen_rows[c]
        for r in range(n):
            if r == original_row: continue
            trial = queen_rows[:]
            trial[c] = r
            attacks = count_attacks(trial)
            if attacks < best_attacks:
                best_attacks = attacks
                best_col, best_row = c, r
    if best_col != -1:
        queen_rows[best_col] = best_row
    board = [['.' for _ in range(n)] for _ in range(n)]
    for c in range(n):
        r = queen_rows[c]
        if r != -1: board[r][c] = 'q'
    solution = '\n'.join(' '.join(row) for row in board)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)