import arcade
from arcade.color import BLACK

# window sizes
WIDTH = 1200
HEIGHT = 800


class StoryView(arcade.View):
    """view is shown when game begins"""

    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)
        game_view = self.window.game_view
        game_view.setup()

    def on_draw(self):
        """draws text for view"""
        arcade.start_render()
        story_string = (
            "The United States Army\n This Confidentail Information\n"
            "Dear H.Gatsby\n"
            "We here by order you to journey to peru to recover the mistical\n"
            "Snake Eye Gem.\n"
            "This is the upmost importance for Cornal Gebidia is in\n"
            "search for this Gem aswell and from recent intel,\n"
            "We believe he on his way to the temple where the gem is kept.\n"
            "if he gets his hands on it, it could turn the war in his favour\n"
            "for it is rumured that the gem has supernatural powers of unknown origin\n"
            "You are the only one.\n"
            "15/10/1942"
        )
        arcade.draw_text(
            story_string,
            10,
            428,
            arcade.color.BLACK,
            font_size=30,
        )

        arcade.draw_text(
            " CONTROLS \n UP ARROW = JUMP \n LEFT ARROW = MOVE LEFT \n RIGHT ARROW = MOVE RIGHT \n SPACE = SHOOT",
            10,
            250,
            arcade.color.BLACK,
            font_size=30,
        )

        arcade.draw_text(
            "Press ENTER to start the Game", 400, 200, arcade.color.BLACK, font_size=40
        )

        arcade.finish_render()

    def on_key_press(self, key, _modifiers):
        """runs when key is pressed"""
        if key == arcade.key.ENTER:
            self.window.show_view(self.window.game_view)
