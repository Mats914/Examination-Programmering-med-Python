# Denna fil innehåller klassen Grid som representerar spelplanen.

import random


class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor."""
    width = 36
    height = 12
    empty = "."   # Tecken för en tom ruta
    wall = "■"    # Tecken för en ogenomtränglig vägg
    exit_symbol = "E"  # Tecken för utgången (V2: Exit)

    def __init__(self):
        """Skapa ett objekt av klassen Grid."""
        # Spelplanen lagras i en lista av listor.
        # Vi använder list comprehension för att sätta "empty" på varje plats.
        self.data = [[self.empty for y in range(self.width)] for z in range(self.height)]

    def get(self, x, y):
        """Hämta det som finns på en viss position."""
        return self.data[y][x]

    def set(self, x, y, value):
        """Ändra vad som finns på en viss position."""
        self.data[y][x] = value

    def set_player(self, player):
        """Spara en referens till spelaren så att vi kan rita ut den."""
        self.player = player

    def clear(self, x, y):
        """Ta bort item från position – sätt rutan till empty."""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid)."""
        xs = ""
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                # Rita spelaren ovanpå det som finns på rutan
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += "@"
                else:
                    xs += str(row[x])
            xs += "\n"
        return xs

    def make_walls(self):
        """Skapa väggar runt hela spelplanen samt inner-väggar med for-loopar. (V1-H)"""

        # --- Yttervägg: vänster och höger kant ---
        for i in range(self.height):
            self.set(0, i, self.wall)
            self.set(self.width - 1, i, self.wall)

        # --- Yttervägg: överkant och underkant ---
        for j in range(1, self.width - 1):
            self.set(j, 0, self.wall)
            self.set(j, self.height - 1, self.wall)

        # --- V1-H: Inner-väggar skapade med for-loopar ---
        # Horisontell vägg i övre halvan (rad 4), med passage vid x=14
        for x in range(1, 14):
            self.set(x, 4, self.wall)
        for x in range(15, self.width - 1):
            self.set(x, 4, self.wall)

        # Vertikal vägg i nedre halvan (kolumn 22), med passage vid y=8
        for y in range(5, 8):
            self.set(22, y, self.wall)
        for y in range(9, self.height - 1):
            self.set(22, y, self.wall)

    def place_exit(self):
        """Placera en utgång (E) på en slumpmässig ledig position. (V2: Exit)"""
        while True:
            x = self.get_random_x()
            y = self.get_random_y()
            if self.is_empty(x, y):
                self.set(x, y, self.exit_symbol)
                break

    def get_random_x(self):
        """Slumpa en x-position inuti spelplanen (ej yttervägg)."""
        return random.randint(1, self.width - 2)

    def get_random_y(self):
        """Slumpa en y-position inuti spelplanen (ej yttervägg)."""
        return random.randint(1, self.height - 2)

    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta."""
        return self.get(x, y) == self.empty
