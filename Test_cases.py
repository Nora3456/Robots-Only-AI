import pytest
from unittest.mock import patch
from ted_game import Game, Player, Enemy


@pytest.fixture
def setup_game():
    """Fixture to set up a fresh game and player before each test."""
    game = Game()
    game.player = Player("Tester", "engineer")
    return game


# --------------------------------------------------------------
# 1. Invalid command handling
# --------------------------------------------------------------
@patch("builtins.input", side_effect=["invalid", "quit"])
def test_invalid_command_handling(mock_input, setup_game, capsys):
    """Ensure the game handles invalid player inputs gracefully."""
    setup_game.running = True
    setup_game.start()
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out


# --------------------------------------------------------------
# 2. Empty inventory usage
# --------------------------------------------------------------
def test_empty_inventory_does_not_crash(setup_game, capsys):
    """Ensure using an empty inventory prints a message, not an error."""
    setup_game.player.inventory.clear()
    setup_game.use_item()
    captured = capsys.readouterr()
    assert "empty" in captured.out.lower()


# --------------------------------------------------------------
# 3. Player death scenario
# --------------------------------------------------------------
def test_player_death_does_not_crash(setup_game):
    """Ensure combat with overpowered enemy doesn’t crash the game."""
    enemy = Enemy("Killer Bot", hp=50, atk=999, armor=0)
    setup_game.player.hp = 5
    try:
        setup_game.combat(enemy)
    except Exception as e:
        pytest.fail(f"Combat raised an unexpected exception: {e}")


# --------------------------------------------------------------
# 4. Invalid item usage
# --------------------------------------------------------------
@patch("builtins.input", return_value="banana")
def test_invalid_item_usage(mock_input, setup_game, capsys):
    """Ensure trying to use a non-existent item doesn’t break the game."""
    setup_game.player.inventory = {"medkit": 1}
    setup_game.use_item()
    captured = capsys.readouterr()
    assert "can’t use" in captured.out.lower() or "can't use" in captured.out.lower()


# --------------------------------------------------------------
# 5. Travel at end of game
# --------------------------------------------------------------
def test_travel_at_end_of_game_does_not_crash(setup_game, capsys):
    """Ensure traveling from final area is handled gracefully."""
    setup_game.player.location = "AI Research Facility Lobby"
    result = setup_game.travel()
    captured = capsys.readouterr()
    assert not result
    assert "end of your journey" in captured.out.lower()


# --------------------------------------------------------------
# 6. Attempting to collect page where none exist
# --------------------------------------------------------------
def test_take_page_when_none_available(setup_game, capsys):
    """Ensure taking a page from an empty area doesn’t break the game."""
    loc = setup_game.player.location
    setup_game.pages[loc] = []
    setup_game.take_page()
    captured = capsys.readouterr()
    assert "no pages" in captured.out.lower()


# --------------------------------------------------------------
# 7. Using item when inventory exists but invalid input
# --------------------------------------------------------------
@patch("builtins.input", return_value="")
def test_use_item_with_empty_input(mock_input, setup_game, capsys):
    """Ensure blank item choice does not break gameplay."""
    setup_game.player.inventory = {"medkit": 1}
    setup_game.use_item()
    captured = capsys.readouterr()
    assert "can’t use" in captured.out.lower() or "can't use" in captured.out.lower()


# --------------------------------------------------------------
# 8. Player healing boundary (not exceeding max HP)
# --------------------------------------------------------------
def test_healing_does_not_exceed_max_hp(setup_game):
    """Ensure healing does not push HP beyond maximum."""
    setup_game.player.hp = setup_game.player.max_hp - 5
    setup_game.player.heal(50)
    assert setup_game.player.hp == setup_game.player.max_hp


# --------------------------------------------------------------
# 9. Game start and quit command handling
# --------------------------------------------------------------
@patch("builtins.input", side_effect=["1", "quit"])
def test_quit_command_during_game(mock_input, setup_game, capsys):
    """Ensure quitting the game works without errors."""
    setup_game.create_character()
    setup_game.running = True
    setup_game.start()
    captured = capsys.readouterr()
    assert "goodbye" in captured.out.lower() or "give up" in captured.out.lower()
