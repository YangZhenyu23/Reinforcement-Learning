# Problem 4: Q-Value TD Learning
#
# Applied to: test case 2 of problem 3 (4x3 grid world)
# Parameters: discount=1, noise=0.1, livingReward=-0.01
#
# Optimal policy (from value iteration, same as slide 15 of chapter 2):
#   E  E  E  exit
#   N  #  W  exit
#   N  W  W  S
#
# Implementation details:
#   - Q values initialized to 0 for all state-action pairs
#   - Epsilon-greedy exploration: epsilon = max(1/(1+episode*0.005), 0.01)
#     decays slowly from 1.0 to 0.01 over ~20000 episodes, ensuring
#     sufficient exploration of all state-action pairs
#   - Learning rate: alpha = 100/(100+N(s,a)), where N(s,a) is the visit
#     count. This keeps alpha relatively high (~0.5 at 100 visits, ~0.09 at
#     1000 visits), allowing Q-values to adapt to improved estimates as the
#     agent learns better policies over time
#   - Episodes start from a uniformly random non-terminal state (exploring
#     starts) to ensure all states are visited sufficiently
#   - Convergence criterion: derived policy remains stable for 8000
#     consecutive episodes (checked every 200 episodes), without comparing
#     to the known optimal policy
#
# Findings:
#   Over multiple experiments of 10 runs each, the optimal policy is found
#   10/10 times consistently. Convergence typically takes 15000-25000
#   episodes. The key to reliable convergence is keeping the learning rate
#   high enough for long enough (alpha = 100/(100+N)) so that Q-values at
#   bottom-row states - where the gap between optimal and suboptimal actions
#   is small (~0.02) - can be refined accurately. A faster-decaying learning
#   rate (e.g., 1/N^0.6) sometimes locks in inaccurate early estimates and
#   achieves only ~8/10 success rate. The slower epsilon decay also helps by
#   maintaining exploration while Q-values for distant states are still being
#   refined.
#
# How to run: python p4.py

import random

# MDP Definition (test case 2 of problem 3)
discount = 1.0
noise = 0.1
living_reward = -0.01

grid = [
    ['_', '_', '_', '1'],
    ['_', '#', '_', '-1'],
    ['S', '_', '_', '_']
]
rows, cols = 3, 4

# Optimal policy from value iteration (pi_k=19 of P3 test case 2)
optimal_policy = {
    (0,0): 'E', (0,1): 'E', (0,2): 'E', (0,3): 'exit',
    (1,0): 'N',                            (1,2): 'W', (1,3): 'exit',
    (2,0): 'N', (2,1): 'W', (2,2): 'W', (2,3): 'S'
}

noise_map = {
    'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'],
    'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']
}
deltas = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
all_actions = ['N', 'E', 'S', 'W']


def is_terminal(r, c):
    return grid[r][c] not in ('_', '#', 'S')

def is_wall(r, c):
    return grid[r][c] == '#'

def get_next(r, c, d):
    dr, dc = deltas[d]
    nr, nc = r + dr, c + dc
    if nr < 0 or nr >= rows or nc < 0 or nc >= cols or is_wall(nr, nc):
        return r, c
    return nr, nc

def take_action(r, c, intended):
    dirs = noise_map[intended]
    actual = random.choices(dirs, weights=[1 - 2 * noise, noise, noise])[0]
    return get_next(r, c, actual)


all_states = [(r, c) for r in range(rows) for c in range(cols) if not is_wall(r, c)]
non_terminal_states = [(r, c) for r, c in all_states if not is_terminal(r, c)]


def derive_policy(Q):
    policy = {}
    for s in all_states:
        if is_terminal(*s):
            policy[s] = 'exit'
        else:
            bv = max(Q[s][a] for a in all_actions)
            policy[s] = next(a for a in all_actions if Q[s][a] >= bv - 1e-10)
    return policy


def format_policy(policy):
    lines = []
    for r in range(rows):
        row = ''
        for c in range(cols):
            if is_wall(r, c):
                row += '  #  '
            else:
                a = policy.get((r, c), '?')
                row += ' exit' if a == 'exit' else '  ' + a + '  '
        lines.append(row)
    return '\n'.join(lines)


def q_learning(max_episodes=80000, check_interval=200, stability_threshold=8000):
    Q = {}
    visit = {}
    for s in all_states:
        if is_terminal(*s):
            Q[s] = {'exit': 0.0}
            visit[s] = {'exit': 0}
        else:
            Q[s] = {a: 0.0 for a in all_actions}
            visit[s] = {a: 0 for a in all_actions}

    prev_policy = None
    stable_episodes = 0

    for ep in range(1, max_episodes + 1):
        epsilon = max(1.0 / (1 + ep * 0.005), 0.01)

        r, c = random.choice(non_terminal_states)

        for _ in range(300):
            if is_terminal(r, c):
                tv = float(grid[r][c])
                visit[(r, c)]['exit'] += 1
                alpha = 100.0 / (100 + visit[(r, c)]['exit'])
                Q[(r, c)]['exit'] += alpha * (tv - Q[(r, c)]['exit'])
                break

            if random.random() < epsilon:
                action = random.choice(all_actions)
            else:
                bv = max(Q[(r, c)][a] for a in all_actions)
                action = next(a for a in all_actions if Q[(r, c)][a] >= bv - 1e-10)

            nr, nc = take_action(r, c, action)

            if is_terminal(nr, nc):
                max_q_next = Q[(nr, nc)]['exit']
            else:
                max_q_next = max(Q[(nr, nc)][a] for a in all_actions)

            visit[(r, c)][action] += 1
            alpha = 100.0 / (100 + visit[(r, c)][action])
            sample = living_reward + discount * max_q_next
            Q[(r, c)][action] += alpha * (sample - Q[(r, c)][action])

            r, c = nr, nc

        if ep % check_interval == 0:
            policy = derive_policy(Q)
            if prev_policy is not None and all(policy[s] == prev_policy[s] for s in all_states):
                stable_episodes += check_interval
            else:
                stable_episodes = 0
            prev_policy = policy

            if stable_episodes >= stability_threshold:
                return Q, policy, ep

    return Q, derive_policy(Q), max_episodes


if __name__ == '__main__':
    num_runs = 10
    successes = 0
    episodes_list = []

    print("Q-Value TD Learning on 4x3 Grid World")
    print("discount={}, noise={}, livingReward={}".format(discount, noise, living_reward))
    print("=" * 50)

    for run in range(1, num_runs + 1):
        Q, policy, episodes = q_learning()
        episodes_list.append(episodes)
        match = all(policy[s] == optimal_policy[s] for s in optimal_policy)
        if match:
            successes += 1
        print("Run {}: {} episodes, matches optimal: {}".format(run, episodes, match))
        print(format_policy(policy))
        print()

    print("=" * 50)
    print("Optimal policy found: {}/{}".format(successes, num_runs))
    print("Average convergence episodes: {:.0f}".format(sum(episodes_list) / len(episodes_list)))
