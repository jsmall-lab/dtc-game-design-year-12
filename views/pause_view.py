import arcade

WIDTH = 1200
HEIGHT = 800


class Pause(arcade.View):
      

    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH -1, 0, HEIGHT -1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Paused", WIDTH / 2, HEIGHT / 2, arcade.color.BLACK, font_size=50, anchor_x="center")
        
        arcade.draw_text("Press ESC to resume", WIDTH / 2, HEIGHT / 2 - 75, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.finish_render()
    
    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)
