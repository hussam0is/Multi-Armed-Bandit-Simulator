import numpy as np
import matplotlib.pyplot as plt

from game import Game
from player import Player
from models import Model
from matplotlib.gridspec import GridSpec


def remove_max(x):
    x.remove(max(x.copy()))
    return x


def format_axes(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)


def results():
    num_of_players = len(arms_selections.keys())
    fig = plt.figure(constrained_layout=True)
    c = 40
    gs = GridSpec(5, c*num_of_players, figure=fig)
    for i, player in enumerate(arms_selections.copy().keys()):
        j = i*c
        ax = fig.add_subplot(gs[0:2, j:j+c-6])
        clrs = ['r' if x == max(arms_selections[player].copy()) or x == max(remove_max(arms_selections[player].copy())) else 'b' for x in arms_selections[player].copy()]
        ax.bar(arms, height=arms_selections[player], color=clrs)
        for j, v in enumerate(arms_selections[player]):
            ax.text(j-0.3+1, v+0.25, str(v), color=clrs[j], fontweight='bold', fontsize=6)
        plt.xticks(arms, [str(arm)+':'+str(e) for e, arm in zip(expectations, arms)], color='orange', rotation=45, fontweight='bold', fontsize='6', horizontalalignment='right')
        plt.title(str(player)+'\'s selections', fontsize=10)
    plt.show()


def play_game(game, players, rounds):
    players_scores = [0] * len(players)
    zero_one_score = []
    print(f'Game Started for players {[player.name for player in players]}')
    for round in range(1, rounds + 1):
        rewards = []
        if round % players[0].for_every == 500:
            print(f'round ----({round})----- Started!!')
        for i, player in enumerate(players):
            choice = player.play()
            reward = game.play(choice)
            rewards.append(reward)
            players_scores[i] += reward
            player.update_score(reward)
            arms_selections[player.name][choice - 1] += 1

        winner = players[rewards.index(max(rewards))].name
        zero_one_score.append(winner)
    print(f'Game Ended!')
    for player in players:
        score = len([x for x in zero_one_score if x == player.name])
        print(f'{player.name}\'s Score: {score}')

    for i, player in enumerate(players):
        print(
            f'{player.name}\'s Total Earnings is : {players_scores[i]}, Earnings Rate: {100 * players_scores[i] / (sum(players_scores))}')
    max_score_index = [i for i, score in enumerate(players_scores) if score == max(players_scores.copy())][0]
    winner = players[max_score_index].name
    print(f'{winner} Won!')
    results()
    return winner


if __name__ == '__main__':

    # Game
    rounds = 100
    global expectations
    expectations = [23, 23.5, 22.5, 23.1, 23.9, 10, 21, 19]
    stds = [1] * len(expectations)
    global arms
    arms = [i + 1 for i in range(len(expectations))]
    g = Game(exps=expectations, stds=stds)

    # Players
    player1 = Player(name='Hussam', arms=arms, model=Model().ExploreExploit, rounds=rounds, alpha=1)
    player2 = Player(name='Nimer', arms=arms, model=Model().ExploreExploit2, rounds=rounds, alpha=1)
    player3 = Player(name='Othman', arms=arms, model=Model().ExploreExploit3, rounds=rounds, alpha=1)
    player_4_rand = Player(name='Random', arms=arms, model=Model().RandomChoices, rounds=rounds)
    players = [player1, player2, player3, player_4_rand]

    global arms_selections
    arms_selections = {player.name: [0] * len(arms) for player in players}

    play_game(g, players, rounds)









