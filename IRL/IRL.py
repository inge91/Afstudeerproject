##################################################################
# Prototype for Maximum Entropy Inverse Reinforcement Learning   #
#                                                                #
# Inge Becht 6093906                                             #
#                                                                #
##################################################################
import math
import numpy as np
# width and height of the map
width = 3
height = 3

# Pretty ASCII art to demonstrate the map
# -------
# |e    |
# |  x  |
# |    b|
# -------

# states of interest for feature calculation 
beginstate = (0,2)
endstate = (2,0)
centrestate = (1,1)

feature_count = 3

# initialise weights all with the same value
weights = np.array([len(feature_count) * 1])

# A trajectory from begin state to end state
trajectory = [(0,2), (0,1), (0,0), (1,0), (2,0)]
trajectories = [trajectory]

# Lists of all actions and all states
states = [(0,0), (0,1), (0,2), (1, 0), (1, 2), (2,0), (2,1), (2,2)]

# Possible actions
Actions = enum(UP = 1, DOWN = 2,  LEFT = 3, RIGHT = 4, STILL = 5)
barricades = [(1,1)]

# Enum possibility
def enum(**enums):
    return type('Enum', (), enums)

# evaluate if state is empty
def empty(state):
    True if state not in barricades else False

# Evaluates if a given move is valid in a given state
def action_possible(state, action):
    return {
        LEFT: (state + (-1, 0))[0] > 0 and empty(state + (-1,0)),
        RIGHT: (state + (1, 0))[0] < width and empty(state + (1,0)),
        UP: (state + (0, 1)[1] < height and empty(state + (0, 1))),
        DOWN: (state + (0, -1)[1] > 0 and empty(state + (1,0))),
    }[action]

# Return list that has all actions opposite of input list
def get_opposite_actions(actions):
    opposite_actions = []
    for action in actions:
        temp = getopposite_action(action)
        if(temp is not STILL):
            opposite_actions.append(temp)
    return opposite_actions

# Return opposite of an action
def get_opposite_action(action):
    return {
            LEFT: RIGHT,
            RIGHT: LEFT,
            UP: DOWN,
            DOWN: UP,
            STILL: STILL
            }[action]

# get all possible actions in a state
def get_actions(state):
    actions = [STILL]
    if action_possible(state, LEFT):
        actions += LEFT
    if action_possible(state, RIGHT):
        actions += RIGHT
    if action_possible(state, UP):
        actions += UP
    if action_possible(state, DOWN):
        actions += DOWN
    return actions

def apply_action(state, action):
    return {
        LEFT: state + (-1, 0)
        RIGHT:state + (1, 0)
        UP:   state + (0, 1)
        DOWN: state + (0, -1)
        STILL: state +(0, 0)
    }[action]

# returns terminal states of all trajectories
def terminal_states():
    return list(set([x[-1] for x in trajectories]))

def main():
    # construct features for all of the trajectories
    apply_meirl()

# Calculates all features for a position
def calculate_features(state):
    feature_values = np.array([])
    np.append(feature_values, calculate_exit_distance(state)])
    np.append(feature_values, calculate_entrance_distance(state))
    np.append(feature_values, calculate_centre_distance(state))

############# Collection of 3 Features ####################
# Calculate how many steps it takes to the end position
def calculate_exit_distance(state):
    return abs(state - endstate)[0] + abs(state - endstate)[1]

# Calculate how many steps it takes to the begin position
def calculate_entrance_distance(state):
    return abs(state - beginstate)[0] + abs(state - beginstate)[1]

# Calculate how many steps it takes to 
def calculate_centre_distance(state):
    return abs(state - centrestate)[0] + abs(state - centrestate)[1]
#############################################################

# Apply backward pass N times
def backward_pass(terminal_state, N):
    Z_action(terminal_state, 500)

# Recursion of state
def Z_state(state, N):
    # get all actions from which you can possibly end up in state
    actions = get_opposite_actions(get_actions(state))
    
    # Caclulte Z_action for all these states
    for action in actions:
       (Z_action(action, state) + 1) if (state in terminal_states()) else
        Z_action(action, state)

# Recursion of actions
def Z_action(action, state, N):
    action_reverse =  get_opposite_action(action)
    prev_state = apply_action(state, action_reverse)
    return math.pow(math.e, reward_functions(state)) * Z_state(new_state, N-1)

# Returns the reward given a state
def reward_function(state):
    features = extract_features(state)
    reward = np.dot(weights, features)
    return reward

# Step 3 of the Expected Edge Frequency Calculation
def local_action_prob_comp(state, action):
    return Z_action(action, state, 500) / Z_state(action, state, 500) 

# Updates reward for non-deterministic MDPs
# TODO: Do i still need to derive?
def update_weights():
    # The gradient descent
    visitation_count = calculate_visitation_count()
    esfv = calculate_expected_state_freq_vis()
    global weights = visitation_count - esfv

# The calculation of E[fo]
# For all features in every square visited in every trajectory
# add their feature values and return as visitation count
def calculate_visitation_count():
    visitation_counts = np.array( feature_count * [0] )
    for trajectory in trajectories:
        for state in trajectory:
            visitation_counts += calculate_features(state)
    return visitation_counts

# The calculation of Sum_si D_si f_si
def calculate_expected_state_freq_vis():
    state_freq = 0
    for state in states:
        state_freq += summing_frequencies(state) * calculate_features(state)
    return state_freq

# Make forward pass N times FIXME: Iterate form t = 1 to N
def forward_pass(state_n, time, N):
    # Probability of state being initial TODO: How to calculate?
    for state in states:
        for action in actions:
            D += D * 
            local_action_prob_comp(state, action) *
            # is 0 or 1

# For a state do the forward_pass with each possible time
def summing_frequencies(state):
    Ds = []
    finaltime = 200
    for time in range (1, finaltime):
        Ds.append(forward_pass(state, Ds[-1], time))
    return Ds

# The probability that given a state and an action
# the new state will be reached
def transition_probability(state_n, state, action):
    # possible FIXME: Should it only be state transitions that really occur?
    1 if (state + action) == state_n else 0 

def apply_meirl():
    terminal_states = terminal_states()
    for terminal_state in terminal_states:
        backward_pass(terminal_state, 500)


if __name__ == '__main__':
    def main()
