import numpy as np
import random


class Game:
    def __init__(self, exps=None, stds=None, window=0) -> None:
        if exps is None or stds is None:
            if exps is None:
                print(f'error: argument exps not found!')
            if stds is None:
                print(f'error: argument stds not found!')
                return
        self.exps = exps
        self.stds = stds
        self.window = window

    def play(self, choice):
        choice -= 1  # get arm index
        window_indices = []
        half_window = int(self.window / 2)
        mediate_index = choice
        if choice < half_window:
            mediate_index = half_window
        if choice > len(self.exps) - 1 - half_window:
            mediate_index = len(self.exps) - 1 - half_window
        for i in range(0, half_window + 1):
            window_indices.append(mediate_index + i)
            window_indices.append(mediate_index - i)
        choice = random.choice(window_indices)
        return abs(np.random.normal(self.exps[choice], self.stds[choice]))
