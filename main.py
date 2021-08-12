import arcade
from views.death_view import DeathView
from views.start_view import StartView
from views.game_view import GameView

WIDTH = 1200
HEIGHT = 800
TITLE = 'The Game'


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title:str):
        super().__init__(width = width, height = height, title = title)
        self.game_view = GameView()
        start_view = StartView()
        self.death_view= DeathView()
        self.show_view(start_view)
        


window = GameWindow(WIDTH, HEIGHT, TITLE)
arcade.run()