# 14.0 BB8 ATTACK GAME   Name:________________
 
# You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 14.


import random
import arcade
import math

# --- Constants ---
# scaling constants
BB8_scale = 0.3
BB8_speed = 5
trooper_scale = 0.1
bullet_scale = 1
wall_scale = .5

SW = 800
SH = 600
SP = 4

# speeds
bullet_speed = 10
e_bullet_speed = 5
trooper_speed = -2
movement_speed = 5
angle_speed = 5

# points for shooting bullets and troopers
t_score = 5
b_score = 1
EXPLOSION_TEXTURE_COUNT = 50
'''
0 = instructions
1-3 = Game Playing Levels
4 = Game Over
'''
levels = 3
trooper_count = [0, 1, 2, 3, 0]


# --- Player Class ---
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale, hit_box_algorithm='Simple')
        self.laser_sound = arcade.load_sound("sounds/laser.wav")
        self.explosion = arcade.load_sound("sounds/explosion.wav")
        self.dx = self.change_x
        self.speed = 0
        self.change_angle = 0

    def update(self):
        self.center_x += self.dx
        self.angle += self.change_angle
        angle_rad = math.radians(self.angle)

        # use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        if self.left < 0:
            self.left = 0
        if self.right > SW:
            self.right = SW
        if self.top > SH:
            self.top = SH
        if self.bottom < 0:
            self.bottom = 0


# --- Explosion Class ---
class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png")
        self.textures = texture_list
        self.current_texture = 0

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


# --- Trooper Class ---
class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)
        self.dx = random.randrange(-1, 2, 2)
        self.dy = random.randrange(-1, 2, 2)

    def update(self):
        self.center_y += self.dy
        self.center_x += self.dx
        if self.bottom < 0 or self.top > SH:
            self.dy *= -1
        elif self.left < 0 or self.right > SW:
            self.dx *= -1


# --- Bullet Class ---
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        angle_shoot = math.radians(self.angle-90)
        self.center_x += -self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)
        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()


# --- Enemy Bullet Class ---
class Enemy_Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.wav")
        self.angle_list = [0, 90, 180, 270]
        self.angle = random.choice(self.angle_list)

    def update(self):
        if self.angle == 0:
            self.center_x += e_bullet_speed
        elif self.angle == 90:
            self.center_y += e_bullet_speed
        elif self.angle == 180:
            self.center_x -= e_bullet_speed
        else:
            self.center_y -= e_bullet_speed

        if self.top < 0 or self.bottom > SH or self.right < 0 or self.left > SW:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)
        self.current_level = 0
        self.gameover = True
        self.score = 0

        # Preload the explosion texture list
        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):
        # create Sprite Lists
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ebullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        # make a stack of walls
        for y in range(5):
            wall = arcade.Sprite("Images/wall.png", wall_scale)
            wall.center_x = int(SW // 3)
            wall.center_y = int(SH // 4) + y * wall.height
            self.walls.append(wall)

        # make a stack on the right side
        wall_coordinates = [
            [469, 278],
            [533, 278],
            [533, 214],
            [469, 214]
        ]

        for coordinate in wall_coordinates:
            wall = arcade.Sprite("Images/wall.png", wall_scale)
            wall.center_x = coordinate[0]
            wall.center_y = coordinate[1]
            self.walls.append(wall)

        if self.current_level in range(1, levels+1):
            self.background = arcade.load_texture(f"Images/sky{self.current_level}.png")

            # create Player
            self.BB8 = Player()
            self.BB8.center_x = SW / 2
            self.BB8.center_y = SH / 2
            self.player_list.append(self.BB8)

            # create Troopers
            for i in range(trooper_count[self.current_level]):
                trooper = Trooper()
                if i % 2 == 0:
                    trooper.center_x = random.randrange(trooper.w, int(SW / 4))
                    trooper.center_y = random.randrange(trooper.h, SH - trooper.h)
                else:
                    trooper.center_x = random.randrange(int(SW * 3/4), SW - trooper.w)
                    trooper.center_y = random.randrange(trooper.h, SH - trooper.h)
                self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        if self.current_level == 0:
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use arrow keys to move BB8 and SPACE to shoot. Press P to play", SW / 2, SH / 2,
                             arcade.color.NEON_GREEN, 14, anchor_x="center", anchor_y="center")

        elif not self.gameover:
            arcade.draw_texture_rectangle(SW // 2, SH // 2, SW, SH, self.background)
            self.ebullet_list.draw()
            self.player_list.draw()
            self.trooper_list.draw()
            self.bullet_list.draw()
            self.explosions_list.draw()
            self.walls.draw()

            # put the text on screen
            output = f"Level: {self.current_level} Score: {self.score}"
            arcade.draw_rectangle_filled(SW - 100, SH - 20, 200, 40, arcade.color.BLACK)
            arcade.draw_text(output, SW - 170, SH - 25, arcade.color.YELLOW, 14)

        #draw gameover screen
        else:
            if self.gameover == True:
                arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
                arcade.draw_text(f"High Score: {self.score}", SW / 2, SH / 2 + 30, arcade.color.NEON_GREEN, 14, anchor_x = "center", anchor_y = "center")
                arcade.draw_text("Game Over! Press I for instructions or P to play again!", SW / 2, SH / 2, arcade.color.NEON_GREEN, 14,anchor_x="center", anchor_y="center")

    def on_update(self, dt):
        if self.current_level in range(1, levels+1):
            self.gameover = False
        else:
            self.gameover = True

        if not self.gameover:
            # update sprite lists
            self.bullet_list.update()
            self.ebullet_list.update()
            self.player_list.update()
            self.trooper_list.update()
            self.explosions_list.update()

            # level up if all troopers shot
            if len(self.trooper_list) == 0:
                self.current_level += 1
                self.reset()

            # BB8 runs into walls
            BB8_hit_wall = arcade.check_for_collision_with_list(self.BB8, self.walls)
            if len(BB8_hit_wall) > 0 and not self.gameover:
                self.BB8.speed *= -1
                BB8_hit_wall.clear()

            # kill BB8 if trooper runs into it
            BB8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
            if len(BB8_hit) > 0 and not self.gameover:
                self.BB8.kill()
                arcade.play_sound(self.BB8.explosion)
                self.current_level = levels + 1

            # randomly drop enemy bombs/bullets
            for trooper in self.trooper_list:
                if random.randrange(1000) == 0:
                    ebullet = Enemy_Bullet()
                    ebullet.center_x = trooper.center_x
                    ebullet.center_y = trooper.center_y
                    self.ebullet_list.append(ebullet)

                # trooper runs into walls
                trooper_hit_wall = arcade.check_for_collision_with_list(trooper, self.walls)
                if len(trooper_hit_wall) > 0 and not self.gameover:
                    if trooper.center_x < trooper_hit_wall[0].left or trooper.center_x > trooper_hit_wall[0].right:
                        trooper.dx *= -1
                    if trooper.center_y < trooper_hit_wall[0].bottom or trooper.center_y > trooper_hit_wall[0].top:
                        trooper.dy *= -1
                    trooper_hit_wall.clear()

            # kill enemy bullets that hit walls
            for ebullet in self.ebullet_list:
                ebullet_hit_wall = arcade.check_for_collision_with_list(ebullet, self.walls)
                if len(ebullet_hit_wall) > 0 and not self.gameover:
                    ebullet.kill()

            # kill BB8 if it gets nuked
            BB8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullet_list)
            if len(BB8_bombed) > 0 and not self.gameover:
                self.BB8.kill()
                arcade.play_sound(self.BB8.explosion)
                self.current_level = levels + 1

            # kill a trooper if BB8 shot it
            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
                if len(hit_list) > 0 and not self.gameover:
                    arcade.play_sound(self.bullet.explosion)
                    bullet.kill()
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    self.explosions_list.append(explosion)
                for trooper in hit_list:
                    trooper.kill()
                    self.score += t_score

                # kill player/BB8 bullets that hit walls
                bullet_hit_wall = arcade.check_for_collision_with_list(bullet, self.walls)
                if len(bullet_hit_wall) > 0 and not self.gameover:
                    bullet.kill()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A and not self.gameover:
            self.BB8.change_angle = angle_speed

        elif key == arcade.key.D and not self.gameover:
            self.BB8.change_angle = -angle_speed

        elif key == arcade.key.W and not self.gameover:
            self.BB8.speed = movement_speed

        elif key == arcade.key.S and not self.gameover:
            self.BB8.speed = -movement_speed

        elif key == arcade.key.SPACE and not self.gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.center_y
            self.bullet.angle = self.BB8.angle + 90
            self.bullet.speed = bullet_speed
            self.bullet_list.append(self.bullet)
            self.score -= b_score
            arcade.play_sound(self.BB8.laser_sound)

        if key == arcade.key.P and self.gameover:
            self.current_level = 1
            self.score = 0
            self.reset()
        elif key == arcade.key.I and self.gameover:
            self.current_level = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.BB8.change_angle = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.BB8.speed = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Walls")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
