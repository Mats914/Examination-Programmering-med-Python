from src.grid import Grid
from src.player import Player
from src import pickups


# TODO: flytta denna till en annan fil
class GameState:
    """Samla spelets variabler i en klass."""
    def __init__(self):
        # V1-A: Spelaren börjar nära mitten av spelplanen
        self.player = Player(Grid.width // 2, Grid.height // 2)
        self.score = 0
        self.inventory = []  # V1-E: lista för upphittade items

        self.g = Grid()
        self.g.set_player(self.player)
        self.g.make_walls()
        pickups.randomize(self.g)


# TODO: flytta denna till en annan fil
def print_status(game_grid, state):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"Du har {state.score} poäng.")
    print(game_grid)


def handle_move(dx, dy, state):
    """Försök flytta spelaren i angiven riktning.
    Kontrollerar väggar, hanterar pickup och drar 1 poäng per steg. (V1-C, V1-E, V1-G)"""
    if state.player.can_move(dx, dy, state.g):
        next_x = state.player.pos_x + dx
        next_y = state.player.pos_y + dy
        maybe_item = state.g.get(next_x, next_y)

        state.player.move(dx, dy)

        # V1-G: The floor is lava – tappa 1 poäng per steg
        state.score -= 1

        # V1-D + V1-E: Plocka upp item och lägg i inventory
        if isinstance(maybe_item, pickups.Item):
            state.score += maybe_item.value
            state.inventory.append(maybe_item)
            state.g.clear(state.player.pos_x, state.player.pos_y)
            print(f"Du hittade en {maybe_item.name}! +{maybe_item.value} poäng.")
    else:
        print("Det går inte att gå åt det hållet.")


def print_inventory(state):
    """Skriv ut spelarens inventory. (V1-F)"""
    if not state.inventory:
        print("Ditt inventory är tomt.")
    else:
        print("Inventory:")
        for item in state.inventory:
            print(f"  - {item.name} (värde: {item.value})")


def start(state):
    print("Välkommen till Fruit Loop!")
    print("Använd WASD för att röra dig, I för inventory, Q/X för att avsluta.")

    command = "a"
    # Loopa tills användaren trycker Q eller X.
    while not command.casefold() in ["q", "x"]:
        print_status(state.g, state)

        command = input("Kommando (WASD / I / Q): ")
        command = command.casefold()[:1]

        # V1-B: Rörelse i alla fyra riktningar
        if command == "d":    # Höger
            handle_move(1, 0, state)
        elif command == "a":  # Vänster
            handle_move(-1, 0, state)
        elif command == "w":  # Upp
            handle_move(0, -1, state)
        elif command == "s":  # Ned
            handle_move(0, 1, state)
        elif command == "i":  # V1-F: Visa inventory
            print_inventory(state)

    # Hit kommer vi när while-loopen slutar
    print(f"Tack för att du spelade! Slutpoäng: {state.score}")


if __name__ == "__main__":
    game_state = GameState()
    start(game_state)
