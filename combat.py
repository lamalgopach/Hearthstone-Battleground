import random
from random import choice
import copy
# from battle import Player, Warband, Battle, GameState
from battle import Player, Warband, BattleState
from minions import RedWhelp
from creating_minions_in_warbands import create_warband


def choose_first(player1, player2):
	order = True

	p1 = copy.deepcopy(player1.warband)
	p2 = copy.deepcopy(player2.warband)	

	w1 = Warband(Player1, p1)
	w2 = Warband(Player2, p2)

	if len(player1.warband) < len(player2.warband):
		order = False
	elif len(player1.warband) == len(player2.warband):
		order = random.choice([True, False])

	if order == True:
		game = [w1, w2]
	else:
		game = [w2, w1]

	return w1, w2, game


alices_warband = create_warband()
bobs_warband = create_warband()

Player1 = Player("Alice", alices_warband)
Player2 = Player("Bob", bobs_warband)
#what are players names? into console

w1, w2, game = choose_first(Player1, Player2)

attacking_player = Player1 if game[0] == w1 else Player2
attacked_player = Player2 if game[1] == w2 else Player1

attacking_warband = w1 if game[0] == w1 else w2
attacked_warband = w2 if game[1] == w2 else w1

battle_state = BattleState(attacking_player, attacked_player, attacking_warband, attacked_warband)
battle_state.print_state("START OF THE GAME: ")

def combat(w1, w2):

	battle_state.start_of_combat()
	battle_state.print_state("after start of combat:")

	# attack till at least one player has no minions:
	while attacking_warband.warband and attacked_warband.warband:

		# assign attacked minion:
		attacked_minion = None
		# count dead minions:
		dead_attacking_minion = 0
		dead_attacked_minion = 0

		if battle_state.count_taunts()[0] > 0:
			taunts = battle_state.count_taunts()[1]
			r = random.randint(0, len(taunts) - 1)
			minion = taunts[r]

			for i in range(len(battle_state.attacked_warband.warband)):
				if battle_state.attacked_warband.warband[i].name == minion.name:
					attacked_minion = i
					break

		# otherwise attacked minion is chosen randomly:
		else:
			attacked_minion = random.randint(0, len(battle_state.attacked_warband.warband) - 1)	

		# create minions in game:
		print(battle_state.attack_i, "dziendobry")
		minion1 = battle_state.attacking_warband.warband[battle_state.attack_i]
		minion2 = battle_state.attacked_warband.warband[attacked_minion]
			
		print("attacker", minion1.name, minion1.attack_value, minion1.health)
		print("attacked", minion2.name, minion2.attack_value, minion2.health)
		print()

		# attack phase:
		minion1.attack()
		minion1.take_damage(minion2.attack_value)
		minion2.take_damage(minion1.attack_value)


		# print(f'after {battle_state.attacking_warband.name}\'s attack')
		print("attacker", minion1.name, minion1.attack_value, minion1.health)
		print("attacked", minion2.name, minion2.attack_value, minion2.health)
		print()

		if minion1.health < 1:
			minion1.die(battle_state.attacking_warband.warband, battle_state.attack_i)
			dead_attacking_minion = 1

		if minion2.health < 1:
			minion2.die(battle_state.attacked_warband.warband, attacked_minion)
			dead_attacked_minion += 1

		# next minion:
		# (if attacker is dead we should keep track it)
		battle_state.attack_i += 1 - dead_attacking_minion

		# if the last minion in the warband was attacking start once again:
		if battle_state.attack_i > len(battle_state.attacking_warband.warband) - 1:
			battle_state.attack_i = 0

		if dead_attacked_minion == 1:
			if battle_state.attacked_i > attacked_minion:
				battle_state.attacked_i -= 1

		# if attacked player has attacking his last minion in the warband 
		# start again:
		if battle_state.attacked_i > len(battle_state.attacked_warband.warband) - 1:
			battle_state.attacked_i = 0

		statement = f'Warbands after {battle_state.attacking_player.name}\'s attack:'
		battle_state.print_state(statement)

		# end of turn, change the player:
		battle_state.play_next()

	if not w1.warband and not w2.warband:
		print("NO WINNER")
		damage = 0

	else:
		print()
		winner = Player1 if w1.warband else Player2
		loser = Player2 if w1.warband else Player1
		print(f'{winner.name} WINNER')
		print(f'{loser.name} LOSER')
		damage = Player1.count_final_damage(w1.warband) if w1.warband else Player2.count_final_damage(w2.warband)
		loser.life -= damage
		print(f'DAMAGE: {damage}')

	print(Player1.life, "Player1 life", Player1.name)
	print(Player2.life, "Player2 life", Player2.name)

combat(w1, w2)

# May 14th: 137 lines of code