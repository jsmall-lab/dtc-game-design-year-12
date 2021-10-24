import typing

import arcade

WIDTH = 1200
HEIGHT = 800
TITLE = "The Game"

PLAYER_MOVEMENT_SPEED = 5
JUMP_SPEED = 11
VIEWPORT_MARGIN = 400

RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_FRAMES = 3
PLAYER_FRAMES_PER_TEXTURE = 6

BULLET_SPEED = 18
BULLET_SCAILING = 0.08
BULLET_DAMAGE = 20
BULLET_AMOUNT = 6

TOTAL_LEVELS = 3
MAX_LIVES = 3
MAX_PLAYER_HEALTH = 180
HEALTH_BAR_WIDTH = 200

MAX_ENEMY_HEALTH = 100
MAX_BOSS_HEALLTH = 300
ENEMY_MOVEMENT_SPEED = 2


def load_texture_pair(filename: str) -> typing.List[arcade.Texture]:
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
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

        self.jump_texture_pair = load_texture_pair(
            "./assets/sprites_for_game/main_character/main_character_jump.png"
        )

        self.idle = False

        self.idle_texture_pair = load_texture_pair(
            "./assets/sprites_for_game/main_character/main_character_idle-1.png.png"
        )

        self.walk_textures: typing.List[typing.List[arcade.Texture]] = []

        if not self.jump:
            for i in range(PLAYER_FRAMES):
                texture = load_texture_pair(
                    f"./assets/sprites_for_game/main_character/main_character{i}.png"
                )
                self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60):

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
        if self.virtual_frames > PLAYER_FRAMES * PLAYER_FRAMES_PER_TEXTURE - 1:
            self.virtual_frames = 0
            self.cur_texture = 0
        if (self.virtual_frames + 1) % PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_frames // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][
                self.character_face_direction
            ]


class Enemy1(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        # 0 - PLAYER_FRAMES
        self.virtual_frames = 0
        # 0 - 59

        self.touching_ramp = False

        # self.jump = False

        # self.jump_texture_pair = load_texture_pair("./assets/sprites_for_game/main_character/main_character_jump.png")

        self.idle = False

        self.idle_texture_pair = load_texture_pair(
            "./assets/sprites_for_game/enemies/enemy1/enemy_idle.png"
        )

        self.walk_textures: typing.List[typing.List[arcade.Texture]] = []

        # if self.jump == False:
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(
                f"./assets/sprites_for_game/enemies/enemy1/enemy{i}.png"
            )
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0 or self.change_y < 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.idle = True
            return

        # if self.change_y > 0:
        # self.texture = self.jump_texture_pair[self.character_face_direction]
        # self.jump = True
        # return

        self.jump = False

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
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        # 0 - PLAYER_FRAMES
        self.virtual_frames = 0
        # 0 - 59

        self.touching_ramp = False

        # self.jump = False

        # self.jump_texture_pair = load_texture_pair("./assets/sprites_for_game/main_character/main_character_jump.png")

        self.idle = False

        self.idle_texture_pair = load_texture_pair(
            "./assets/sprites_for_game/enemies/boss/boss_idle.png"
        )

        self.walk_textures: typing.List[typing.List[arcade.Texture]] = []

        # if self.jump == False:
        for i in range(PLAYER_FRAMES):
            texture = load_texture_pair(
                f"./assets/sprites_for_game/enemies/boss/boss{i}.png"
            )
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0 or self.change_y < 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            self.idle = True
            return

        # if self.change_y > 0:
        # self.texture = self.jump_texture_pair[self.character_face_direction]
        # self.jump = True
        # return

        self.jump = False

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
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
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
        self.current_level = 1
        self.enemy_list = None
        self.time_since_last_firing = 0.0
        self.time_between_firing = 0.9

    def load_map(self):
        platforms_layername = "walls"
        next_level_marker_layername = "next_level_marker"
        health_pickup_layername = "health_pickup"
        bullet_pickup_layername = "bullet_pickup"
        level = arcade.tilemap.read_tmx(
            f"assets/maps/level{self.current_level}_map.tmx"
        )
        self.wall_list = arcade.tilemap.process_layer(
            map_object=level,
            layer_name=platforms_layername,
            use_spatial_hash=True,
            scaling=0.5,
        )
        marker_list = arcade.tilemap.process_layer(
            map_object=level,
            layer_name=next_level_marker_layername,
            use_spatial_hash=True,
            scaling=0.5,
        )
        self.health_pickup_list = arcade.tilemap.process_layer(
            map_object=level,
            layer_name=health_pickup_layername,
            use_spatial_hash=True,
            scaling=0.5,
        )
        self.bullet_pickup_list = arcade.tilemap.process_layer(
            map_object=level,
            layer_name=bullet_pickup_layername,
            use_spatial_hash=True,
            scaling=0.5,
        )
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

    def progress_level(self):
        if self.current_level == TOTAL_LEVELS:
            self.window.show_view(self.window.game_won)
            self.current_level = 1
        else:
            self.window.show_view(self.window.level_won)
            self.current_level += 1
            self.time_between_firing -= 0.5
            self.setup()

    def enemiy_pos(self):
        if self.current_level == 1:
            enemy1 = Enemy1()
            enemy1.center_x = 8300
            enemy1.center_y = 448
            enemy1.change_x = ENEMY_MOVEMENT_SPEED
            enemy1.boundary_right = 8664
            enemy1.boundary_left = 7830
            enemy1.boundary_top = 600
            self.enemy_list.append(enemy1)

            enemy2 = Enemy1()
            enemy2.center_x = 10400
            enemy2.center_y = 1280
            enemy2.change_x = ENEMY_MOVEMENT_SPEED
            enemy2.boundary_right = 10953
            enemy2.boundary_left = 10373
            enemy2.boundary_top = 1400
            self.enemy_list.append(enemy2)

            enemy3 = Enemy1()
            enemy3.center_x = 16400
            enemy3.center_y = 512
            enemy3.change_x = ENEMY_MOVEMENT_SPEED
            enemy3.boundary_right = 17030
            enemy3.boundary_left = 16020
            enemy3.boundary_top = 600
            self.enemy_list.append(enemy3)

        if self.current_level == 2:
            enemy4 = Enemy1()
            enemy4.center_x = 3700
            enemy4.center_y = 384
            enemy4.change_x = ENEMY_MOVEMENT_SPEED
            enemy4.boundary_right = 4100
            enemy4.boundary_left = 3640
            enemy4.boundary_top = 450
            self.enemy_list.append(enemy4)

            enemy5 = Enemy1()
            enemy5.center_x = 6300
            enemy5.center_y = 960
            enemy5.change_x = ENEMY_MOVEMENT_SPEED
            enemy5.boundary_right = 6772
            enemy5.boundary_left = 5942
            enemy5.boundary_top = 1060
            self.enemy_list.append(enemy5)

            enemy6 = Enemy1()
            enemy6.center_x = 7400
            enemy6.center_y = 1792
            enemy6.change_x = ENEMY_MOVEMENT_SPEED
            enemy6.boundary_right = 7640
            enemy6.boundary_left = 7000
            enemy6.boundary_top = 1890
            self.enemy_list.append(enemy6)

            enemy7 = Enemy1()
            enemy7.center_x = 6000
            enemy7.center_y = 2304
            enemy7.change_x = ENEMY_MOVEMENT_SPEED
            enemy7.boundary_right = 7042
            enemy7.boundary_left = 6309
            enemy7.boundary_top = 2400
            self.enemy_list.append(enemy7)

            enemy8 = Enemy1()
            enemy8.center_x = 10000
            enemy8.center_y = 576
            enemy8.change_x = ENEMY_MOVEMENT_SPEED
            enemy8.boundary_right = 10448
            enemy8.boundary_left = 9498
            enemy8.boundary_top = 670
            self.enemy_list.append(enemy8)

        if self.current_level == 3:

            enemy9 = Enemy1()
            enemy9.center_x = 1000
            enemy9.center_y = 512
            enemy9.change_x = ENEMY_MOVEMENT_SPEED
            enemy9.boundary_right = 1220
            enemy9.boundary_left = 830
            enemy9.boundary_top = 610
            self.enemy_list.append(enemy9)

            enemy10 = Enemy1()
            enemy10.center_x = 3000
            enemy10.center_y = 512
            enemy10.change_x = ENEMY_MOVEMENT_SPEED
            enemy10.boundary_right = 3474
            enemy10.boundary_left = 2964
            enemy10.boundary_top = 610
            self.enemy_list.append(enemy10)

            enemy11 = Enemy1()
            enemy11.center_x = 5000
            enemy11.center_y = 768
            enemy11.change_x = ENEMY_MOVEMENT_SPEED
            enemy11.boundary_right = 5314
            enemy11.boundary_left = 4674
            enemy11.boundary_top = 860
            self.enemy_list.append(enemy11)

            enemy12 = Enemy1()
            enemy12.center_x = 6500
            enemy12.center_y = 384
            enemy12.change_x = ENEMY_MOVEMENT_SPEED
            enemy12.boundary_right = 6936
            enemy12.boundary_left = 6120
            enemy12.boundary_top = 480
            self.enemy_list.append(enemy12)

            enemy13 = Enemy1()
            enemy13.center_x = 6700
            enemy13.center_y = 384
            enemy13.change_x = 2.2
            enemy13.boundary_right = 6936
            enemy13.boundary_left = 6120
            enemy13.boundary_top = 480
            self.enemy_list.append(enemy13)

            enemy14 = Enemy1()
            enemy14.center_x = 8000
            enemy14.center_y = 1472
            enemy14.change_x = ENEMY_MOVEMENT_SPEED
            enemy14.boundary_right = 8828
            enemy14.boundary_left = 7628
            enemy14.boundary_top = 1600
            self.enemy_list.append(enemy14)

            boss = Boss()
            boss.center_x = 14000
            boss.center_y = 2944
            boss.change_x = ENEMY_MOVEMENT_SPEED
            boss.boundary_right = 14512
            boss.boundary_left = 13300
            boss.boundary_top = 3044
            self.enemy_list.append(boss)

    def player_lives(self):
        if self.lives == 0:
            self.lives = MAX_LIVES

    def setup(self):

        # main player
        self.player = PlayerCharacter()
        self.player_health = MAX_PLAYER_HEALTH
        self.player.center_x = 50
        self.player.center_y = 500
        self.view_left = 0
        self.view_bottom = 0
        self.player_lives()

        self.enemy_list = arcade.SpriteList()

        # bullet sprite
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.bullet_amount = BULLET_AMOUNT
        self.load_map()
        self.player_physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list
        )

        self.enemiy_pos()

    def player_health_bar(self):
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

    def lives_counter(self):
        arcade.draw_text(
            str(self.lives),
            self.view_left + 30,
            self.view_bottom + (HEIGHT - 150),
            arcade.color.BLACK,
            70,
        )

    def player_bullet_amount(self):
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

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player.draw()
        self.enemy_list.draw()
        self.health_pickup_list.draw()
        self.bullet_pickup_list.draw()
        self.lives_counter()
        self.player_bullet_amount()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.player_health_bar()
        if self.current_level == 3:
            self.gem_pickup_list.draw()

    def death(self):
        self.window.show_view(self.window.death_view)

    def game_failed(self):
        self.window.show_view(self.window.game_failed)

    def update(self, delta_time: float):
        self.enemy_list.update()
        self.player.update()
        self.player.update_animation()
        self.enemy_list.update()
        self.enemy_list.update_animation()
        self.time_since_last_firing += delta_time
        for enemy in self.enemy_list:
            #if arcade.check_for_collision_with_list(enemy, self.wall_list):
                #enemy.change_x *= -1
            if (
                enemy.center_x < enemy.boundary_left
                or enemy.center_x > enemy.boundary_right
            ):
                enemy.change_x *= -1
            if (
                self.player.center_x <= enemy.boundary_right
                and self.player.center_x >= enemy.boundary_left
                and self.player.center_y <= enemy.boundary_top
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
                        self.time_since_last_firing = 0
                    else:
                        bullet = arcade.Sprite(
                            "assets/consumables/Bullet-1.png.png", BULLET_SCAILING
                        )
                        bullet.change_x = BULLET_SPEED
                        bullet.center_x = enemy.center_x + 45
                        bullet.center_y = enemy.center_y
                        self.time_since_last_firing = 0

                    self.enemy_bullet_list.append(bullet)
        if self.current_level == 3:
            if self.player.center_x >= 12000:
                self.enemiy_health = MAX_BOSS_HEALLTH

        for bullet in self.bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            for b in touching:
                bullet.kill()

            for enemy in touching:

                self.enemiy_health -= BULLET_DAMAGE

                if self.enemiy_health == 0:
                    enemy.kill()
                    self.enemiy_health = MAX_ENEMY_HEALTH

        for bullet in self.enemy_bullet_list:
            touching = arcade.check_for_collision(bullet, self.player)
            if touching:
                bullet.kill()
                self.player_health -= BULLET_DAMAGE
                print(BULLET_DAMAGE, self.player_health)

        for bullet in self.enemy_bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.wall_list)
            for b in touching:
                bullet.kill()

            if bullet.center_x > self.player.center_x + WIDTH:
                bullet.kill()
            if bullet.center_x < self.player.center_x - WIDTH:
                bullet.kill()

        self.enemy_bullet_list.update()

        # if arcade.check_for_collision(enemy, self.player) == True:
        # exit()

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

        health_hit_list = arcade.check_for_collision_with_list(
            self.player, self.health_pickup_list
        )
        for health in health_hit_list:
            health.remove_from_sprite_lists()
            self.player_health = MAX_PLAYER_HEALTH

        bullet_hit_list = arcade.check_for_collision_with_list(
            self.player, self.bullet_pickup_list
        )
        for bullet in bullet_hit_list:
            bullet.kill()
            self.bullet_amount += BULLET_AMOUNT

        if self.current_level == 3:
            gem_hit = arcade.check_for_collision_with_list(
                self.player, self.gem_pickup_list
            )
            for gem in gem_hit:
                gem.kill()

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

        if self.view_left < 0:
            self.view_left = 0

        if self.player_health == 0:
            self.death()
            self.setup()
            self.lives -= 1

        if self.player.center_y < -1100:
            self.death()
            self.setup()
            self.lives -= 1

            # character live counter
        if self.lives == 0:
            self.game_failed()
            self.current_level = 1

        if self.player.center_x > self.marker_x:
            self.progress_level()

    def pause(self):
        self.window.show_view(self.window.pause_view)

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
        if key == arcade.key.ESCAPE:
            self.pause()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
