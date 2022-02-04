import random
import numpy as np


class Model:
    def __init__(self):
        self.ExploreExploit = ExploreExploit
        self.ExploreExploit2 = ExploreExploit2
        self.ExploreExploit3 = ExploreExploit3
        self.RandomChoices = RandomChoices


# Explore-Exploit using basic successor elimination algorithm
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

    def avg_rewards(self, arm):
        return sum(self.rewards_nd_counts[arm]['rewards'])/self.rewards_nd_counts[arm]['counts']

    def sd_estimate(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        rewards = self.rewards_nd_counts[arm]['rewards']
        estimated_mean = self.avg_rewards(arm)
        return np.math.sqrt((1 / (m - 1)) * sum([(reward - estimated_mean) ** 2 for reward in rewards]))

    def confidence_scale(self, m):
        return np.math.sqrt(8 * np.math.log(self.T) / m)

    def usb(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        v = self.avg_rewards(arm=arm)
        usb = v + self.confidence_scale(m)
        return usb

    def lsb(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        v = self.avg_rewards(arm=arm)
        lsb = v - self.confidence_scale(m)
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
                    if self.usb(arm_j) < self.lsb(arm_i):
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


# random model
class RandomChoices(ExploreExploit):  # arbitrary
    def __init__(self, arms, rounds, player_name, alpha=0) -> None:
        super().__init__(arms, rounds, player_name, alpha=0)

    def choice(self):
        self.round += 1
        choice = np.random.randint(1, self.K + 1)
        self.last_choice = choice
        return choice


# Explore-Exploit successive elimination with standard error == 1 of the mean estimation
class ExploreExploit2(ExploreExploit):
    def __init__(self, arms, rounds, player_name, alpha=0):
        super().__init__(arms, rounds, player_name, alpha)

    def usb(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        v = self.avg_rewards(arm=arm)
        sd = self.sd_estimate(arm=arm)
        usb = v/sd + self.confidence_scale(m)
        return usb

    def lsb(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        v = self.avg_rewards(arm=arm)
        sd = self.sd_estimate(arm=arm)
        lsb = v/sd - self.confidence_scale(m)
        return lsb


# Explore-Exploit successive elimination with refined mean for normal distributed rewards
class ExploreExploit3(ExploreExploit):
    def __init__(self, arms, rounds, player_name, alpha=0):
        super().__init__(arms, rounds, player_name, alpha)

    def usb(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        v = self.avg_rewards(arm=arm)
        usb = v*np.math.sqrt(m) + self.confidence_scale(m)
        return usb

    def lsb(self, arm):
        m = self.rewards_nd_counts[arm]['counts']
        v = self.avg_rewards(arm=arm)
        lsb = v*np.math.sqrt(m) - self.confidence_scale(m)
        return lsb
