# arm_bandits_simulator
A simulation of Multi-arm bandit problem using **Successive Elimination** algorithm.
Rewards for each arm are driven from noraml distributions.

**Input:**
1- expectations= -list of rewards expectations to assign for each arm reward-
2- stds = -list of standard deviation to assign for each arm reward-

we have:
r(arm_i)~N(exps[i], stds[i])

3- assign each player's required parameters
4- enter number of rounds
5- enter number of games to play = simulation rounds

**Output:**
winner = has the biggest ammount of cash
Model ExploreExploite3 gets the best results.
the model tries to identify arms with the highest rewards using successive elimination algorithm.

the original probability of the follow inequality is: for each arm i and number of times m where arm i chosen we have P(|mu_m - mu*|< lambda_m)<1- 2/(T^4)
here the rewards came from a bernollie distribution function. 
to apply the equation on normal distribution, I calculated the modification needed for lambda_m, which is to multiply it by m^0.5 which got the best results in model ExploreExploite3. 

for any questions you may contact me at hussam.is@outlook.com


one game results:

![alt text](https://github.com/hussam0is/arm_bandits_simulator/blob/main_br/one_game_results.png)




Simulation results:


![alt text](https://github.com/hussam0is/arm_bandits_simulator/blob/main_br/simulation_results.png)

