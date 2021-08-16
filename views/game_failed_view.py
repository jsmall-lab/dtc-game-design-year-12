import arcade

WIDTH = 1200
HEIGHT = 800


class GameFailed(arcade.View):
      

    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH -1, 0, HEIGHT -1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("YOU FAILED \n You Were Unable To Retreive the gem", WIDTH / 2, HEIGHT / 2, arcade.color.BLACK, font_size=50, anchor_x="center")
        
        arcade.draw_text("Click to Start Game Again", WIDTH / 2, HEIGHT / 2 - 75, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.finish_render()
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        restart = self.window.start_view
        self.window.show_view(restart)