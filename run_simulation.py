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
        ax.text(0.5, 0.5, "ax%d" % (i + 1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)


def results(arms_selections, expectations, arms):
    num_of_players = len(arms_selections.keys())
    fig = plt.figure(constrained_layout=True)
    c = 40
    gs = GridSpec(5, c * num_of_players, figure=fig)
    for i, player in enumerate(arms_selections.copy().keys()):
        j = i * c
        ax = fig.add_subplot(gs[0:2, j:j + c - 6])
        clrs = ['r' if x == max(arms_selections[player].copy()) or x == max(
            remove_max(arms_selections[player].copy())) else 'b' for x in arms_selections[player].copy()]
        ax.bar(arms, height=arms_selections[player], color=clrs)
        for j, v in enumerate(arms_selections[player]):
            max_arm = ''
            if clrs[j] == 'r':
                max_arm = str(j+1)+'-'
            ax.text(j - 0.3 + 1, v + 0.25, max_arm + str(v), color=clrs[j], fontweight='bold', fontsize=6)
        plt.xticks(arms, [str(arm) + ':' + str(e) for e, arm in zip(expectations, arms)], color='orange', rotation=45,
                   fontweight='bold', fontsize='6', horizontalalignment='right')
        plt.title(str(player) + '\'s selections', fontsize=10)
    plt.show()


def play_game(game, players, rounds):
    players_scores = [0] * len(players)
    zero_one_score = []
    arms = [i + 1 for i in range(len(game.exps))]
    arms_selections = {player.name: [0] * len(arms) for player in players}
    print(f'Game Started for players {[player.name for player in players]}')
    for _round in range(1, rounds + 1):
        rewards = []
        for i, player in enumerate(players):
            choice = player.play()
            reward = game.play(choice)
            rewards.append(reward)
            players_scores[i] += reward
            player.update_score(reward)
            arms_selections[player.name][choice - 1] += 1

        winner = players[rewards.index(max(rewards))].name
        zero_one_score.append(winner)

    for player in players:
        score = len([x for x in zero_one_score if x == player.name])
        print(f'{player.name}\'s Score: {score}')
    for i, player in enumerate(players):
        print(
            f'{player.name}\'s Total Earnings is : {players_scores[i]}, Earnings Rate: {100 * players_scores[i] / (sum(players_scores))}')
    max_score_index = [i for i, score in enumerate(players_scores) if score == max(players_scores.copy())][0]
    winner = players[max_score_index].name
    print(f'Game Ended. {winner} Won!')
    return winner, arms_selections


def game_simulation(simulations=500):
    # Game parameters
    rounds = 100
    expectations1 = [20,19,17,10,10,20]
    expectations2 = [10, 10, 5, 15, 5, 5, 5, 15, 10, 20, 5, 5, 5, 20, 5, 5, 1, 20, 1, 1, 1, 20,20,1,1]
    expectations = expectations1
    window = 3  # game will pick a random arm at window distance of the player's desired arm
    stds = [2] * len(expectations)
    arms = [i + 1 for i in range(len(expectations))]
    g = Game(exps=expectations, stds=stds, window=window)
    # Players
    player1 = Player(name='Hussam', arms=arms, model=Model().ExploreExploit, rounds=rounds, alpha=1)
    player2 = Player(name='Nimer', arms=arms, model=Model().ExploreExploit2, rounds=rounds, alpha=1)
    player3 = Player(name='Othman', arms=arms, model=Model().ExploreExploit3, rounds=rounds, alpha=1)
    player_4_rand = Player(name='Random', arms=arms, model=Model().RandomChoices, rounds=rounds)
    players = [player1, player2, player3, player_4_rand]
    # Simulation
    wins = {player.name: 0 for player in players}
    for i in range(simulations):
        winner, arms_selections = play_game(g, players, rounds)
        print(f'----------------------------({i + 1})-------------------------------------')
        wins[winner] += 1
        player1 = Player(name='Hussam', arms=arms, model=Model().ExploreExploit, rounds=rounds, alpha=1)
        player2 = Player(name='Nimer', arms=arms, model=Model().ExploreExploit2, rounds=rounds, alpha=1)
        player3 = Player(name='Othman', arms=arms, model=Model().ExploreExploit3, rounds=rounds, alpha=1)
        player_4_rand = Player(name='Random', arms=arms, model=Model().RandomChoices, rounds=rounds)
        players = [player1, player2, player3, player_4_rand]

    results(arms_selections, expectations, arms)  # game results plot of the latest game played
    # simulation results plot
    plt.bar(np.arange(len(players)), wins.values())
    plt.title('Simulation Results')
    for i, v in enumerate(wins):
        plt.text(i - 0.5, wins[v] + 0.001, '   ' + v + ' ' + str(wins[v]) +'\n'+ type(players[i].Model).__name__, fontweight='bold')

    print('Simulation Ended.')
    top_player_index = list(wins.values()).index(max(list(wins.values())))
    top_player = players[top_player_index].name
    best_model = type(players[top_player_index].Model).__name__
    print(f'-{top_player}- is the top player! -{best_model}- is the best Model!')
    plt.show()


if __name__ == '__main__':
    # Game
    game_simulation()
