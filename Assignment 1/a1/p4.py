import sys, parse, grader
import heapq

def greedy_search(problem):
    frontier = []
    heapq.heappush(frontier, (problem.h[problem.start_state], 0, problem.start_state, [problem.start_state]))
    best_h = {problem.start_state: problem.h[problem.start_state]}
    best_order = {problem.start_state: 0}
    explored = set()
    explored_order = []
    order = 1
    while frontier:
        h, current_order, node, path = heapq.heappop(frontier)
        if h != best_h.get(node) or current_order != best_order.get(node): continue
        if node in problem.goal_states: return ' '.join(explored_order) + '\n' + ' '.join(path)
        if node not in explored:
            explored.add(node)
            explored_order.append(node)
            for child in problem.graph[node]:
                if child in explored: continue
                child_h = problem.h[child]
                if child not in best_h or child_h <= best_h[child]:
                    best_h[child] = child_h
                    best_order[child] = order
                    heapq.heappush(frontier, (child_h, order, child, path + [child]))
                    order += 1
    solution = ' '.join(explored_order) + '\n'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)