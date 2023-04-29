import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import math
from scipy.stats import poisson

matplotlib.use('Agg')


class BikeRental:

    def __init__(self):
        self.max_g_bike = 20
        self.max_move_of_g_bike = 5
        self.rental_request_first_loc = 3
        self.rental_request_second_loc = 4
        self.returns_first_loc = 3
        self.returns_second_loc = 2
        self.gamma = 0.9
        self.rental_credit = 10
        self.move_g_bike_cost = 2
        self.actions = np.arange(-self.max_move_of_g_bike, self.max_move_of_g_bike + 1)
        self.poisson_upper_bound = 11  # upper bound to poisson distribution
        self.value = np.zeros((self.max_g_bike + 1, self.max_g_bike + 1))
        self.policy = np.zeros(self.value.shape)
        self.p_backup = dict()
#defining function
    def poisson_dist(self, x, lam):
        if (x, lam) not in self.p_backup.keys():
            self.p_backup[(x, lam)] = poisson.pmf(x, lam)
        return self.p_backup[(x, lam)]

    def expected_return(self, state, action, state_value):
        returns = float(-(self.move_g_bike_cost * abs(action)))
        num_of_g_bike_first_loc = int(max(min(state[0] - action, self.max_g_bike), 0))
        num_of_g_bike_second_loc = int(max(min(state[1] + action, self.max_g_bike), 0))
        for rental_request_first_loc in range(self.poisson_upper_bound):
            for rental_request_second_loc in range(self.poisson_upper_bound):
                prob = self.poisson_dist(rental_request_first_loc, self.rental_request_first_loc) * self.poisson_dist(
                    rental_request_second_loc, self.rental_request_second_loc)
                valid_rental_first_loc = min(num_of_g_bike_first_loc, rental_request_first_loc)
                valid_rental_second_loc = min(num_of_g_bike_second_loc, rental_request_second_loc)
                reward = (valid_rental_first_loc + valid_rental_second_loc) * self.rental_credit
                g_bike_location_one = num_of_g_bike_first_loc - valid_rental_first_loc
                g_bike_location_two = num_of_g_bike_second_loc - valid_rental_second_loc
                returned_location_one = self.returns_first_loc
                returned_location_two = self.returns_second_loc
                g_bike_location_one = min(g_bike_location_one + returned_location_one, self.max_g_bike)
                g_bike_location_two = min(g_bike_location_two + returned_location_two, self.max_g_bike)
                returns += prob * (reward + self.gamma * state_value[g_bike_location_one, g_bike_location_two])
        return returns

    def policy_evaluation(self):
        while True:
            old_value = self.value.copy()
            for i in range(self.max_g_bike + 1):
                for j in range(self.max_g_bike + 1):
                    new_state_value = self.expected_return([i, j], self.policy[i, j], self.value)
                    self.value[i, j] = new_state_value
            max_value_change = abs(old_value - self.value).max()
            if max_value_change < 1e-4:
                break

    def policy_improvement(self):
        policy_not_improvable = True
        for i in range(self.max_g_bike + 1):
            for j in range(self.max_g_bike + 1):
                old_action = self.policy[i, j]
                action_returns = []
                for action in self.actions:
                    if (0 <= action <= i) or (-j <= action <= 0):
                        action_returns.append(self.expected_return([i, j], action, self.value))
                    else:
                        action_returns.append(-np.inf)
                new_action = self.actions[np.argmax(action_returns)]
                self.policy[i, j] = new_action
                if policy_not_improvable and old_action != new_action:
                    policy_not_improvable = False
        print(action_returns)
        if policy_not_improvable:
            print('Policy is stable and at optimal')
        else:
            print("Policy can be improved")

        return policy_not_improvable

def main():
    iterations = 0
    _, axes = plt.subplots(2, 3, figsize=(20, 12))
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    axes = axes.flatten()
    one = BikeRental()
    while True:
        fig = sb.heatmap(np.flipud(one.policy), cmap="viridis", ax=axes[iterations])
        fig.set_ylabel('Number of Bikes at First Location', fontsize=12)
        fig.set_yticks(list(reversed(range(one.max_g_bike + 1))))
        fig.set_xlabel('Number of Bikes at Second Location', fontsize=12)
        fig.set_title('Policy {}'.format(iterations), fontsize=12)
        one.policy_evaluation()
        policy_not_improvable = one.policy_improvement()
        if policy_not_improvable:
            fig = sb.heatmap(np.flipud(one.value), cmap="viridis", ax=axes[-1])
            fig.set_ylabel('Number of Bikes at First Location', fontsize=12)
            fig.set_yticks(list(reversed(range(one.max_g_bike + 1))))
            fig.set_xlabel('Number of Bikes at Second Location', fontsize=12)
            fig.set_title('Optimal Value', fontsize=15)
            break

        iterations += 1

    plt.savefig('gbike.png', dpi=300)
    plt.close()
    print("Done")




if __name__ == '__main__':
    main()

# Code reference Shah Jainil Kumar