from random import randint
from random import choice
import math

run = True

initial = True

points = 0

light_units = 0

mid_units = 0

heavy_units = 0

"""points references: light unit = 2pts, medium unit = 5pts, heavy unit = 10pts"""

def points_gen():
  gen = randint(1, 10)
  global points
  points += gen
  return points

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

faction = ""

faction_chosen = False

def faction_choice():
  global faction
  global faction_chosen

  faction_choice = input("Choose your faction (TYRANNY or NECROPOLIS): ")
  if faction_choice.lower() == "tyranny":
    faction = "TYRANNY"
    print("You have chosen The Tyranny.")
    faction_chosen = True

  elif faction_choice.lower() == "necropolis":
    faction = "NECROPOLIS"
    print("You have chosen The Necropolis.")
    faction_chosen = True

  else:
    print("Invalid faction.")

  return(faction_chosen)
  return(faction)

def action_list():
  global points
  global faction_chosen
  global initial
  global light_units
  global mid_units
  global heavy_units

#current commands:
#earn points
#show points
#buy units
#change faction
#view units (hidden command)
#quit

  if initial == True:
    print("For a list of commands, type 'HELP'.")
    initial = False

  action_choice = input("Choose an action. \n >")

  if action_choice.lower() == "earn":
    gen = randint(1,10)
    bonus = randint(1, 10)
    points += gen
    if bonus == gen:
      points += bonus
      print("Resource trove uncovered!")
      print("%d points earned, plus %d bonus points." % (gen, bonus))
    else:
      print("%d points earned." % gen)
      return points

  elif action_choice.lower() == "show":
    print("You have %d available points." % points)

  elif action_choice.lower() == "help":
    print("Available actions: [EARN] points, [BUY] units, [SHOW] points, change [FACTION], [QUIT] game")

  elif action_choice.lower() == "buy":

    if faction.lower() == "tyranny":
      type_choice = input("Choose a unit type to produce: [INFANTRY]: 2pts, [COMMANDO]: 5pts, [SIEGEBREAKER]: 10pts\n >")

      if type_choice.lower() == "infantry":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 2, 0)))
        cost = (mult * 2)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          light_units += mult
          print("Produced %d INFANTRY units." % mult)

      elif type_choice.lower() == "commando":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 5, 0)))
        cost = (mult * 5)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          mid_units += mult
          print("Produced %d COMMANDO units." % mult)

      elif type_choice.lower() == "siegebreaker":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 10, 0)))
        cost = (mult * 10)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          heavy_units += mult
          print("Produced %d SIEGEBREAKER units." % mult)

      else:
	      print("Unit type not found.")

    else:
      type_choice = input("Choose an undead type to raise: [LEGIONNAIRE]: 2pts, [VENGEFUL]: 5pts, [PROMETHID]: 10pts\n >")

      if type_choice.lower() == "legionnaire":
        mult = int(input("Enter a number of undead to raise (max available = %d): \n >" % round_down(points / 2, 0)))
        cost = (mult * 2)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          light_units += mult
          print("Produced %d LEGIONNAIRE undead." % mult)

      elif type_choice.lower() == "vengeful":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 5, 0)))
        cost = (mult * 5)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          mid_units += mult
          print("Produced %d VENGEFUL undead." % mult)

      elif type_choice.lower() == "promethid":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 10, 0)))
        cost = (mult * 10)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          heavy_units += mult
          print("Produced %d PROMETHID undead." % mult)

      else:
	      print("Undead class not found.")

  elif action_choice.lower() == "faction":
    faction_switch = input("Are you sure? All currently held points and units will be lost. [YES/NO] ")

    if faction_switch.lower() == "yes":
      faction_chosen = False
      initial = True
      points = 0

  elif action_choice.lower() == "units":
    print("Light units: %d" % light_units)
    print("Medium units: %d" % mid_units)
    print("Heavy units: %d" % heavy_units)

  elif action_choice.lower() == "quit":
    quit()

  else:
    print("Unrecognised command.")

while run == True:

  if faction_chosen == False:
    faction_choice()

  else:
    action_list()