import arcade
from arcade.color import BLACK

WIDTH = 1200
HEIGHT = 800


class ControlsView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()


        arcade.draw_text(
            " CONTROLS \n \n UP ARROW = JUMP \n LEFT ARROW = MOVE LEFT \n RIGHT ARROW = MOVE RIGHT \n SPACE = SHOOT",
            WIDTH / 2,  
            HEIGHT - 300,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ESC to go back to Pause",
            400,
            200,
            arcade.color.BLACK,
            font_size=40
                    )

        arcade.finish_render()
        
    def on_key_press(self, key, _modifiers):
        """If the user presses the mouse button, start the game."""
        #if key == arcade.key.ENTER:
