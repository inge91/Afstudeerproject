################################################################
# Prototyping for Inverse Reinforcement Learning               #
#                                                              #
# Inge Becht 6093906                                           #
#                                                              #
################################################################
import math
# width and height of the map
width = 3
height = 3

# points of interest for feature calculation 
beginpoint = (0,2)
endpoint = (2,0)
centrepoint = (1,1)

feature_count = 3

# Pretty ASCII art to demonstrate the map
# -------
# |e    |
# |  x  |
# |    b|
# -------

def main():
    # A trajectory from begin point to end point
    trajectory = [(0,2), (0,1), (0,0), (1,0), (2,0)]
    trajectories = [trajectory]

    # construct features for all of the trajectories
    features = calculate_features(trajectories)

    # initialise weights all with the same value
    weights = len(feature_count) * 1




# Calculates all features for every trajectory at every point
def calculate_features(trajectories):
    trajectories_features = []
    for trajectory in trajectories:
        trajectory_features = []
        for point in trajectory:
            feature_values = []
            feature_values += [calculate_exit_distance(point)]
            feature_values += [calculate_entrance_distance(point)]
            feature_values += [calculate_centre_distance(point)]
            trajectory_features += feature_values
        trajectories_features += trajectory_features
    return trajectories_features


# Calculate how many steps it takes to the end position
def calculate_exit_distance(point):
    return abs(point - endpoint)[0] + abs(point - endpoint)[1]

# Calculate how many steps it takes to the begin position
def calculate_entrance_distance(point):
    return abs(point - beginpoint)[0] + abs(point - beginpoint)[1]

# Calculate how many steps it takes to 
def calculate_centre_distance(point):
    return abs(point - centrepoint)[0] + abs(point - centrepoint)[1]


# Apply backward pass N times
def backward_pass(N):
    for i in range(0, N):
        Zstate(state)

# Recursion of state
def Zstate(state):
    Sterminal = endpoint
    # all actions possible in states
    for action in actions:
        Zaction(action) + 1 if (state == Sterminal) else Zaction(action)

# Recursion of actions
def Zaction(action, state):
    for prev_state in states:
        probability_transition(action, prev_state, state) *  math.pow(math.e,
                reward_functions(state)) * Zstate(prev_state)

# gives the reward given a state
def reward_function(state):
    features = extract_features(state)
    w * fs



if __name__ == '__main__':
    def main()
