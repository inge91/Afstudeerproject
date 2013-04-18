################################################################
# Prototyping for Inverse Reinforcement Learning               #
#                                                              #
# Inge Becht 6093906                                           #
#                                                              #
################################################################
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
beginstate = (0,21d)
endstate = (2,0)
centrestate = (1,1)

feature_count = 3

# initialise weights all with the same value
weights = np.array([len(feature_count) * 1])

# A trajectory from begin state to end state
trajectory = [(0,2), (0,1), (0,0), (1,0), (2,0)]
trajectories = [trajectory]

states = [(0,0), (0,1), (0,2), (1, 0), (1, 2), (2,0), (2,1), (2,2)]


def main():
    # construct features for all of the trajectories
    features = calculate_features(trajectories)

# Calculates all features for a position
def calculate_features(state):
    feature_values = np.array([])
    np.append(feature_values, calculate_exit_distance(state)])
    np.append(feature_values, calculate_entrance_distance(state))
    np.append(feature_values, calculate_centre_distance(state))


# Calculate how many steps it takes to the end position
def calculate_exit_distance(state):
    return abs(state - endstate)[0] + abs(state - endstate)[1]

# Calculate how many steps it takes to the begin position
def calculate_entrance_distance(state):
    return abs(state - beginstate)[0] + abs(state - beginstate)[1]

# Calculate how many steps it takes to 
def calculate_centre_distance(state):
    return abs(state - centrestate)[0] + abs(state - centrestate)[1]


# Apply backward pass N times
def backward_pass(N):
    for i in range(0, N):
        Zstate(state)

# Recursion of state
def Zstate(state):
    Sterminal = endstate
    # all actions possible in states
    for action in actions:
        (Zaction(action) + 1) if (state == Sterminal) else Zaction(action)

# Recursion of actions
def Zaction(action, state):
    for prev_state in states:
        probability_transition(action, prev_state, state) *  math.pow(math.e,
                reward_functions(state)) * Zstate(prev_state)

# Returns the reward given a state
def reward_function(state):
    features = extract_features(state)
    reward = np.dot(weights, features)
    return reward

# Updates reward for non-deterministic MDPs
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
    for state in states:
        forward_pass(state)
        calculate_features(state)

# Make forward pass N times FIXME: Iterate form t = 1 to N
def forward_pass(state_n, N):
    # Probability of state being initial TODO: How to calculate?
    D = 
    for i in range(0, N):
        for state in states:
            for action in actions:
                D += summing_frequencies(state) * 
                local_action_prob_comp(state, action) *
                # is 0 or 1
                transition_probability(state_n, state, action)

def summing_frequencies(state, time)

    


        






if __name__ == '__main__':
    def main()
