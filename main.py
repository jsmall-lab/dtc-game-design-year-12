import arcade
from views.death_view import DeathView
from views.start_view import StartView
from views.game_view import GameView
from views.level_won_view import LevelWon
from views.game_won_view import GameWon


WIDTH = 1200
HEIGHT = 800
TITLE = 'The Game'


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title:str):
        super().__init__(width = width, height = height, title = title)
        self.game_view = GameView()
        self.start_view = StartView()
        self.death_view= DeathView()
        self.level_won = LevelWon()
        self.game_won = GameWon()
        self.show_view(self.start_view)
        


window = GameWindow(WIDTH, HEIGHT, TITLE)
arcade.run()