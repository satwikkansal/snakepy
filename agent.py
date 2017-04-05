import random
import numpy
import operator

class Agent(object):
    """Base class for all agents."""

    def __init__(self,env):

        self.env = env
        self.q_table = {}
        self.reward = 0
        self.alpha = 0.3
        self.gamma = 0.1
        self.epsilon = 0.1
        self.penalties = []
        self.total_reward = 0.0
        self.counts = 0.0

    def reset(self, destination=None):
        self.reward = 0

    def get_action(self):
        max_q = 0
        
        self.state = self.env.get_state()

        if not self.state in self.q_table:
            self.q_table[self.state] = {ac:0 for ac in self.env.valid_actions}

        action = random.choice(self.env.valid_actions)
        random_action = action

        # Exploration v/s exploitation
        if numpy.random.random()>self.epsilon:
            if len(set(self.q_table[self.state].values())) == 1:
                pass
            else:
                action = max(self.q_table[self.state].iteritems(), key=operator.itemgetter(1))[0]
        return action


    def update(self, action, reward):

        self.total_reward += reward

        self.next_state = self.env.get_state()

        #check if next_state has q_values already
        if self.next_state not in self.q_table:
            self.q_table[self.next_state] = {ac:0 for ac in self.env.valid_actions}

        # Learn policy based on state, action, reward
        old_q_value = self.q_table[self.state][action]

        #maximum q_value for next_state actions
        next_max = max(self.q_table[self.next_state].values())

        # calculate the q_value for the next_max action.
        new_q_value = (1 - self.alpha)*old_q_value + self.alpha*(reward + self.gamma*next_max)
        self.q_table[self.state][action] = new_q_value
        if random.randrange(0,5000) == 5:
            print "LearningAgent.update(): state = {}, action = {}, reward = {}".format(self.state, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=Fa
    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    penalties_count_after_training = a.penalties.count(1)
    print penalties_count_after_training
    #running 10 trials without exploration to see whether we've learned enough or not.
    a.epsilon = 0.0
    sim.run(n_trials=100)
    penalties_count_after_testing = a.penalties.count(1) - penalties_count_after_training
    print penalties_count_after_testing


def comprehensive_test():

    alphas = [0.3,0.5,0.7,0.9]
    gammas = [0.1,0.3,0.5,0.7]
    epsilons = [0.01, 0.1, 0.2]
    results = {}
    best_choice_alpha = []
    best_choice_gamma = []
    best_choice_epsilon = []
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials
    for n in range(10):
        for alpha in alphas:
            for gamma in gammas:
                for epsilon in epsilons:
                	penalties_count_before_trials = a.penalties.count(1)
                   	a.alpha = alpha
                   	a.gamma = gamma
                   	a.epsilon = epsilon
                   	sim = Simulator(e, update_delay=0.0001, display=False)
                   	sim.run(n_trials=100)
                   	penalties_count_after_trials = a.penalties.count(1) - penalties_count_before_trials
                   	results[(alpha,gamma,epsilon)] = {'ratio' : a.total_reward/a.counts,
                   									   'penalties' : penalties_count_after_trials
                   									   }
        x,y,z =  max(results.iteritems(), key=operator.itemgetter(1))[0]
        best_choice_alpha.append(x)
        best_choice_gamma.append(y)
        best_choice_epsilon.append(z)
    sorted_reults = sorted(results.items(), key=lambda x: x[1]['penalties'], reverse=True)
    print sorted_reults
    best_choice = (max(set(best_choice_alpha), key=best_choice_alpha.count), max(set(best_choice_gamma), key=best_choice_gamma.count), max(set(best_choice_epsilon), key=best_choice_epsilon.count))
    print "This the best choice", best_choice
    #comes out to be (0.3,0.1,0.1)

if __name__ == '__main__':
   run()
 