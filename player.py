class Player:
    def __init__(self, name, model, arms, rounds, alpha=0) -> None:
        self.rewards = []
        self.arms = arms
        self.Model = model(arms, rounds, name, alpha)  # model
        self.score = 0
        self.name = name
        self.for_every = 1
        pass

    def play(self):
        choice = self.Model.choice()
        # if self.Model.round % self.for_every == 0:
        #   print(f'{self.name} Chose Arm ({choice})')
        return choice  # model

    def update_score(self, reward):
        self.score += reward
        self.Model.update_reward(reward)  # model
