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
        self.inventory = []  # V1-E

        self.g = Grid()
        self.g.set_player(self.player)
        self.g.make_walls()
        pickups.randomize(self.g)


# TODO: flytta denna till en annan fil
def print_status(game_grid, state):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {state.score} points.")
    print(game_grid)


def handle_move(dx, dy, state):
    """Försök flytta spelaren i angiven riktning. (V1-B, V1-C, V1-G)"""
    if state.player.can_move(dx, dy, state.g):
        next_x = state.player.pos_x + dx
        next_y = state.player.pos_y + dy
        maybe_item = state.g.get(next_x, next_y)

        state.player.move(dx, dy)

        # V1-G: The floor is lava
        state.score -= 1

        # V1-D + V1-E: Pickup och inventory
        if isinstance(maybe_item, pickups.Item):
            state.score += maybe_item.value
            state.inventory.append(maybe_item)
            state.g.clear(state.player.pos_x, state.player.pos_y)
            print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
    else:
        print("You can't move that way!")


def print_inventory(state):
    """Skriv ut inventory. (V1-F)"""
    if not state.inventory:
        print("Your inventory is empty.")
    else:
        print("Inventory:")
        for item in state.inventory:
            print(f"  - {item.name} (value: {item.value})")


def start(state):
    command = "a"
    # Loopa tills användaren trycker Q eller X.
    while not command.casefold() in ["q", "x"]:
        print_status(state.g, state)

        command = input("Use WASD to move, Q/X to quit. ")
        command = command.casefold()[:1]

        # V1-B: Alla fyra riktningar
        if command == "d":
            handle_move(1, 0, state)
        elif command == "a":
            handle_move(-1, 0, state)
        elif command == "w":
            handle_move(0, -1, state)
        elif command == "s":
            handle_move(0, 1, state)
        elif command == "i":   # V1-F
            print_inventory(state)

    # Hit kommer vi när while-loopen slutar
    print("Thank you for playing!")


if __name__ == "__main__":
    game_state = GameState()
    start(game_state)
