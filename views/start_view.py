import arcade

WIDTH = 1200
HEIGHT = 800

class StartView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.AERO_BLUE)
        arcade.set_viewport(0, WIDTH -1, 0, HEIGHT -1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Start Screen", WIDTH / 2, HEIGHT / 2
        , arcade.color.WHITE, font_size=50, anchor_x="center")
        
        arcade.draw_text("Click to Start", WIDTH / 2, HEIGHT / 2 - 75
        , arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.finish_render()


