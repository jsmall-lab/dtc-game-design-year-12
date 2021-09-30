import arcade

WIDTH = 1200
HEIGHT = 800


class LevelWon(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

    def on_draw(self):
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
            "Click to play Next Level",
            WIDTH / 2,
            HEIGHT / 2 - 75,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
        )
        arcade.finish_render()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """If the user presses the mouse button, start the game."""
        game_view = self.window.game_view
        game_view.setup()
        self.window.show_view(game_view)
