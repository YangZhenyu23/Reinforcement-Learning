import sys, parse, grader
import heapq

def astar_search(problem):
    frontier = []
    heapq.heappush(frontier, (problem.h[problem.start_state], 0, problem.start_state, [problem.start_state]))
    best_g = {problem.start_state: 0.0}
    explored = set()
    explored_order = []
    order = 1
    while frontier:
        f, _, node, path = heapq.heappop(frontier)
        g = f - problem.h[node]
        if g != best_g.get(node): continue
        if node in problem.goal_states: return ' '.join(explored_order) + '\n' + ' '.join(path)
        if node not in explored:
            explored.add(node)
            explored_order.append(node)
            for child in problem.graph[node]:
                if child in explored: continue
                child_g = g + problem.edge_costs[(node, child)]
                if child not in best_g or child_g < best_g[child]:
                    best_g[child] = child_g
                    heapq.heappush(frontier, (child_g + problem.h[child], order, child, path + [child]))
                    order += 1
    solution = ' '.join(explored_order) + '\n'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)