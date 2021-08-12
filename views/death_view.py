import arcade

WIDTH = 1200
HEIGHT = 800


class DeathView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH -1, 0, HEIGHT -1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("You Have Died", WIDTH / 2, HEIGHT / 2, arcade.color.BLACK, font_size=50, anchor_x="center")
        
        arcade.draw_text("Click to Try Again", WIDTH / 2, HEIGHT / 2 - 75, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.finish_render()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
           game_view = self.window.game_view
           self.window.show_view(game_view)
           game_view.setup()

