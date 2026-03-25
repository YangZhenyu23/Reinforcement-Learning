import sys, random, grader, parse

# download the test cases from the test_cases folder with the help of the grader.py file
def play_episode(problem):
    seed = problem['seed']      # seed for the random number generator
    noise = problem['noise']    # noise for the random number generator
    living_reward = problem['livingReward'] # living reward for the grid
    grid = problem['grid']
    policy = problem['policy'] # policy for the grid

    # if the seed is not -1, then set the seed for the random number generator
    if seed != -1:
        random.seed(seed, version=1)

    # get the number of rows and columns in the grid
    rows = len(grid) # number of rows in the grid
    cols = len(grid[0]) # number of columns in the grid

    # get the starting position of the player
    start_r, start_c = 0, 0
    for r in range(rows):
        for c in range(cols): # iterate through the grid
            if grid[r][c] == 'S': # if the current position is the starting position
                start_r, start_c = r, c # set the starting position

    # create a map of the noise for the random number generator
    noise_map = {
        'N': ['N', 'E', 'W'], # north       
        'E': ['E', 'S', 'N'], # east
        'S': ['S', 'W', 'E'], # south
        'W': ['W', 'N', 'S'] # west
    }
    deltas = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)} # deltas for the random number generator

    def render(pr, pc, show_p=True):
        # render the grid
        lines = []
        for r in range(rows): # iterate through the grid
            row = '' # initialize the row
            for c in range(cols): # iterate through the columns
                if show_p and r == pr and c == pc: # if the current position is the player
                    row += '{:>5}'.format('P') # add the player to the row
                else:
                    row += '{:>5}'.format(grid[r][c]) # add the current position to the row
            lines.append(row) # add the row to the list of lines
        return '\n'.join(lines) # join the lines with a new line

    # initialize the current position of the player
    cr, cc = start_r, start_c # current row and column
    cum = 0.0 # cumulative reward sum
    sep = '-------------------------------------------- \n' # separator for the output

    # output the start state
    out = 'Start state:\n'
    out += render(cr, cc) + '\n'
    out += 'Cumulative reward sum: ' + str(round(cum, 2)) + '\n'

    # play the episode
    while True:
        intended = policy[cr][cc] # intended action
        if intended == 'exit':
            reward = float(grid[cr][cc]) # reward for the current state if the player exits the grid
            cum += reward # add the reward to the cumulative reward sum
            out += sep
            out += 'Taking action: exit (intended: exit)\n' # output the action
            out += 'Reward received: ' + str(reward) + '\n' # output the reward    
            out += 'New state:\n' # output the new state
            out += render(cr, cc, False) + '\n'
            out += 'Cumulative reward sum: ' + str(round(cum, 2)) # output the cumulative reward sum
            break
        else: # if the player does not exit the grid
            actual = random.choices(
                population=noise_map[intended], # population for the random number generator
                weights=[1 - noise * 2, noise, noise] # weights for the random number generator
            )[0]
            dr, dc = deltas[actual] # delta row and column
            nr, nc = cr + dr, cc + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nc] == '#': # if the new position is out of bounds or a wall
                nr, nc = cr, cc # set the new position to the current position
            cr, cc = nr, nc
            cum += living_reward # add the living reward to the cumulative reward sum               
            out += sep
            out += 'Taking action: ' + actual + ' (intended: ' + intended + ')\n' # output the action
            out += 'Reward received: ' + str(living_reward) + '\n' # output the reward
            out += 'New state:\n' # output the new state
            out += render(cr, cc) + '\n'
            out += 'Cumulative reward sum: ' + str(round(cum, 2)) + '\n' # output the cumulative reward sum

    return out # return the output  

if __name__ == "__main__":
    # get the test case id from the command line
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)