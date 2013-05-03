##################################################################
# Prototype for Maximum Entropy Inverse Reinforcement Learning   #
#                                                                #
# Inge Becht 6093906                                             #
#                                                                #
##################################################################
import math
import numpy as np
from mutable_int import mutableInt
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
# TODO: How to make length variable
weights = np.array([1,1,1])

# A trajectory from begin state to end state
trajectory = [(0,2), (0,1), (0,0), (1,0), (2,0)]
trajectories = [trajectory]

# Lists of all actions and all states
states = [(0,0), (0,1), (0,2), (1, 0), (1, 2), (2,0), (2,1), (2,2)]

# Enum possibility
def enum(**enums):
    return type('Enum', (), enums)

# Possible actions
Actions = enum(UP = 1, DOWN = 2,  LEFT = 3, RIGHT = 4, STILL = 5)
barricades = [(1,1)]


# evaluate if state is empty
def empty(state):
    return True if state not in barricades else False

# Adds 2 tuples together
def add(x, y):
    return (x[0] + y[0], x[1] + y[1])

# Evaluates if a given move is valid in a given state
def action_possible(state, action):
    return {
        Actions.LEFT: (add(state, (-1, 0))[0] > 0) and empty(add(state, (-1,0))),
        Actions.RIGHT: (add(state, (1, 0))[0] < width) and empty(add(state,
            (1,0))),
        Actions.UP: (add(state, (0, 1))[1]) < height and empty(add(state, (0,
            1))),
        Actions.DOWN: (add(state, (0, -1))[1]) > 0 and empty(add(state, (1,0))),
    }[action]

# Return list that has all actions opposite of input list
def get_opposite_actions(actions):
    opposite_actions = []
    for action in actions:
        temp = get_opposite_action(action)
        if(temp is not Actions.STILL):
            opposite_actions.append(temp)
    return opposite_actions

# Return opposite of an action
def get_opposite_action(action):
    return {
            Actions.LEFT: Actions.RIGHT,
            Actions.RIGHT: Actions.LEFT,
            Actions.UP: Actions.DOWN,
            Actions.DOWN: Actions.UP,
            Actions.STILL: Actions.STILL
            }[action]

# get all possible actions in a state
def get_actions(state):
    actions = [Actions.STILL]
    if action_possible(state, Actions.LEFT):
        actions.append(Actions.LEFT)
    if action_possible(state, Actions.RIGHT):
        actions.append(Actions.RIGHT)
    if action_possible(state, Actions.UP):
        actions.append(Actions.UP)
    if action_possible(state, Actions.DOWN):
        actions.append(Actions.DOWN)
    return actions

def apply_action(state, action):
    return {
        Actions.LEFT:  (state[0] + -1, state[1] ),
        Actions.RIGHT: (state[0] + 1, state[1] ),
        Actions.UP:    (state[0], state[1] + 1),
        Actions.DOWN:  (state[0], state[1] -1),
        Actions.STILL: state
    }[action]

# returns terminal states of all trajectories
def terminal_states():
    return list(set([x[-1] for x in trajectories]))

def main():
    # construct features for all of the trajectories
    apply_meirl()

# Calculates all features for a position
def calculate_features(state):
    exit_dist = calculate_exit_distance(state)
    begin_dist = calculate_entrance_distance(state)
    centre_dist = calculate_centre_distance(state)
    return np.array([exit_dist, begin_dist, centre_dist])

############# Collection of 3 Features ####################
# Calculate how many steps it takes to the end position
def calculate_exit_distance(state):
    return abs(state[0] - endstate[0]) + abs(state[1] - endstate[1])

# Calculate how many steps it takes to the begin position
def calculate_entrance_distance(state):
    return abs(state[0] - beginstate[0]) + abs(state[1] - beginstate[1])

# Calculate how many steps it takes to 
def calculate_centre_distance(state):
    return abs(state[0] - centrestate[0]) + abs(state[1] - centrestate[1])
#############################################################

# Apply backward pass N times
def backward_pass(terminal_state, N):
    Zs = mutableInt(0)
    Za = mutableInt(0)
    Za = Z_state(terminal_state,Zs , Za, N)

# Recursion of state
def Z_state(state, Zs, Za, N):
    if N == 0:
        return Zs 
    # get all actions from which you can possibly end up in state
    actions = get_opposite_actions(get_actions(state))
    
    # Caclulte Z_action for all these states
    for action in actions:
        if (state in terminal_states()):
            Zs += (Z_action(action, Zs, Za, state, N) + 1)
        else:
            Z_action(action, Zs, Za, state, N)

# Recursion of actions
def Z_action(action, Zs, Za, state, N):
    print Zs
    if N == 0:
        return Za
    action_reverse =  get_opposite_action(action)
    prev_state = apply_action(state, action_reverse)
    #Za += math.pow(math.e, reward_function(state)) * Z_state(prev_state, Zs, Za, N-1)
    Za += Z_state(prev_state, Zs, Za, N-1)

# Returns the reward given a state
def reward_function(state):
    features = calculate_features(state)
    print features
    print weights
    reward = np.dot(weights, features)
    return reward

# Step 3 of the Expected Edge Frequency Calculation
def local_action_prob_comp(state, action):
    Zs = mutableInt(0)
    Za = mutableInt(0)
    return Z_action(action, Zs, Za, state, 2) / Z_state(state, Zs, Za,  2) 

# Updates reward for non-deterministic MDPs
# TODO: Do i still need to derive?
def update_weights():
    global weights 
    # The gradient descent
    visitation_count = calculate_visitation_count()
    esfv = calculate_expected_state_freq_vis()
    weights = visitation_count - esfv

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
#def forward_pass(state_n, time, N):
#    # Probability of state being initial TODO: How to calculate?
#    for state in states:
#        for action in actions:
#            D += D * 
#            local_action_prob_comp(state, action) *
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
    print local_action_prob_comp((0,0), Actions.LEFT)


if __name__ == '__main__':
    apply_meirl()
