class Player:
    def __init__(self, name, model, arms, rounds, alpha=0) -> None:
        self.rewards = []
        self.arms = arms
        self.Model = model(arms, rounds, name, alpha)
        self.name = name
        pass

    def play(self):
        choice = self.Model.choice()
        return choice

    def update_score(self, reward):
        self.Model.update_reward(reward)
