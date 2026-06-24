import random


class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor."""
    width = 36
    height = 12
    empty = "."  # Tecken för en tom ruta
    wall = "■"   # Tecken för en ogenomtränglig vägg

    def __init__(self):
        """Skapa ett objekt av klassen Grid"""
        self.data = [[self.empty for y in range(self.width)] for z in range(self.height)]

    def get(self, x, y):
        """Hämta det som finns på en viss position"""
        return self.data[y][x]

    def set(self, x, y, value):
        """Ändra vad som finns på en viss position"""
        self.data[y][x] = value

    def set_player(self, player):
        self.player = player

    def clear(self, x, y):
        """Ta bort item från position"""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid)"""
        xs = ""
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += "@"
                else:
                    xs += str(row[x])
            xs += "\n"
        return xs

    def make_walls(self):
        """Skapa väggar runt hela spelplanen. (V1-H: for-loopar används)"""
        # Yttervägg – samma som original
        for i in range(self.height):
            self.set(0, i, self.wall)
            self.set(self.width - 1, i, self.wall)

        for j in range(1, self.width - 1):
            self.set(j, 0, self.wall)
            self.set(j, self.height - 1, self.wall)

        # V1-H: Inner-väggar med for-loopar
        # Vertikal vägg höger om mitten, passage vid y=5
        for y in range(1, 5):
            self.set(22, y, self.wall)
        for y in range(6, self.height - 1):
            self.set(22, y, self.wall)

    def get_random_x(self):
        """Slumpa en x-position inuti spelplanen (ej yttervägg)"""
        return random.randint(1, self.width - 2)

    def get_random_y(self):
        """Slumpa en y-position inuti spelplanen (ej yttervägg)"""
        return random.randint(1, self.height - 2)

    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta"""
        return self.get(x, y) == self.empty
