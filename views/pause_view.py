import arcade

# window sizes
WIDTH = 1200
HEIGHT = 800


class Pause(arcade.View):
    """view is shown when game is paused"""

    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

    def on_draw(self):
        """draws text for view"""
        arcade.start_render()
        arcade.draw_text(
            "Paused",
            WIDTH / 2,
            HEIGHT / 2,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press ESC to resume",
            WIDTH / 2,
            HEIGHT / 2 - 75,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press ENTER to go to Controls",
            WIDTH / 2,
            HEIGHT / 2 - 100,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
        )
        arcade.finish_render()

    def on_key_press(self, key, modifiers: int):
        """runs when keys are pressed"""
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)
        if key == arcade.key.ENTER:
            self.window.show_view(self.window.controls_view)
