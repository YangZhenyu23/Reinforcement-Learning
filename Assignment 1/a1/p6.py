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

def number_of_attacks(problem):
    n = problem.n
    queen_rows = problem.queen_rows
    rows = []
    for r in range(n):
        values = []
        for c in range(n):
            trial = queen_rows[:]
            trial[c] = r
            values.append(count_attacks(trial))
        rows.append(' '.join('{:2d}'.format(v) for v in values))
    solution = '\n'.join(rows)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)