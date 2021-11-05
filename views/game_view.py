import typing
import arcade

# window sizes
WIDTH = 1200
HEIGHT = 800
TITLE = "The Game"

# player contents
PLAYER_MOVEMENT_SPEED = 5
JUMP_SPEED = 11
TOTAL_LEVELS = 3
MAX_LIVES = 3
MAX_PLAYER_HEALTH = 180

# viewport size
VIEWPORT_MARGIN = 400

# animation contents for all sprites
RIGHT_FACING = 0
LEFT_FACING = 1
PLAYER_FRAMES = 3
PLAYER_FRAMES_PER_TEXTURE = 6

# bullets contents for enemy and player except bullet_amount(for player only)
BULLET_SPEED = 18
BULLET_SCAILING = 0.08
BULLET_DAMAGE = 20
BULLET_AMOUNT = 6

# inital size of player health bar
HEALTH_BAR_WIDTH = 200

# enemy contents
MAX_ENEMY_HEALTH = 100
ENEMY_MOVEMENT_SPEED = 2


def load_texture_pair(filename: str) -> typing.List[arcade.Texture]:
    """loads animation for all animated sprites"""
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class PlayerCharacter(arcade.Sprite):
    """class for loading player sprite and animations"""

    def __init__(self):
        super().__init__()
        """starts all player functions"""
        self.change_x = 0
        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        #  0 - PLAYER_FRAMES
        self.virtual_frames = 0
        #  0 - 59

        # loads jump sprite for player
        self.jump = False
        self.jump_texture_pair = load_texture_pair(
            "./assets/sprites_for_game/main_character/main_character_jump.png"
        )

        # loads idle sprite for player
        self.idle = False
        self.idle_texture_pair = load_texture_pair(
            "./assets/sprites_for_game/main_character/main_character_idle-1.png.png"
        )

        # loads walking animation for player sprite
        self.walk_textures: typing.List[typing.List[arcade.Texture]] = []
        if not self.jump:
            for i in range(PLAYER_FRAMES):
                texture = load_texture_pair(
                    f"./assets/sprites_for_game/main_character/main_character{i}.png"
                )
                self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60):
        """updates frame of player sprite"""
        # changes direction player sprite is facing
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # changes frame to idle player sprite
        if self.change_x == 0 or self.change_y < 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.idle = True
            return

        # changes frame to jumping player sprite
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            self.jump = True
            return
        self.jump = False

        # cycles player sprite through walking animation
        self.idle = False
        self.virtual_frames += 1
        if self.virtual_frames > PLAYER_FRAMES * PLAYER_FRAMES_PER_TEXTURE - 1:
            self.virtual_frames = 0
            self.cur_texture = 0
        if (self.virtual_frames + 1) % PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_frames // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][
                self.character_face_direction
            ]


class Enemy1(arcade.Sprite):
    def __init__(self, x, y, right_boundary, left_boundary, top_boundary, change_x):
        """class for loading enemy sprite and aniamtions"""
        super().__init__()
        """starts all enemy functions"""
        self.character_face_direction = RIGHT_FACING
        self.center_x = x
        self.center_y = y
        self.boundary_right = right_boundary
        self.boundary_left = left_boundary
        self.boundary_top = top_boundary
        self.change_x = change_x

        self.cur_texture = 0
        #  0 - PLAYER_FRAMES
        self.virtual_frames = 0
        #  0 - 59

        # loads idle frame for enemy
        self.idle = False
        self.idle_texture_pair = load_texture_pair(
            "./assets/sprites_for_game/enemies/enemy1/enemy_idle.png"
        )

        # loads walking animations for enemy sprite
        self.walk_textures: typing.List[typing.List[arcade.Texture]] = []
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(
                f"./assets/sprites_for_game/enemies/enemy1/enemy{i}.png"
            )
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60):
        """updates frame of enemy sprite"""
        # changes direction enemy sprite is facing
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # changes frame to idle for enemy
        if self.change_x == 0 or self.change_y < 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.idle = True
            return

        # cycles walking animations for enemy sprite
        self.idle = False
        self.virtual_frames += 1
        if self.virtual_frames > PLAYER_FRAMES * PLAYER_FRAMES_PER_TEXTURE - 1:
            self.virtual_frames = 0
            self.cur_texture = 0
        if (self.virtual_frames + 1) % PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_frames // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][
                self.character_face_direction
            ]


class Boss(arcade.Sprite):
    def __init__(self, x, y, right_boundary, left_boundary, top_bounary, change_x):
        """class for loading boos sprite and animations"""
        super().__init__()
        """starts all functions for boss sprite"""
        self.character_face_direction = RIGHT_FACING
        self.center_x = x
        self.center_y = y
        self.boundary_right = right_boundary
        self.boundary_left = left_boundary
        self.boundary_top = top_bounary
        self.change_x = change_x

        self.cur_texture = 0
        #  0 - PLAYER_FRAMES
        self.virtual_frames = 0
        #  0 - 59

        # loads idle frame for boss sprite
        self.idle = False
        self.idle_texture_pair = load_texture_pair(
            "./assets/sprites_for_game/enemies/boss/boss_idle.png"
        )

        # loads walking animations for boss sprite
        self.walk_textures: typing.List[typing.List[arcade.Texture]] = []
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(
                f"./assets/sprites_for_game/enemies/boss/boss{i}.png"
            )
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60):
        """updates frame of boss sprite"""
        # chanegs direction boss sprite is faceing
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # changes frame to idle for boss sprite
        if self.change_x == 0 or self.change_y < 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.idle = True
            return
        self.jump = False

        # cycles through walking aniamtions for boss sprite
        self.idle = False
        self.virtual_frames += 1
        if self.virtual_frames > PLAYER_FRAMES * PLAYER_FRAMES_PER_TEXTURE - 1:
            self.virtual_frames = 0
            self.cur_texture = 0
        if (self.virtual_frames + 1) % PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_frames // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][
                self.character_face_direction
            ]


class GameView(arcade.View):
    """view shown when playing game"""

    def __init__(self):
        """creates list and variables for game"""
        super().__init__()
        self.player = None
        self.wall_list: arcade.SpriteList
        self.enemy_list = None
        self.player_physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.lives = MAX_LIVES
        self.player_health = None
        self.enemiy_health = MAX_ENEMY_HEALTH
        self.bullet_list = None
        self.bullet_amount = None
        self.enemy_bullet_list = None
        self.marker_x = None
        self.current_level = 3
        self.enemy_list = None
        self.time_since_last_firing = 0.0
        self.time_between_firing = 0.9

    def load_map(self):
        """loads maps for game"""
        platforms_layername = "walls"
        next_level_marker_layername = "next_level_marker"
        health_pickup_layername = "health_pickup"
        bullet_pickup_layername = "bullet_pickup"
        level = arcade.tilemap.read_tmx(
            f"assets/maps/level{self.current_level}_map.tmx"
        )
        # creates walls for level
        self.wall_list = arcade.tilemap.process_layer(
            map_object=level,
            layer_name=platforms_layername,
            use_spatial_hash=True,
            scaling=0.5,
        )
        # creates markers so player can go to next level
        marker_list = arcade.tilemap.process_layer(
            map_object=level,
            layer_name=next_level_marker_layername,
            use_spatial_hash=True,
            scaling=0.5,
        )
        # creates health pickup for level
        self.health_pickup_list = arcade.tilemap.process_layer(
            map_object=level,
            layer_name=health_pickup_layername,
            use_spatial_hash=True,
            scaling=0.5,
        )
        # creates bullets pickup for level
        self.bullet_pickup_list = arcade.tilemap.process_layer(
            map_object=level,
            layer_name=bullet_pickup_layername,
            use_spatial_hash=True,
            scaling=0.5,
        )
        # if is is level 3 then it creates gem
        if self.current_level == 3:
            gem_layername = "gem"
            self.gem_pickup_list = arcade.tilemap.process_layer(
                map_object=level,
                layer_name=gem_layername,
                use_spatial_hash=True,
                scaling=0.5,
            )

        marker = marker_list[0]
        self.wall_list.append(marker)
        self.marker_x = marker.center_x

    def setup(self):
        """sets values to variables"""
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = PlayerCharacter()
        self.bullet_list = arcade.SpriteList()
        self.bullet_amount = BULLET_AMOUNT
        self.player_health = MAX_PLAYER_HEALTH
        self.load_map()
        self.player_physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list
        )

        self.player.center_x = 50
        self.player.center_y = 500

        self.view_left = 0
        self.view_bottom = 0

        if self.lives == 0:
            self.lives = MAX_LIVES

        # enemy setup for each level
        if self.current_level == 1:
            self.enemy_list.append(
                Enemy1(8300, 448, 8664, 7830, 600, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(10400, 1280, 10953, 10373, 1400, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(16400, 512, 17030, 16020, 600, ENEMY_MOVEMENT_SPEED)
            )

        if self.current_level == 2:
            self.enemy_list.append(
                Enemy1(3700, 384, 4100, 3640, 450, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(6300, 960, 6772, 5942, 1060, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(7400, 1792, 7640, 7006, 1890, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(6000, 2304, 7042, 6309, 2400, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(10000, 576, 10448, 9400, 670, ENEMY_MOVEMENT_SPEED)
            )

        if self.current_level == 3:
            self.enemy_list.append(
                Enemy1(1000, 514, 1220, 830, 610, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(3000, 512, 3474, 2964, 610, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(5000, 768, 5314, 4674, 860, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Enemy1(6500, 384, 6936, 6120, 480, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(Enemy1(6700, 384, 6936, 6120, 480, 2.2))
            self.enemy_list.append(
                Enemy1(8000, 1472, 8828, 7628, 1600, ENEMY_MOVEMENT_SPEED)
            )
            self.enemy_list.append(
                Boss(14000, 2944, 14512, 13300, 3044, ENEMY_MOVEMENT_SPEED)
            )

    def on_draw(self):
        """draws sprites for game"""
        arcade.start_render()

        self.wall_list.draw()
        self.player.draw()
        self.enemy_list.draw()
        self.health_pickup_list.draw()
        self.bullet_pickup_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()
        if self.current_level == 3:
            self.gem_pickup_list.draw()

        # draws item amount remaining and what amount is
        arcade.draw_text(
            "Bullets",
            self.view_left + 30,
            self.view_bottom + (HEIGHT - 200),
            arcade.color.BLACK,
            30,
        )
        arcade.draw_text(
            str(self.bullet_amount),
            self.view_left + 140,
            self.view_bottom + (HEIGHT - 200),
            arcade.color.BLACK,
            40,
        )
        arcade.draw_text(
            str(self.lives),
            self.view_left + 30,
            self.view_bottom + (HEIGHT - 150),
            arcade.color.BLACK,
            70,
        )
        health_width = HEALTH_BAR_WIDTH * (self.player_health / MAX_PLAYER_HEALTH)
        arcade.draw_text(
            "HEALTH",
            self.view_left + 100,
            self.view_bottom + (HEIGHT - 100),
            arcade.color.BLACK,
            20,
        )
        arcade.draw_rectangle_filled(
            self.view_left + 300,
            self.view_bottom + (HEIGHT - 85),
            width=health_width,
            height=20,
            color=arcade.color.RED,
        )

    def death(self):
        """runs when player dies"""
        self.window.show_view(self.window.death_view)

    def game_failed(self):
        """runs when player loses game"""
        self.window.show_view(self.window.game_failed)

    def update(self, delta_time: float):
        """updates frame of the game"""
        self.enemy_list.update()
        self.player.update()
        self.player.update_animation()
        self.enemy_list.update()
        self.enemy_list.update_animation()
        # updates variable that controls rate of enemy fire
        self.time_since_last_firing += delta_time
        # enemy shooting, and enemy chasing of player
        for enemy in self.enemy_list:
            if (
                enemy.center_x < enemy.boundary_left or
                enemy.center_x > enemy.boundary_right
            ):
                enemy.change_x *= -1
            if (
                self.player.center_x <= enemy.boundary_right and
                self.player.center_x >= enemy.boundary_left and
                self.player.center_y < enemy.boundary_top
            ):
                if self.player.center_x > enemy.center_x:
                    enemy.change_x = 2
                if self.player.center_x < enemy.center_x:
                    enemy.change_x = -2
                if self.time_since_last_firing >= self.time_between_firing:
                    if enemy.character_face_direction == LEFT_FACING:
                        bullet = arcade.Sprite(
                            "assets/consumables/Bullet-1.png.png",
                            BULLET_SCAILING,
                            flipped_horizontally=True,
                        )
                        bullet.change_x = -BULLET_SPEED
                        bullet.center_x = enemy.center_x - 45
                        bullet.center_y = enemy.center_y
                        self.time_since_last_firing = 0.0

                    else:
                        bullet = arcade.Sprite(
                            "assets/consumables/Bullet-1.png.png", BULLET_SCAILING
                        )
                        bullet.change_x = BULLET_SPEED
                        bullet.center_x = enemy.center_x + 45
                        bullet.center_y = enemy.center_y
                        self.time_since_last_firing = 0.0

                    self.enemy_bullet_list.append(bullet)
        # code that runs when bullet and enemy list is touching
        for bullet in self.bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for b in touching:
                bullet.kill()
            for enemy in touching:
                self.enemiy_health -= BULLET_DAMAGE
                if self.enemiy_health == 0:
                    enemy.kill()
                    self.enemiy_health = MAX_ENEMY_HEALTH

        # code that runs when enemy bullet and player sprite are touching
        for bullet in self.enemy_bullet_list:
            touching = arcade.check_for_collision(bullet, self.player)
            if touching:
                bullet.kill()
                self.player_health -= BULLET_DAMAGE

        # code that runs when bullet and wall_list are touching
        for bullet in self.enemy_bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.wall_list)
            for b in touching:
                bullet.kill()
            if bullet.center_x > self.player.center_x + WIDTH:
                bullet.kill()
            if bullet.center_x < self.player.center_x - WIDTH:
                bullet.kill()
        for bullet in self.bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.wall_list)
            for b in touching:
                bullet.kill()
            if bullet.center_x > self.player.center_x + WIDTH:
                bullet.kill()
            if bullet.center_x < self.player.center_x - WIDTH:
                bullet.kill()

        self.enemy_bullet_list.update()
        self.player_physics_engine.update()
        changed = False
        self.bullet_list.update()

        # code that runs when either health pickup, bullet pickup, or gem pickup are touching player sprite
        health_hit_list = arcade.check_for_collision_with_list(
            self.player, self.health_pickup_list
        )
        for health in health_hit_list:
            health.kill()
            self.player_health = MAX_PLAYER_HEALTH
        bullet_hit_list = arcade.check_for_collision_with_list(
            self.player, self.bullet_pickup_list
        )
        for bullet in bullet_hit_list:
            bullet.kill()
            self.bullet_amount += BULLET_AMOUNT
        # changes which part of window is shown
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
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True
        if self.view_left < 0:
            self.view_left = 0
        if changed:
            arcade.set_viewport(
                self.view_left,
                WIDTH + self.view_left,
                self.view_bottom,
                HEIGHT + self.view_bottom,
            )

        if self.player_health <= 0:
            self.death()
            self.lives -= 1

        # kills player when it falls too far below map
        if self.player.center_y < -800:
            self.death()
            self.lives -= 1

        if self.lives == 0:
            self.game_failed()
            self.current_level = 1

        # runs when player touches marker tile, progresses to next level
        if self.player.center_x > self.marker_x:
            self.current_level += 1
            self.window.show_view(self.window.level_won)
        # finishes game
        if self.current_level == 3:
            gem_hit = arcade.check_for_collision_with_list(
                self.player, self.gem_pickup_list
            )
            for gem in gem_hit:
                self.window.show_view(self.window.game_won)
                gem.kill()
                self.current_level = 1

    def on_key_press(self, key, modifiers):
        """runs when a key is pressed"""
        # movement
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        if key == arcade.key.UP and self.player_physics_engine.can_jump(y_distance=5):
            self.player.change_y = JUMP_SPEED
        if key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
        # shooting
        if not self.player.jump:
            if key == arcade.key.SPACE:
                if self.bullet_amount > 0:
                    if self.player.character_face_direction == LEFT_FACING:
                        bullet = arcade.Sprite(
                            "assets/consumables/Bullet-1.png.png",
                            BULLET_SCAILING,
                            flipped_horizontally=True,
                        )
                        bullet.change_x = -BULLET_SPEED
                        bullet.center_x = self.player.center_x - 45
                        bullet.center_y = self.player.center_y
                        self.bullet_amount -= 1
                    else:
                        bullet = arcade.Sprite(
                            "assets/consumables/Bullet-1.png.png", BULLET_SCAILING
                        )
                        bullet.change_x = BULLET_SPEED
                        bullet.center_x = self.player.center_x + 45
                        bullet.center_y = self.player.center_y
                        self.bullet_amount -= 1
                    self.bullet_list.append(bullet)
        # switches view to pause view
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.pause_view)

    def on_key_release(self, key, modifiers):
        """runs when a key is released"""
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
