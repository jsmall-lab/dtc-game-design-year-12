import arcade

WIDTH = 1900
HEIGHT = 1000
TITLE = 'The Game'

MOVEMENT_SPEED = 5
JUMP_SPEED = 10

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.player = None
        self.wall_list: arcade.SpriteList
        self.physics_engine = None
      
    def load_map(self):
        platforms_layername = "Tile Layer 1"
        level1 = arcade.tilemap.read_tmx("assets/maps/level1_map.tmx")
        self.wall_list = arcade.tilemap.process_layer(map_object= level1, layer_name = platforms_layername, use_spatial_hash = True, scaling = 0.5)

    def setup(self):
        self.player = arcade.Sprite('assets/sprites_for_game/character.png-1.png.png', 2)
        self.load_map()
        self.player.center_x = 500
        self.player.center_y = 500
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player.draw()
    
    def update(self, delta_time):
        self.player.update()
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP and self.physics_engine.can_jump(y_distance=5):
            self.player.change_y = JUMP_SPEED
        if key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
   


game = Game()
game.setup()
arcade.run()