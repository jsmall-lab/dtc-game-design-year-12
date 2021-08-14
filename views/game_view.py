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

BULLET_SPEED = 18
BULLET_SCAILING = 0.08

TOTAL_LEVELS = 3
MAX_PLAYER_HEALTH = 150
HEALTH_BAR_WIDTH = 200

MAX_ENEMY_HEALTH = 100
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

class Enemy1(arcade.Sprite):
    def __init__(self):
        super().__init__()
        
        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        # 0 - PLAYER_FRAMES
        self.virtual_frames = 0
        # 0 - 59

        self.touching_ramp = False

        #self.jump = False

        #self.jump_texture_pair = load_texture_pair("./assets/sprites_for_game/main_character/main_character_jump.png")

        self.idle = False

        self.idle_texture_pair = load_texture_pair("./assets/sprites_for_game/enemies/enemy1/enemy_idle.png")

        
        self.walk_textures: typing.List[typing.List[arcade.Texture]] = []

        #if self.jump == False:
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(f"./assets/sprites_for_game/enemies/enemy1/enemy{i}.png")
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

       # if self.change_y > 0:
            #self.texture = self.jump_texture_pair[self.character_face_direction]
           # self.jump = True
           # return
        
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
        self.enemy_list = None
        self.player_physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.lives = 3
        self.player_health = MAX_PLAYER_HEALTH
        self.enemiy_health = MAX_ENEMY_HEALTH
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.marker_x = None
        self.current_level = 1
        self.enemy_list = None
        self.time_since_last_firing = 0.0
        self.time_between_firing = 1.5

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
            self.window.show_view(self.window.game_won)
            self.current_level = 1
        else:
            self.window.show_view(self.window.level_won)
            self.current_level += 1
            self.setup()
  
    def enemiy_pos(self):
        if self.current_level == 1:
            enemy1 = Enemy1()
            enemy1.center_x = 8300
            enemy1.center_y = 448
            enemy1.change_x = 2
            enemy1.boundary_right = 8664
            enemy1.boundary_left = 7830
            enemy1.change_x = 2
            self.enemy_list.append(enemy1)

            enemy2 = Enemy1()
            enemy2.center_x = 10400
            enemy2.center_y = 1280
            enemy2.change_x = 2
            enemy2.boundary_right = 10953
            enemy2.boundary_left = 10373
            self.enemy_list.append(enemy2)

            enemy3 = Enemy1()
            enemy3.center_x = 16400
            enemy3.center_y = 512
            enemy3.change_x = 2
            enemy3.boundary_right = 17030
            enemy3.boundary_left = 16020
            self.enemy_list.append(enemy3)

    def setup(self):
        
            
        # main player
        self.player = PlayerCharacter()
        self.player.center_x = 50
        self.player.center_y = 500
        self.view_left = 0
        self.view_bottom = 0

        self.enemy_list = arcade.SpriteList()
        
         # bullet sprite
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.load_map()
        self.player_physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list)
        
        self.enemiy_pos()

    def player_health_bar(self):
        health_width = HEALTH_BAR_WIDTH * (self.player_health/MAX_PLAYER_HEALTH)

        arcade.draw_text("HEALTH", self.view_left + 100, self.view_bottom + (HEIGHT - 100), arcade.color.BLACK, 20)
        arcade.draw_rectangle_filled(self.view_left + 300, self.view_bottom + (HEIGHT - 85), width=health_width, height=20, color=arcade.color.RED)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player.draw()
        self.enemy_list.draw()
        arcade.draw_text(str(self.lives), self.view_left + 30 , self.view_bottom + (HEIGHT -150) , arcade.color.BLACK, 70)
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.player_health_bar()

    def death(self):
        self.window.show_view(self.window.death_view)

    def update(self, delta_time):
        self.enemy_list.update()
        self.player.update()
        self.player.update_animation()
        #print(self.player.center_x, self.player.center_y)
        self.enemy_list.update()
        self.enemy_list.update_animation()
        self.time_since_last_firing += delta_time
        for enemy in self.enemy_list:
            if arcade.check_for_collision_with_list(enemy, self.wall_list) == True :
                enemy.change_x *= -1
            if enemy.center_x < enemy.boundary_left or enemy.center_x > enemy.boundary_right:
                enemy.change_x *= -1
            if self.player.center_x <= enemy.boundary_right and self.player.center_x >= enemy.boundary_left:
                if self.player.center_x > enemy.center_x:
                    enemy.change_x = 2
                if self.player.center_x < enemy.center_x:
                    enemy.change_x = -2
                if self.time_since_last_firing >= self.time_between_firing:
                   
                    if enemy.character_face_direction == LEFT_FACING:
                        bullet = arcade.Sprite('assets/consumables/Bullet-1.png.png', BULLET_SCAILING, flipped_horizontally= True)                
                        bullet.change_x = -BULLET_SPEED
                        bullet.center_x = enemy.center_x - 45
                        bullet.center_y = enemy.center_y
                        self.time_since_last_firing = 0
                    else:
                        bullet = arcade.Sprite('assets/consumables/Bullet-1.png.png', BULLET_SCAILING)
                        bullet.change_x = BULLET_SPEED
                        bullet.center_x = enemy.center_x + 45
                        bullet.center_y = enemy.center_y
                        self.time_since_last_firing = 0
                        
                    self.enemy_bullet_list.append(bullet)
        
        for bullet in self.bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            for b in touching:
                bullet.kill()
            
            for enemy in touching:
                self.enemiy_health -= 25

                if self.enemiy_health == 0:
                    enemy.kill()
                    self.enemiy_health = MAX_ENEMY_HEALTH

        

        for bullet in self.enemy_bullet_list:
            touching = arcade.check_for_collision(bullet, self.player)
            if touching == True:
                bullet.kill()
                self.player_health -= 25

        for bullet in self.enemy_bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.wall_list)
            for b in touching:
                bullet.kill()

        self.enemy_bullet_list.update()            

                #if arcade.check_for_collision(enemy, self.player) == True:
                    #exit()


        self.player_physics_engine.update()
            
       

        changed = False

        self.bullet_list.update()

        for bullet in self.bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.wall_list)
            for b in touching:
                bullet.kill()
  
            if bullet.center_x > self.player.center_x + WIDTH:
                bullet.kill()
            if bullet.center_x < self.player.center_x - WIDTH:
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
        
        if self.player_health == 0:
            self.death()
            self.setup()
            self.lives -= 1

        if self.player.center_y < - 1100:
            self.death()
            self.setup()
            self.lives -= 1
           
                # character live counter
        if self.lives == 0:
            exit()
        
        if self.player.center_x > self.marker_x:
            self.progress_level()
            
   
            
        

    def on_key_press(self, key, modifiers):
        # user input
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        if key == arcade.key.UP and self.player_physics_engine.can_jump(y_distance=5):
            self.player.change_y = JUMP_SPEED
        if key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
        # first bullet when space bar is pressed 
        if self.player.jump == False: 
            if key == arcade.key.SPACE:   
                if self.player.character_face_direction == LEFT_FACING:
                    bullet = arcade.Sprite('assets/consumables/Bullet-1.png.png', BULLET_SCAILING, flipped_horizontally= True)                
                    bullet.change_x = -BULLET_SPEED
                    bullet.center_x = self.player.center_x - 45
                    bullet.center_y = self.player.center_y
                else:
                    bullet = arcade.Sprite('assets/consumables/Bullet-1.png.png', BULLET_SCAILING)
                    bullet.change_x = BULLET_SPEED
                    bullet.center_x = self.player.center_x + 45
                    bullet.center_y = self.player.center_y
                self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
   

        



