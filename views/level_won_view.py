import arcade

# window sizes
WIDTH = 1200
HEIGHT = 800


class LevelWon(arcade.View):
    """view is shown when level is won"""

    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)
        game = self.window.game_view
        game.setup()

    def on_draw(self):
        """draws text for view"""
        arcade.start_render()
        arcade.draw_text(
            "Congratulations \nYou Have Finsished the level",
            WIDTH / 2,
            HEIGHT / 2,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press Enter to play Next Level",
            WIDTH / 2,
            HEIGHT / 2 - 75,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
        )
        arcade.finish_render()

    def on_key_press(self, key, _modifiers):
        """runs when key is pressed"""
        if key == arcade.key.ENTER:
            self.window.show_view(self.window.game_view)
