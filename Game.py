import arcade

WIDTH = 1900
HEIGHT = 1000
TITLE = 'The Game'

MOVEMENT_SPEED = 5


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.player = None

    def setup(self):
        self.player = arcade.Sprite('assets/sprites_for_game/character.png-1.png.png', 2)
        self.player.center_x = 500
        self.player.center_y = 500
    
    def on_draw(self):
        arcade.start_render()
        self.player.draw()
    
    def update(self, delta_time):
        self.player.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        if key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0


game = Game()
game.setup()
arcade.run()