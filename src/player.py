# Denna fil innehåller klassen Player.


class Player:
    marker = "@"

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        # V2: Spade – håller reda på om spelaren har en spade
        self.has_spade = False

    def move(self, dx, dy):
        """Flyttar spelaren.
        dx = horisontell förflyttning, från vänster till höger
        dy = vertikal förflyttning, uppifrån och ned"""
        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, dx, dy, grid):
        """Returnerar True om spelaren kan flytta sig i angiven riktning.
        Kontrollerar att nästa ruta inte är en vägg. (V1-C)
        Om spelaren har en spade tas väggen bort istället. (V2: Spade)"""
        next_x = self.pos_x + dx
        next_y = self.pos_y + dy
        next_cell = grid.get(next_x, next_y)

        # V2: Spade – om spelaren har en spade och träffar en vägg, ta bort väggen
        if next_cell == grid.wall and self.has_spade:
            grid.clear(next_x, next_y)  # Väggen försvinner
            self.has_spade = False       # Spaden är förbrukad
            print("You used the spade and removed a wall!")
            return True

        # Annars: kan bara gå om nästa ruta inte är en vägg
        return next_cell != grid.wall
