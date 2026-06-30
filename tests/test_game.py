# Enhetstester för spelet Fruit Loop.
# Kör testerna med: pytest tests/
# (V3: TDD – testa funktioner med pytest)

import pytest
from src.grid import Grid
from src.player import Player
from src import pickups
from src.game import (
    GameState, handle_move, handle_jump,
    _pickup_fruit, _pickup_trap, _pickup_chest,
    _pickup_key, _pickup_exit,
)


def make_state():
    """Skapar ett nytt GameState för testning."""
    return GameState()


class TestPlayer:
    def test_startposition_nara_mitten(self):
        """Spelaren ska börja nära mitten av spelplanen. (V1-A)"""
        state = make_state()
        assert state.player.pos_x == Grid.width // 2
        assert state.player.pos_y == Grid.height // 2

    def test_move_hoger(self):
        """Spelaren ska kunna flytta sig åt höger."""
        p = Player(5, 5)
        p.move(1, 0)
        assert p.pos_x == 6 and p.pos_y == 5

    def test_move_upp(self):
        """Spelaren ska kunna flytta sig uppåt."""
        p = Player(5, 5)
        p.move(0, -1)
        assert p.pos_x == 5 and p.pos_y == 4

    def test_can_move_blockeras_av_yttervagg(self):
        """Spelaren ska inte kunna gå igenom ytterväggen. (V1-C)"""
        g = Grid()
        g.make_walls()
        p = Player(1, 5)
        g.set_player(p)
        assert p.can_move(-1, 0, g) is False

    def test_can_move_tillaten_pa_tom_ruta(self):
        """Spelaren ska kunna gå till en tom ruta."""
        g = Grid()
        g.make_walls()
        p = Player(5, 6)
        g.set_player(p)
        assert p.can_move(1, 0, g) is True

    def test_can_move_blockeras_av_innervagg(self):
        """Spelaren ska inte kunna gå igenom en inner-vägg. (V1-C, V1-H)"""
        g = Grid()
        g.make_walls()
        p = Player(5, 5)
        g.set_player(p)
        # Inner-vägg på rad 4 – spelaren vid y=5 kan inte gå upp
        assert p.can_move(0, -1, g) is False

    def test_spade_tar_bort_vagg(self):
        """Spaden ska ta bort en vägg och förbrukas. (V2: Spade)"""
        g = Grid()
        g.make_walls()
        p = Player(1, 6)
        g.set_player(p)
        p.has_spade = True
        result = p.can_move(-1, 0, g)
        assert result is True
        assert p.has_spade is False
        assert g.get(0, 6) == g.empty


class TestPickups:
    def test_item_varde_ar_20(self):
        """Alla startfrukter ska vara värda 20 poäng. (V1-D)"""
        for item in pickups.pickups:
            assert item.value == 20

    def test_trap_symbol(self):
        """Trap ska ha symbolet X."""
        assert str(pickups.Trap()) == "X"

    def test_spade_symbol(self):
        """Spade ska ha symbolet P."""
        assert str(pickups.Spade()) == "P"

    def test_randomize_placerar_alla_frukter(self):
        """randomize() ska placera alla startfrukter på kartan."""
        g = Grid()
        p = Player(18, 6)
        g.set_player(p)
        g.make_walls()
        pickups.randomize(g)
        count = sum(
            1 for y in range(g.height) for x in range(g.width)
            if isinstance(g.get(x, y), pickups.Item)
        )
        assert count == len(pickups.pickups)

    def test_spawn_new_fruit_skapar_item(self):
        """spawn_new_fruit() ska skapa ett nytt Item på kartan. (V2: Bördig jord)"""
        g = Grid()
        p = Player(18, 6)
        g.set_player(p)
        g.make_walls()
        fruit = pickups.spawn_new_fruit(g)
        assert isinstance(fruit, pickups.Item)


class TestGameLogic:
    def test_score_minskar_per_steg_efter_grace(self):
        """Poängen ska minska med 1 per steg efter grace period. (V1-G)"""
        state = make_state()
        state.moves_since_pickup = 10
        score_before = state.score
        handle_move(1, 0, state)
        assert state.score == score_before - 1

    def test_grace_period_inga_avdrag(self):
        """Inga poängavdrag inom grace period. (V3: Grace period)"""
        state = make_state()
        state.moves_since_pickup = 0
        score_before = state.score
        handle_move(1, 0, state)
        assert state.score == score_before

    def test_pickup_fruit_okar_score(self):
        """Att plocka upp en frukt ska öka poängen med 20. (V1-D)"""
        state = make_state()
        item = pickups.Item("test_apple", value=20)
        score_before = state.score
        _pickup_fruit(item, state)
        assert state.score == score_before + 20

    def test_pickup_fruit_laggs_i_inventory(self):
        """Uppplockad frukt ska hamna i inventory. (V1-E)"""
        state = make_state()
        item = pickups.Item("test_cherry")
        _pickup_fruit(item, state)
        assert item in state.inventory

    def test_pickup_trap_minskar_score(self):
        """Att gå på en fälla ska minska poängen med 10. (V2: Fällor)"""
        state = make_state()
        score_before = state.score
        _pickup_trap(state)
        assert state.score == score_before - 10

    def test_pickup_key_okar_nyckelraknare(self):
        """Att plocka upp en nyckel ska öka nyckelräknaren. (V2: Nycklar)"""
        state = make_state()
        _pickup_key(state)
        assert state.keys_in_inventory == 1

    def test_pickup_chest_utan_nyckel(self):
        """Kista utan nyckel ska inte ge poäng. (V2: Kistor)"""
        state = make_state()
        state.keys_in_inventory = 0
        score_before = state.score
        _pickup_chest(state)
        assert state.score == score_before

    def test_pickup_chest_med_nyckel(self):
        """Kista med nyckel ska ge 100 poäng och förbruka nyckeln. (V2: Kistor)"""
        state = make_state()
        state.keys_in_inventory = 1
        score_before = state.score
        _pickup_chest(state)
        assert state.score == score_before + 100
        assert state.keys_in_inventory == 0

    def test_exit_innan_alla_frukter(self):
        """Exit ska inte avsluta spelet förrän alla frukter plockats. (V2: Exit)"""
        state = make_state()
        state.items_collected = 0
        assert _pickup_exit(state) is False

    def test_exit_efter_alla_frukter(self):
        """Exit ska avsluta spelet när alla frukter är plockade. (V2: Exit)"""
        state = make_state()
        state.items_collected = pickups.original_pickup_count
        assert _pickup_exit(state) is True

    def test_jump_flyttar_tva_steg(self):
        """Jump ska flytta spelaren två steg. (V2: Jump)"""
        state = make_state()
        start_x = state.player.pos_x
        handle_jump(-1, 0, state)
        assert state.player.pos_x == start_x - 2
