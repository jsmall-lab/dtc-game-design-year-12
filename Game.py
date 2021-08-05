import arcade
import typing

WIDTH = 1200
HEIGHT = 700
TITLE = 'The Game'

PLAYER_MOVEMENT_SPEED = 5
JUMP_SPEED = 10
VIEWPORT_MARGIN = 400

RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_FRAMES = 3
PLAYER_FRAMES_PER_TEXTURE = 6

BULLET_SPEED = 25
BULLET_SCAILING = 0.08

def load_texture_pair(filename: str) -> typing.List[arcade.Texture]:
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class PlayerCharacter (arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.change_x = 0
        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        # 0 - PLAYER_FRAMES
        self.virtual_frames = 0
        # 0 - 59

        self.idle = False

        self.idle_texture_pair = load_texture_pair("./assets/sprites_for_game/main_character_idle-1.png.png")


        self.walk_textures: typing.List[typing.List[arcade.texture]] = []
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(f"./assets/sprites_for_game/main character/main_character{i}.png")
            self.walk_textures.append(texture)
        
        self.texture = self.idle_texture_pair[0]


    def update_animation(self, delta_time:float = 1/60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        

        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.idle = True
            return

        
        self.idle = False
        self.virtual_frames += 1
        if self.virtual_frames > PLAYER_FRAMES*PLAYER_FRAMES_PER_TEXTURE -1:
            self.virtual_frames = 0
            self.cur_texture = 0
        if (self.virtual_frames + 1) % PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_frames // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


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
        self.player = PlayerCharacter()
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
        self.player.update_animation()
        self.physics_engine.update()
        changed = False

        self.bullet_list.update()
        for bullet in self.bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.wall_list)
            for b in touching:
                bullet.kill()
#TODO kill bullets off the edge of the screen             

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
        
        if self.player.center_y < - 1100:
            self.setup()
            self.lives -= 1
        # character live counter
        if self.lives == 0:
            exit()

    def on_key_press(self, key, modifiers):
        # user input
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        if key == arcade.key.UP and self.physics_engine.can_jump(y_distance=5):
            self.player.change_y = JUMP_SPEED
        if key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
        # first bullet when space bar is pressed 
        if key == arcade.key.SPACE:   
            bullet = arcade.Sprite('assets/sprites_for_game/Bullet-1.png.png', BULLET_SCAILING)
            bullet.center_x = self.player.center_x + 40
            bullet.center_y = self.player.center_y
            if self.player.change_x < 0:                
                bullet.change_x = -BULLET_SPEED
            else:
                bullet.change_x = BULLET_SPEED
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
   


game = Game()
game.setup()
arcade.run()