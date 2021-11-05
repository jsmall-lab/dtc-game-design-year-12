import arcade

# window sizes
WIDTH = 1200
HEIGHT = 800


class StartView(arcade.View):
    """shown when game is first started"""

    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)
        self.start_song = arcade.load_sound("assets/sounds/start_song.wav")
        self.song = arcade.play_sound(self.start_song, looping=True)

    def on_draw(self):
        """draws text for view"""
        arcade.start_render()
        arcade.draw_text(
            "The Journey for The Snake Eye Gem",
            WIDTH / 2,
            HEIGHT / 2,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press Enter to Start",
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
            self.window.show_view(self.window.story_view)
            arcade.stop_sound(self.song)
