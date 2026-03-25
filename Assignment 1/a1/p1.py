import sys, grader, parse
import collections
def dfs_search(problem):
    frontier = collections.deque([(problem.start_state, [problem.start_state])])
    explored = set()
    explored_order = []
    while frontier:
        node, path = frontier.pop()
        if node in problem.goal_states: return ' '.join(explored_order) + '\n' + ' '.join(path)
        if node not in explored:
            explored.add(node)
            explored_order.append(node)
            for child in problem.graph[node]:
                if child not in explored: frontier.append((child, path + [child]))
    solution = ' '.join(explored_order) + '\n'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)