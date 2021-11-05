import arcade
from views.death_view import DeathView
from views.game_failed_view import GameFailed
from views.game_view import GameView
from views.game_won_view import GameWon
from views.level_won_view import LevelWon
from views.pause_view import Pause
from views.start_view import StartView
from views.story_view import StoryView
from views.controls_view import ControlsView

# window sizes and title
WIDTH = 1200
HEIGHT = 800
TITLE = "The Quest For The Snake Eye Gem"


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str):
        """class brings all views together to run game"""
        super().__init__(width=width, height=height, title=title)
        """sets variables"""
        self.game_view = GameView()
        self.start_view = StartView()
        self.death_view = DeathView()
        self.level_won = LevelWon()
        self.game_won = GameWon()
        self.game_failed = GameFailed()
        self.pause_view = Pause()
        self.story_view = StoryView()
        self.controls_view = ControlsView()
        self.show_view(self.start_view)


window = GameWindow(WIDTH, HEIGHT, TITLE)
arcade.run()
