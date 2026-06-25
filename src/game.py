# Huvudfil för spelet Fruit Loop.
# Starta spelet med: python -m src.game

from src.grid import Grid
from src.player import Player
from src import pickups


class GameState:
    """Samlar spelets alla variabler och tillstånd i en klass."""
    def __init__(self):
        # V1-A: Spelaren börjar nära mitten av spelplanen
        start_x = Grid.width // 2
        start_y = Grid.height // 2
        self.player = Player(start_x, start_y)

        self.score = 0
        self.inventory = []        # V1-E: Lista med uppplockade föremål
        self.keys_in_inventory = 0 # V2: Håller reda på antal nycklar
        self.moves_since_pickup = 0  # V3: Grace period – antal steg sedan senaste pickup
        self.items_collected = 0   # V2: Exit – räknar hur många ursprungliga items man plockat

        # Skapa spelplanen och placera ut väggar och föremål
        self.g = Grid()
        self.g.set_player(self.player)
        self.g.make_walls()
        pickups.randomize(self.g)
        self.g.place_exit()  # V2: Exit – placera utgången


def print_status(game_grid, state):
    """Visa spelvärlden, antal poäng och antal nycklar."""
    print("--------------------------------------")
    print(f"You have {state.score} points. | Keys: {state.keys_in_inventory}")
    print(game_grid)


def handle_pickup(maybe_item, state):
    """Hanterar vad som händer när spelaren går på en ruta med ett föremål."""

    if isinstance(maybe_item, pickups.Item):
        # Vanlig frukt – lägg till poäng och inventory
        state.score += maybe_item.value
        state.inventory.append(maybe_item)
        state.items_collected += 1
        state.moves_since_pickup = 0  # V3: Nollställ grace period
        state.g.clear(state.player.pos_x, state.player.pos_y)
        print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")

    elif isinstance(maybe_item, pickups.Trap):
        # V2: Fälla – tappa 10 poäng, fällan ligger kvar
        state.score -= 10
        print("You stepped on a trap! -10 points.")

    elif isinstance(maybe_item, pickups.Key):
        # V2: Nyckel – plocka upp och lägg i inventory
        state.keys_in_inventory += 1
        state.inventory.append(maybe_item)
        state.g.clear(state.player.pos_x, state.player.pos_y)
        print("You picked up a key!")

    elif isinstance(maybe_item, pickups.Chest):
        # V2: Kista – öppna om man har en nyckel
        if state.keys_in_inventory > 0:
            state.keys_in_inventory -= 1
            state.score += pickups.Chest.treasure_value
            state.g.clear(state.player.pos_x, state.player.pos_y)
            print(f"You opened a chest! +{pickups.Chest.treasure_value} points.")
        else:
            print("The chest is locked. Find a key first!")

    elif maybe_item == state.g.exit_symbol:
        # V2: Exit – vinn spelet om alla ursprungliga items är plockade
        if state.items_collected >= pickups.original_pickup_count:
            print(f"\n🎉 You escaped! Final score: {state.score}")
            return True  # Signalera att spelet är slut

    return False  # Spelet fortsätter


def handle_move(dx, dy, state):
    """Försök flytta spelaren i angiven riktning.
    Kontrollerar väggar, hanterar pickup, drar poäng per steg. (V1-B, V1-C, V1-G)
    Returnerar True om spelet är slut (spelaren nådde exit)."""

    if state.player.can_move(dx, dy, state.g):
        # Kolla vad som finns på nästa ruta innan vi flyttar
        next_x = state.player.pos_x + dx
        next_y = state.player.pos_y + dy
        maybe_item = state.g.get(next_x, next_y)

        # Flytta spelaren
        state.player.move(dx, dy)

        # V1-G / V3: The floor is lava – tappa 1 poäng per steg
        # Grace period: inga poängavdrag de första 5 stegen efter pickup
        state.moves_since_pickup += 1
        if state.moves_since_pickup > 5:
            state.score -= 1

        # Hantera det som finns på den nya rutan
        game_over = handle_pickup(maybe_item, state)
        return game_over
    else:
        print("You can't move that way!")
        return False


def print_inventory(state):
    """Skriv ut innehållet i spelarens inventory. (V1-F)"""
    if not state.inventory:
        print("Your inventory is empty.")
    else:
        print("--- Inventory ---")
        for item in state.inventory:
            print(f"  - {item.name}")
        print("-----------------")


def start(state):
    """Huvudspelloopen – körs tills spelaren avslutar eller vinner."""
    print("Welcome to Fruit Loop!")
    print("Collect all fruits and find the Exit (E) to win.")
    print("Watch out for traps (X)! Use keys (K) to open chests (C).")

    command = "a"
    game_over = False

    # Loopa tills användaren trycker Q/X eller vinner
    while not command.casefold() in ["q", "x"] and not game_over:
        print_status(state.g, state)

        command = input("Use WASD to move, Q/X to quit. ")
        command = command.casefold()[:1]

        # V1-B: Rörelse i alla fyra riktningar
        if command == "d":
            game_over = handle_move(1, 0, state)
        elif command == "a":
            game_over = handle_move(-1, 0, state)
        elif command == "w":
            game_over = handle_move(0, -1, state)
        elif command == "s":
            game_over = handle_move(0, 1, state)
        elif command == "i":
            # V1-F: Visa inventory
            print_inventory(state)

    # Hit kommer vi när while-loopen slutar
    print(f"Thank you for playing! Final score: {state.score}")


# __name__ sätts till "__main__" om man startar game.py direkt.
# Detta förhindrar att start() körs vid import, t.ex. vid testning.
if __name__ == "__main__":
    game_state = GameState()
    start(game_state)
