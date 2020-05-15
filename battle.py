import copy
import random
from minions import RedWhelp



class Player:
	def __init__(self, name, warband, level=1, life=40):
		self.name = name
		self.warband = warband
		self.level = level
		self.life = life

	# at the end of the battle count damage:
	def count_final_damage(self, alive_minions):
		damage = self.level
		for minion in alive_minions:
			damage += minion.tier
		return damage

	def player_die(self):
		# if self.life < 0:
		pass


class Warband:
	def __init__(self, player, warband):
		self.player = player
		self.warband = warband




class BattleState:
	def __init__ (self, attacking_player, attacked_player):
		self.attacking_player = attacking_player
		self.attacked_player = attacked_player


		

class Battle:
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2

	def choose_first(self, Player1, Player2):
		order = True

		p1 = copy.deepcopy(self.player1.warband)
		p2 = copy.deepcopy(self.player2.warband)	

		w1 = Warband(Player1, p1)
		w2 = Warband(Player2, p2)

		if len(self.player1.warband) < len(self.player2.warband):
			order = False
		elif len(self.player1.warband) == len(self.player2.warband):
			order = random.choice([True, False])

		if order == True:
			game = [w1, w2]
		else:
			game = [w2, w1]

		return w1, w2, game

	def play(self):
		# first player attack
		# next player attack
		# 
		pass


	def print_state(self, statement, w1, w2):
		print()
		print(statement)
		print()
		print(f'{self.player1.name}:')
		if w1.warband:
			for minion in w1.warband:
				print(minion.name, minion.attack_value, minion.health, minion.has_ds)
		else:
			print("Warband empty")	
		print()
		print(f'{self.player2.name}:')
		if w2.warband:
			for minion in w2.warband:
				print(minion.name, minion.attack_value, minion.health, minion.has_ds)
		else:
			print("Warband empty")	
		print()
		print()
		print()


class GameState:
	def __init__(self, player1, player2, warband1, warband2, attacking_player, 
		attacked_player, attacking_warband, attacked_warband, attack1=0, attack2=0, 
		attack_i=0, attacked_i=0):
		self.player1 = player1
		self.player2 = player2
		self.warband1 = warband1
		self.warband2 = warband2
		self.attacking_player = attacking_player
		self.attacked_player = attacked_player
		self.attacking_warband = attacking_warband
		self.attacked_warband = attacked_warband
		self.attack1 = attack1
		self.attack2 = attack2
		self.attack_i = attack_i
		self.attacked_i = attacked_i

	def next_turn(self):
		if self.attacking_player == self.player1:
			self.attacking_player = self.player2
			self.attacked_player = self.player1
			self.attacking_warband = self.warband2
			self.attacked_warband = self.warband1
			self.attack1 = self.attack_i
			self.attack2 = self.attacked_i
			self.attack_i = self.attack2
			self.attacked_i = self.attack1
		else:
			self.attacking_player = self.player1
			self.attacked_player = self.player2
			self.attacking_warband = self.warband1
			self.attacked_warband = self.warband2
			self.attack2 = self.attack_i
			self.attack1 = self.attacked_i
			self.attack_i = self.attack1
			self.attacked_i = self.attack2

	def count_taunts(self):
		output = 0
		taunted_minions = []
		for minion in self.attacked_warband.warband:
			if minion.taunt == True:
				output += 1
				taunted_minions.append(minion)
		return output, taunted_minions

	def start_of_combat(self):
		red_whelp_list, red_whelp_dict = self.create_rw_list_and_dict(self.attacking_warband, self.attacked_warband)
		red_whelp_list2, red_whelp_dict2 = self.create_rw_list_and_dict(self.attacked_warband, self.attacking_warband)
		red_whelp_dict.update(red_whelp_dict2)
		red_whelp_list.extend(red_whelp_list2)
		# randomly choose attacking red whelp
		while red_whelp_list:
			random_rw = random.choice(red_whelp_list)
			friendly_warband = red_whelp_dict[random_rw][0]
			enemy_warband = red_whelp_dict[random_rw][1]
			random_rw.attack_in_start_of_combat(friendly_warband, enemy_warband)
			red_whelp_list.remove(random_rw)

	def create_rw_list_and_dict(self, friendly_warband, enemy_warband):
		red_whelp_list = []
		red_whelp_dict = {}
		for minion in friendly_warband.warband:
			if isinstance(minion, RedWhelp):
				red_whelp_list.append(minion)
				red_whelp_dict[minion] = (friendly_warband, enemy_warband)
		return red_whelp_list, red_whelp_dict

# May 14th: 159 lines of code