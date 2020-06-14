import random
from enum import Enum

class MinionType(Enum):
	MINION = 0
	MURLOC = 1
	DRAGON = 2
	BEAST = 3
	MECH = 4
	DEMON = 5


class Card:
	def __init__(self, *, name, attack_value, health, tier, m_type, taunt=False, 
		has_ds=False, has_deathrattle=False, has_triggered_attack=False, 
		has_overkill=False, poisonous=False, damage_effect=False, has_windfury=False):

		self.name = name
		self.attack_value = attack_value
		self.health = health
		self.tier = tier
		self.m_type = m_type
		self.taunt = taunt
		self.has_ds = has_ds
		self.has_deathrattle = has_deathrattle
		self.has_triggered_attack = has_triggered_attack
		self.has_overkill = has_overkill
		self.poisonous = poisonous
		self.damage_effect = damage_effect
		self.has_windfury = has_windfury

	def attack(self):
		# used in Glyph Guardian
		return

	def take_poison(self):
		
		if self.has_ds:
			self.has_ds = False

		else:
			self.health = 0

	def take_damage(self, damage, poisonous):
		if damage == 0:
			return

		if self.has_ds:
			self.has_ds = False
		elif poisonous:
			self.health = 0
		else:
			self.health -= damage
		# if self.has_ds:
		# 	self.has_ds = False
		# else:
		# 	self.health -= damage

	def die(self, battle, status, j):
		friendly_minions = battle.attacking_player.warband if status == 1 else battle.attacked_player.warband
		# dead_warband = battle.attacking_player.dead_minions if status == 1 else battle.attacked_player.dead_minions
		del friendly_minions[j]
		# dead_warband.append(self)
		if status == 1:
			battle.attacking_player.dead_minions_dict[self] = j
			battle.attacking_player.dead_minions.append(self)
		else:
			battle.attacked_player.dead_minions_dict[self] = j
			battle.attacked_player.dead_minions.append(self)

	def triggered_attack(self, battle):
		enemy_minions = battle.attacked_player.warband
		j = battle.attacked_player.attacked_minion
		if j != 0 and j + 1 < len(enemy_minions):
			a = j - 1
			b = j + 1	
			enemy_minions[b].take_damage(self.attack_value, self.poisonous)
		elif j == 0 and j + 1 <= len(enemy_minions):
			a = j + 1
		elif j == len(enemy_minions) - 1:
			a = j - 1
		enemy_minions[a].take_damage(self.attack_value, self.poisonous)

	def summon_minion(self, minion_class):
		minion = minion_class()
		return minion


class BrannBronzebeard(Card):
# add effect
	def __init__(self):
		super().__init__(name="Brann Bronzebeard", attack_value=2, health=4, tier=5, 
						m_type=MinionType.MINION)



class CrowdFavorite(Card):
	# add special function later
	def __init__(self):
		super().__init__(name="Crowd Favorite", attack_value=4, health=4, tier=3, 
						m_type=MinionType.MINION)


class Crystalweaver(Card):
	#btlcry
	def __init__(self):
		super().__init__(name="Crystalweaver", attack_value=5, health=4, tier=3, 
						m_type=MinionType.MINION)


class DefenderOfArgus(Card):
	#btlcry
	def __init__(self):
		super().__init__(name="Defender of Argus", attack_value=2, health=3, tier=4, 
						m_type=MinionType.MINION)


class Houndmaster(Card):
	#btlcry
	def __init__(self):
		super().__init__(name="Houndmaster", attack_value=4, health=3, tier=3, 
						m_type=MinionType.MINION)


class KangorsApprentice(Card):
	def __init__(self):
		super().__init__(name="Kangor's Apprentice", attack_value=3, health=6, tier=6, 
						m_type=MinionType.MINION, has_deathrattle=True)

	def deathrattle(self, battle, status):
		friendly_minions = battle.attacking_player.warband if status == 1 else battle.attacked_player.warband
		j = battle.attacking_player.dead_minions_dict[self] if status == 1 else battle.attacked_player.dead_minions_dict[self]

		warband = []
		warband = battle.attacking_player.dead_minions if status == 1 else battle.attacked_player.dead_minions

		mechs_to_summon = []

		for minion in warband:
			if minion.m_type == MinionType.MECH:
				mechs_to_summon.append(minion)
		
		if mechs_to_summon:
			mechs = []
			i = 0
			for mech in mechs_to_summon:
				if len(friendly_minions) < 7 and i < 2:
					summoned_mech = self.summon_minion(type(mech))

					# summoned_mech.attack_value = mech.attack_value
					# summoned_mech.health = mech.health
					# summoned_mech.taunt = mech.taunt
					# summoned_mech.has_ds = mech.has_ds
					# summoned_mech.has_deathrattle = mech.has_deathrattle
					# summoned_mech.has_triggered_attack = mech.has_triggered_attack
					# summoned_mech.damage_effect = mech.damage_effect

					friendly_minions.insert(j + i, summoned_mech)
					i += 1
				else:
					break


class LightfangEnforcer(Card):
	# effect
	def __init__(self):
		super().__init__(name="Lightfang Enforcer", attack_value=2, health=2, tier=5, 
						m_type=MinionType.MINION)

class MenagerieMagician(Card):
	#btlcry
	def __init__(self):
		super().__init__(name="Menagerie Magician", attack_value=4, health=4, tier=4, 
						m_type=MinionType.MINION)


class NadinaTheRed(Card):
	def __init__(self):
		super().__init__(name="Nadina The Red", attack_value=7, health=4, tier=6, 
						m_type=MinionType.MINION, has_deathrattle=True)
	
	def deathrattle(self, battle, status):
		friendly_minions = battle.attacking_player.warband if status == 1 else battle.attacked_player.warband

		if friendly_minions:
			for minion in friendly_minions:
				if minion.m_type == MinionType.DRAGON:
					minion.has_ds = True

class RedWhelp(Card):
	def __init__(self):
		super().__init__(name="Red Whelp", attack_value=1, health=2, tier=1, 
						m_type=MinionType.DRAGON)

	def add_damage_in_combat(self, friendly_minions):
		damage = 0
		for minion in friendly_minions:
			if minion.m_type == MinionType.DRAGON:
				damage += 1
		return damage


class RighteousProtector(Card):
	def __init__(self):
		super().__init__(name="Righteous Protector", attack_value=1, health=1, tier=1, 
						m_type=MinionType.MINION, taunt=True, has_ds =True)


class SelflessHero(Card):
	def __init__(self):
		super().__init__(name="Selfless Hero", attack_value=2, health=1, tier=1, 
						m_type=MinionType.MINION, has_deathrattle=True)

	def deathrattle(self, battle, status):
		friendly_minions = battle.attacking_player.warband if status == 1 else battle.attacked_player.warband
	
		if not friendly_minions:
			return

		minions_no_ds = [minion for minion in friendly_minions if not minion.has_ds]
		
		if not minions_no_ds:
			return

		minion = random.choice(minions_no_ds)
		minion.has_ds = True


class ShifterZerus(Card):
	# add effect
	def __init__(self):
		super().__init__(name="Shifter Zerus", attack_value=1, health=1, tier=3, 
						m_type=MinionType.MINION)


class SpawnOfnZoth(Card):
	def __init__(self):
		super().__init__(name="Spawn Of n'Zoth", attack_value=2, health=2, tier=2, 
						m_type=MinionType.MINION, has_deathrattle=True)
	
	def deathrattle(self, battle, status):
		friendly_minions = battle.attacking_player.warband if status == 1 else battle.attacked_player.warband

		if friendly_minions:
			for minion in friendly_minions:
				minion.attack_value += 1
				minion.health += 1


class StrongshellScavenger(Card):
	# btlcry
	def __init__(self):
		super().__init__(name="Strongshell Scavenger", attack_value=2, health=3, tier=5,
						m_type=MinionType.MINION)


class UnstableGhoul(Card):
	def __init__(self):
		super().__init__(name="Unstable Ghoul", attack_value=1, health=3, tier=2, 
						m_type=MinionType.MINION, has_deathrattle=True)
	
	def deathrattle(self, battle, status):
		friendly_minions = battle.attacking_player.warband if status == 1 else battle.attacked_player.warband
		enemy_minions = battle.attacked_player.warband if status == 1 else battle.attacking_player.warband

		if friendly_minions:
			for minion in friendly_minions:
				minion.take_damage(1, self.poisonous)

		if enemy_minions:
			for minion in enemy_minions:
				minion.take_damage(1, self.poisonous)

class VirmenSensei(Card):
	#btlcry
	def __init__(self):
		super().__init__(name="Virmen Sensei", attack_value=4, health=5, tier=4, 
						m_type=MinionType.MINION)

class WaxriderTogwaggle(Card):
	def __init__(self):
		super().__init__(name="Waxrider Togwaggle", attack_value=1, health=2, tier=2, 
						m_type=MinionType.MINION)

	def change_stats(self):
		self.health += 2
		self.attack_value += 2

class WrathWeaver(Card):
	#btlcry damage
	def __init__(self):
		super().__init__(name="Wrath Weaver", attack_value=1, health=1, tier=1, 
						m_type=MinionType.MINION)

class ZappSlywick(Card):
	def __init__(self):
		super().__init__(name="ZappSlywick", attack_value=7, health=10, tier=6, 
						m_type=MinionType.MINION, has_windfury=True)	

# class(es) not imported to create minions in warbands
class FinkleEinhorn(Card):
	def __init__(self):
		super().__init__(name="Finkle Einhorn", attack_value=3, health=3, tier=1, 
						m_type=MinionType.MINION)


# Jakub:
# minion = SpawnOfnZoth()
# if minion.deathrattle is not None:
# # if hasattr(minion, "deathrattle"):
# 	minion.deathrattle(friendly_minions, j)

# 	def attack(self, game_state, target):
# 		target.health -= self.attack_value
# 		self.health -= target.attack_value
# 		return game_state

# class GlyphGuardian(Minion):
# 	def attack(*args, **kwargs):
# 		self.attack_value *= 2
# 		super().attack(*args, **kwargs)


#todo:
# classes to do: waxtoggler