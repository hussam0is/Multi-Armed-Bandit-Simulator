import random
import numpy as np


class Model:
    def __init__(self):
        self.ExploreExploit = ExploreExploit
        self.ExploreExploit2 = ExploreExploit2
        self.ExploreExploit3 = ExploreExploit3
        self.RandomChoices = RandomChoices


class ExploreExploit:
    rewards_nd_counts: dict

    def __init__(self, arms, rounds, player_name, alpha=0) -> None:
        self.arms = arms
        self.K = len(arms)
        self.T = rounds
        self.rewards_nd_counts = {arm: {'counts': 0, 'rewards': []} for arm in self.arms}
        self.round = 0
        self.alpha = alpha
        self.played = []
        self.not_played = arms.copy()
        self.playing_arms = arms.copy()
        self.player_name = player_name
        self.last_choice = None

    def update_reward(self, reward):
        self.rewards_nd_counts[self.last_choice]['counts'] += 1
        self.rewards_nd_counts[self.last_choice]['rewards'].append(reward)

    def USB(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        rewards = self.rewards_nd_counts[arm]['rewards']
        sum_rewards = sum(rewards)
        v = sum_rewards / m
        lmbda = lambda m: np.math.sqrt(8 * np.math.log(self.T) / m)
        usb = v + lmbda(m)
        return usb

    def LSB(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        rewards = self.rewards_nd_counts[arm]['rewards']
        sum_rewards = sum(rewards)
        v = sum_rewards / m
        lmbda = lambda m: np.math.sqrt(8 * np.math.log(self.T) / m)
        lsb = v - lmbda(m)
        return lsb

    def choice(self):
        self.round += 1  # choice returned in round == round
        # eliminate arms
        if len(self.not_played) == 0 and self.round - 1 > self.alpha * len(
                self.arms):  # how many times model observe all arms before elemination
            self.played = []
            for arm_i in self.playing_arms.copy():
                for arm_j in self.playing_arms.copy():
                    if arm_i == arm_j:
                        continue
                    if self.USB(arm_j) < self.LSB(arm_i):
                        self.playing_arms.remove(arm_j)
                        # print(f'{self.player_name}: [arm {arm_j} removed!]')
            self.not_played = self.playing_arms.copy()

        # pick arbitrary hand from each arm in  self.not_played
        if len(self.not_played) == 0:
            self.not_played = self.playing_arms.copy()
            self.played = []
        sample_random_arm = random.choice(self.not_played)
        choice = self.not_played[self.not_played.index(sample_random_arm)]
        self.not_played.remove(choice)
        self.played.append(choice)
        self.last_choice = choice
        return choice


class RandomChoices:  # arbitrary
    def __init__(self, arms, rounds, player_name, alpha=0) -> None:
        self.arms = arms
        self.K = len(arms)
        self.T = rounds
        self.time_choice_reward = dict()  # {round: (choice, reward)}
        self.round = 0
        self.alpha = alpha
        self.last_choice = None

    def choice(self):
        self.round += 1
        choice = np.random.randint(1, self.K + 1)
        self.last_choice = choice
        return choice

    def update_reward(self, reward):
        self.time_choice_reward[round] = (self.last_choice, reward)


class ExploreExploit2(ExploreExploit):
    def __init__(self, arms, rounds, player_name, alpha=0):
        super().__init__(arms, rounds, player_name, alpha)

    def USB(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        rewards = self.rewards_nd_counts[arm]['rewards']
        sum_rewards = sum(self.rewards_nd_counts[arm]['rewards'])
        estimated_mean = sum_rewards / m
        estimated_var = (1 / (m - 1)) * sum([(reward - estimated_mean) ** 2 for reward in rewards])
        estimated_sd = np.math.sqrt(estimated_var)
        # v = sum([1 if (reward - estimated_mean)/estimated_sd>0 else 0 for reward in rewards])/m
        lmbda = lambda m: np.math.sqrt(8 * np.math.log(self.T) / m)
        v = estimated_mean
        usb = v / estimated_sd + lmbda(m)
        return usb

    def LSB(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        rewards = self.rewards_nd_counts[arm]['rewards']
        sum_rewards = sum(self.rewards_nd_counts[arm]['rewards'])
        estimated_mean = sum_rewards / m
        estimated_var = (1 / (m - 1)) * sum([(reward - estimated_mean) ** 2 for reward in rewards])
        estimated_sd = np.math.sqrt(estimated_var)
        # v = sum([1 if (reward - estimated_mean)/estimated_sd>0 else 0 for reward in rewards])/m
        lmbda = lambda m: np.math.sqrt(8 * np.math.log(self.T) / m)
        v = estimated_mean
        lsb = v / estimated_sd - lmbda(m)
        return lsb


class ExploreExploit3(ExploreExploit):
    def __init__(self, arms, rounds, player_name, alpha=0):
        super().__init__(arms, rounds, player_name, alpha)

    def USB(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        rewards = self.rewards_nd_counts[arm]['rewards']
        sum_rewards = sum(self.rewards_nd_counts[arm]['rewards'])
        estimated_mean = sum_rewards / m
        estimated_var = (1 / (m - 1)) * sum([(reward - estimated_mean) ** 2 for reward in rewards])
        estimated_sd = np.math.sqrt(estimated_var)
        lmbda = lambda m: np.math.sqrt(8 * np.math.log(self.T) / m)
        v = estimated_mean
        usb = v*np.math.sqrt(m) + lmbda(m)
        return usb

    def LSB(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        rewards = self.rewards_nd_counts[arm]['rewards']
        sum_rewards = sum(self.rewards_nd_counts[arm]['rewards'])
        estimated_mean = sum_rewards / m
        estimated_var = (1 / (m - 1)) * sum([(reward - estimated_mean) ** 2 for reward in rewards])
        estimated_sd = np.math.sqrt(estimated_var)
        lmbda = lambda m: np.math.sqrt(8 * np.math.log(self.T) / m)
        v = estimated_mean
        lsb = v*np.math.sqrt(m) - lmbda(m)
        return lsb
