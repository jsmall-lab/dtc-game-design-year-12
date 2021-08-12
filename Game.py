import arcade
import typing

         
WIDTH = 1200
HEIGHT = 800
TITLE = 'The Game'

PLAYER_MOVEMENT_SPEED = 5
JUMP_SPEED = 11
VIEWPORT_MARGIN = 400

RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_FRAMES = 3
PLAYER_FRAMES_PER_TEXTURE = 6

BULLET_SPEED = 25
BULLET_SCAILING = 0.08

TOTAL_LEVELS = 3

def load_texture_pair(filename: str) -> typing.List[arcade.Texture]:
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.change_x = 0
        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        # 0 - PLAYER_FRAMES
        self.virtual_frames = 0
        # 0 - 59

        self.touching_ramp = False

        self.jump = False

        self.jump_texture_pair = load_texture_pair("./assets/sprites_for_game/main_character/main_character_jump.png")

        self.idle = False

        self.idle_texture_pair = load_texture_pair("./assets/sprites_for_game/main_character/main_character_idle-1.png.png")

        
        self.walk_textures: typing.List[typing.List[arcade.Texture]] = []

        if self.jump == False:
            for i in range(PLAYER_FRAMES):
                texture = load_texture_pair(f"./assets/sprites_for_game/main_character/main_character{i}.png")
                self.walk_textures.append(texture)
                
        self.texture = self.idle_texture_pair[0]


    def update_animation(self, delta_time:float = 1/60):
       
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
            
        
        if self.change_x == 0 or self.change_y < 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.idle = True
            return

        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            self.jump = True
            return
        
        self.jump = False

        self.idle = False
        self.virtual_frames += 1
        if self.virtual_frames > PLAYER_FRAMES*PLAYER_FRAMES_PER_TEXTURE -1:
            self.virtual_frames = 0
            self.cur_texture = 0
        if (self.virtual_frames + 1) % PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_frames // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.player = None
        self.wall_list: arcade.SpriteList
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.lives = 3
        self.bullet_list = None
        self.marker_x = None
        self.current_level =1

    def load_map(self):
        platforms_layername = "walls"
        next_level_marker_layername = "next_level_marker"
        level = arcade.tilemap.read_tmx(f"assets/maps/level{self.current_level}_map.tmx")
        self.wall_list = arcade.tilemap.process_layer(map_object= level, layer_name = platforms_layername, use_spatial_hash = True, scaling = 0.5)
        marker_list = arcade.tilemap.process_layer(map_object= level, layer_name = next_level_marker_layername, use_spatial_hash = True, scaling = 0.5)
        marker = marker_list[0]
        self.wall_list.append(marker)
        self.marker_x = marker.center_x

    def progress_level(self):
        if self.current_level == TOTAL_LEVELS:
            raise NotImplementedError()
        else:
            self.current_level += 1
            self.setup()

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
        arcade.draw_text(str(self.lives), self.view_left + 30 , self.view_bottom + (HEIGHT -150) , arcade.color.BLACK, 70)
        self.bullet_list.draw()
    def death(self):
        self.window.show_view(self.window.death_view)

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
  
            if bullet.center_x > self.player.center_x + WIDTH:
                bullet.kill()
                         

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
        
        
        if self.player.center_y <= - 1100:
            if self.lives > 0:
                self.lives -= 1
            if self.lives < 1:
                self.death
        
        if self.player.center_x > self.marker_x:
            self.progress_level()
            

        

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
        if self.player.jump == False: 
            if key == arcade.key.SPACE:   
                if self.player.character_face_direction == LEFT_FACING:
                    bullet = arcade.Sprite('assets/sprites_for_game/Bullet-1.png.png', BULLET_SCAILING, flipped_horizontally= True)                
                    bullet.change_x = -BULLET_SPEED
                    bullet.center_x = self.player.center_x - 45
                    bullet.center_y = self.player.center_y
                else:
                    bullet = arcade.Sprite('assets/sprites_for_game/Bullet-1.png.png', BULLET_SCAILING)
                    bullet.change_x = BULLET_SPEED
                    bullet.center_x = self.player.center_x + 45
                    bullet.center_y = self.player.center_y
                self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
   
class StartView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH -1, 0, HEIGHT -1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Start Screen", WIDTH / 2, HEIGHT / 2, arcade.color.BLACK, font_size=50, anchor_x="center")
        
        arcade.draw_text("Click to Start", WIDTH / 2, HEIGHT / 2 - 75, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.finish_render()
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = self.window.game_view
        game_view.setup()
        self.window.show_view(game_view)
        

class DeathView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.set_viewport(0, WIDTH -1, 0, HEIGHT -1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("You Have Died", WIDTH / 2, HEIGHT / 2, arcade.color.BLACK, font_size=50, anchor_x="center")
        
        arcade.draw_text("Click to Restart Map", WIDTH / 2, HEIGHT / 2 - 75, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.finish_render()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
           game_view = self.window.game_view
           self.window.show_view(game_view)
           game_view.setup()

class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title:str):
        super().__init__(width = width, height = height, title = title)
        self.game_view = GameView()
        start_view = StartView()
        self.death_view= DeathView()
        self.show_view(start_view)
        


window = GameWindow(WIDTH, HEIGHT, TITLE)
arcade.run()