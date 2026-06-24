class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=20, symbol="?"):
        self.name = name
        self.value = value  # V1-D: Fruktsallad - alla items är värda 20 poäng
        self.symbol = symbol

    def __str__(self):
        return self.symbol


pickups = [
    Item("carrot",      symbol="c"),
    Item("apple",       symbol="a"),
    Item("strawberry",  symbol="s"),
    Item("cherry",      symbol="h"),
    Item("watermelon",  symbol="w"),
    Item("radish",      symbol="r"),
    Item("cucumber",    symbol="u"),
    Item("meatball",    symbol="m"),
]


def randomize(grid):
    for item in pickups:
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, item)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen
