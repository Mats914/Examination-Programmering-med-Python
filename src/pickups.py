# Denna fil innehåller alla klasser för föremål samt funktioner för att placera dem på kartan.

import random


class Item:
    """Representerar en frukt eller grönsak man kan plocka upp."""
    def __init__(self, name, value=20, symbol="?"):
        # V1-D: Alla frukter är värda 20 poäng (fruktsallad)
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class Trap:
    """Representerar en fälla på spelplanen.
    Om spelaren går på en fälla förlorar man 10 poäng. Fällan ligger kvar. (V2: Fällor)"""
    symbol = "X"

    def __init__(self):
        self.name = "trap"

    def __str__(self):
        return self.symbol


class Spade:
    """Representerar en spade man kan plocka upp.
    Nästa gång spelaren går in i en vägg används spaden för att ta bort den. (V2: Spade)"""
    symbol = "P"

    def __init__(self):
        self.name = "spade"

    def __str__(self):
        return self.symbol


class Key:
    """Representerar en nyckel man kan plocka upp. (V2: Nycklar och kistor)"""
    symbol = "K"

    def __init__(self):
        self.name = "key"

    def __str__(self):
        return self.symbol


class Chest:
    """Representerar en kista på spelplanen.
    Öppnas med en nyckel och ger 100 poäng. (V2: Nycklar och kistor)"""
    symbol = "C"
    treasure_value = 100

    def __init__(self):
        self.name = "chest"

    def __str__(self):
        return self.symbol


# Lista med alla startfrukter som placeras ut på kartan
pickups = [
    Item("carrot"),
    Item("apple"),
    Item("strawberry"),
    Item("cherry"),
    Item("watermelon"),
    Item("radish"),
    Item("cucumber"),
    Item("meatball"),
]

# Antal ursprungliga frukter – används för att avgöra när Exit aktiveras (V2: Exit)
original_pickup_count = len(pickups)

# Alla möjliga namn på frukter som kan skapas via bördig jord (V2: Bördig jord)
_fertile_names = ["banana", "grape", "peach", "pear", "plum", "lemon", "mango", "kiwi"]


def spawn_new_fruit(grid):
    """Skapar en ny slumpmässig frukt på en ledig ruta. (V2: Bördig jord)"""
    name = random.choice(_fertile_names)
    new_fruit = Item(name)
    _place_on_empty(grid, new_fruit)
    return new_fruit


def randomize(grid):
    """Placera ut alla föremål på slumpmässiga lediga positioner på kartan."""
    # Placera startfrukter
    for item in pickups:
        _place_on_empty(grid, item)

    # V2: Fällor – placera 3 fällor
    for _ in range(3):
        _place_on_empty(grid, Trap())

    # V2: Spade – placera 1 spade
    _place_on_empty(grid, Spade())

    # V2: Nycklar och kistor – 2 nycklar och 2 kistor
    for _ in range(2):
        _place_on_empty(grid, Key())
        _place_on_empty(grid, Chest())


def _place_on_empty(grid, obj):
    """Hjälpfunktion: placera ett objekt på en slumpmässig ledig ruta."""
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, obj)
            break
