import arcade
# Window, Width, Height, an Title
WIDTH = 1900
HEIGHT = 1000
TITLE = 'The Game'
#Movement speed and jump speed for user.main character
MOVEMENT_SPEED = 5
JUMP_SPEED = 10

#this is distance between main character and window boarder
VIEWPORT_MARGIN = 400

#speed of bullet fied from gun and the scailing for bullet sprite
BULLET_SPEED = 10
BULLET_SCAILING = 0.08

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.player = None
        self.wall_list: arcade.SpriteList
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.lives = 3
        self.bullet_list = None
    
    def load_map(self):
        platforms_layername = "Tile Layer 1"
        level1 = arcade.tilemap.read_tmx("assets/maps/level1_map.tmx")
        self.wall_list = arcade.tilemap.process_layer(map_object= level1, layer_name = platforms_layername, use_spatial_hash = True, scaling = 0.5)


    def setup(self):
        # main player
        self.player = arcade.Sprite('assets/sprites_for_game/character.png-1.png.png', 2)
        self.player.center_x = 50
        self.player.center_y = 500
        self.view_left = 0
        self.view_bottom = 0

        # bullet sprite
        self.bullet_list = arcade.SpriteList()
        self.load_map()
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list)
        


    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player.draw()
        arcade.draw_text(str(self.lives), 100 , 900 , arcade.color.BLACK, 70)
        self.bullet_list.draw()

    def update(self, delta_time):
        self.player.update()
        self.physics_engine.update()
        changed = False
        self.bullet_list.update()

        # scrolling for main character
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True
        
        right_boundary = self.view_left + WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + HEIGHT - VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary -self.player.bottom
            changed = True

        if self.view_left < 0:
            self.view_left = 0
            
        if changed:
            arcade.set_viewport(self.view_left,
                                WIDTH + self.view_left,
                                self.view_bottom,
                                HEIGHT + self.view_bottom)

        if self.view_left < 0:
            self.view_left = 0
        
        if self.player.center_y < - 500:
            self.setup()
            self.lives -= 1
        # character live counter
        if self.lives == 0:
            exit()

    def on_key_press(self, key, modifiers):
        # user input
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP and self.physics_engine.can_jump(y_distance=5):
            self.player.change_y = JUMP_SPEED
        if key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        # firs bullet when space bar is pressed 
        if key == arcade.key.SPACE:   
            bullet = arcade.Sprite('assets/sprites_for_game/Bullet-1.png.png', BULLET_SCAILING)
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y
            bullet.change_x = BULLET_SPEED
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
   


game = Game()
game.setup()
arcade.run()