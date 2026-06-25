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
        self.inventory = []          # V1-E: Lista med uppplockade föremål
        self.keys_in_inventory = 0   # V2: Räknare för nycklar
        self.items_collected = 0     # V2: Exit – räknar plockade frukter
        self.moves_since_pickup = 0  # V3: Grace period – steg sedan senaste pickup

        # Skapa spelplanen och placera ut väggar och föremål
        self.g = Grid()
        self.g.set_player(self.player)
        self.g.make_walls()
        pickups.randomize(self.g)
        self.g.place_exit()          # V2: Exit – placera utgången sist


def print_status(game_grid, state):
    """Visa spelvärlden, poäng och antal nycklar."""
    print("--------------------------------------")
    print(f"You have {state.score} points. | Keys: {state.keys_in_inventory}")
    print(game_grid)


def print_inventory(state):
    """Skriv ut innehållet i spelarens inventory. (V1-F)"""
    if not state.inventory:
        print("Your inventory is empty.")
    else:
        print("--- Inventory ---")
        for item in state.inventory:
            print(f"  - {item.name}")
        print("-----------------")


# --- Pickup-hantering uppdelad i egna funktioner för tydlighet ---

def _pickup_fruit(item, state):
    """Hanterar upplockning av en frukt. Returnerar True om spelet är slut."""
    state.score += item.value
    state.inventory.append(item)
    state.items_collected += 1
    state.moves_since_pickup = 0   # V3: Nollställ grace period vid pickup
    state.g.clear(state.player.pos_x, state.player.pos_y)
    print(f"You found a {item.name}, +{item.value} points.")
    return False


def _pickup_trap(state):
    """Hanterar att spelaren går på en fälla. (V2: Fällor)"""
    state.score -= 10
    print("You stepped on a trap! -10 points.")
    return False


def _pickup_spade(state):
    """Hanterar upplockning av en spade. (V2: Spade)"""
    state.player.has_spade = True
    state.inventory.append(pickups.Spade())
    state.g.clear(state.player.pos_x, state.player.pos_y)
    print("You picked up a spade! Walk into a wall to use it.")
    return False


def _pickup_key(state):
    """Hanterar upplockning av en nyckel. (V2: Nycklar och kistor)"""
    state.keys_in_inventory += 1
    state.inventory.append(pickups.Key())
    state.g.clear(state.player.pos_x, state.player.pos_y)
    print("You picked up a key!")
    return False


def _pickup_chest(state):
    """Hanterar interaktion med en kista. (V2: Nycklar och kistor)"""
    if state.keys_in_inventory > 0:
        state.keys_in_inventory -= 1
        state.score += pickups.Chest.treasure_value
        state.g.clear(state.player.pos_x, state.player.pos_y)
        print(f"You opened a chest! +{pickups.Chest.treasure_value} points.")
    else:
        print("The chest is locked. Find a key first!")
    return False


def _pickup_exit(state):
    """Hanterar att spelaren når utgången. (V2: Exit)"""
    if state.items_collected >= pickups.original_pickup_count:
        print(f"\nYou escaped! Final score: {state.score}")
        return True   # Spelet är slut – spelaren vann
    else:
        remaining = pickups.original_pickup_count - state.items_collected
        print(f"Exit is locked! Collect {remaining} more fruit(s) first.")
    return False


def handle_pickup(maybe_item, state):
    """Avgör vad som finns på rutan och anropar rätt pickup-funktion.
    Returnerar True om spelet är slut."""
    if isinstance(maybe_item, pickups.Item):
        return _pickup_fruit(maybe_item, state)
    elif isinstance(maybe_item, pickups.Trap):
        return _pickup_trap(state)
    elif isinstance(maybe_item, pickups.Spade):
        return _pickup_spade(state)
    elif isinstance(maybe_item, pickups.Key):
        return _pickup_key(state)
    elif isinstance(maybe_item, pickups.Chest):
        return _pickup_chest(state)
    elif maybe_item == state.g.exit_symbol:
        return _pickup_exit(state)
    return False


def handle_move(dx, dy, state):
    """Försök flytta spelaren i angiven riktning. (V1-B, V1-C, V1-G)
    Returnerar True om spelet är slut."""
    if state.player.can_move(dx, dy, state.g):
        # Kolla vad som finns på nästa ruta innan vi flyttar
        next_x = state.player.pos_x + dx
        next_y = state.player.pos_y + dy
        maybe_item = state.g.get(next_x, next_y)

        state.player.move(dx, dy)

        # V1-G + V3: The floor is lava – tappa 1 poäng per steg.
        # Grace period: inga poängavdrag de första 5 stegen efter pickup.
        state.moves_since_pickup += 1
        if state.moves_since_pickup > 5:
            state.score -= 1

        return handle_pickup(maybe_item, state)
    else:
        print("You can't move that way!")
        return False


def start(state):
    """Huvudspelloopen – körs tills spelaren avslutar eller vinner."""
    print("Welcome to Fruit Loop!")
    print("Collect all fruits (?), then reach the Exit (E) to win.")
    print("Watch out for traps (X)! Keys (K) open chests (C). Spade (P) removes walls.")

    command = "a"
    game_over = False

    # Loopa tills användaren trycker Q/X eller vinner
    while command not in ["q", "x"] and not game_over:
        print_status(state.g, state)

        command = input("Use WASD to move, I for inventory, Q/X to quit. ")
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

    print(f"Thank you for playing! Final score: {state.score}")


# __name__ sätts till "__main__" om man startar game.py direkt.
# Detta förhindrar att start() körs vid import, t.ex. vid testning.
if __name__ == "__main__":
    game_state = GameState()
    start(game_state)
