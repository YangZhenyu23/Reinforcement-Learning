import sys, parse, grader
import heapq

def ucs_search(problem):
    frontier = []
    heapq.heappush(frontier, (0.0, 0, problem.start_state, [problem.start_state]))
    best_cost = {problem.start_state: 0.0}
    explored = set()
    explored_order = []
    order = 1
    while frontier:
        cost, _, node, path = heapq.heappop(frontier)
        if cost != best_cost.get(node): continue
        if node in problem.goal_states: return ' '.join(explored_order) + '\n' + ' '.join(path)
        if node not in explored:
            explored.add(node)
            explored_order.append(node)
            for child in problem.graph[node]:
                if child in explored: continue
                child_cost = cost + problem.edge_costs[(node, child)]
                if child not in best_cost or child_cost < best_cost[child]:
                    best_cost[child] = child_cost
                    heapq.heappush(frontier, (child_cost, order, child, path + [child]))
                    order += 1
    solution = ' '.join(explored_order) + '\n'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)