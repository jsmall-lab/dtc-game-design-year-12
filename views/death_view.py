import arcade

# window sizes
WIDTH = 1200
HEIGHT = 800


class DeathView(arcade.View):
    """view shown when dead"""

    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)
        game = self.window.game_view
        game.setup()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "You Have Died",
            WIDTH / 2,
            HEIGHT / 2,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press Enter to Try Again",
            WIDTH / 2,
            HEIGHT / 2 - 75,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
        )
        arcade.finish_render()

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.ENTER:
            self.window.show_view(self.window.game_view)
