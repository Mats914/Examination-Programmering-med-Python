class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=20, symbol="?"):
        self.name = name
        self.value = value  # V1-D: Fruktsallad - alla items är värda 20 poäng
        self.symbol = symbol

    def __str__(self):
        return self.symbol


# V1-D: value=20 istället för 10. Symbol "?" behålls som original.
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


def randomize(grid):
    for item in pickups:
        while True:
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, item)
                break
