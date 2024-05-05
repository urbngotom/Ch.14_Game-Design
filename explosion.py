# 14.0 BB8 ATTACK GAME   Name:________________
 
# You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 14.


import random
import arcade

# --- Constants ---
# scaling constants
BB8_scale = 0.3
BB8_speed = 5
trooper_scale = 0.1
trooper_count = 40
bullet_scale = 1
SW = 800
SH = 600
SP = 4
bullet_speed = 10
trooper_speed = -2

# points for shooting bullets and troopers
t_score = 5
b_score = 1
EXPLOSION_TEXTURE_COUNT = 50


# --- Player Class ---
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale, hit_box_algorithm='Simple')
        self.laser_sound = arcade.load_sound("sounds/laser.wav")
        self.explosion = arcade.load_sound("sounds/explosion.wav")
        self.dx = self.change_x

    def update(self):
        self.center_x += self.dx

        if self.right < 0:
            self.left = SW
        if self.left > SW:
            self.right = 0


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

    def update(self):
        self.center_y += trooper_speed
        if self.top < 0:
            self.center_x = random.randrange(self.w, SW-self.w)
            self.center_y = random.randrange(SH+self.h, SH * 2)


# --- Bullet Class ---
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.center_y += bullet_speed
        if self.bottom > SH:
            self.kill()


# --- Enemy Bullet Class ---
class Enemy_Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.center_y -= bullet_speed
        if self.top < 0:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)

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

        # initiate the score
        self.score = 0
        self.gameover = False

        # create Player
        self.BB8 = Player()
        self.BB8.center_x = SW / 2
        self.BB8.bottom = 2
        self.player_list.append(self.BB8)

        # create Troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randint(trooper.w, SW - trooper.w)
            trooper.center_y = random.randint(SH // 2, SH * 2)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        self.ebullet_list.draw()
        self.player_list.draw()
        self.trooper_list.draw()
        self.bullet_list.draw()
        self.explosions_list.draw()

        # put the text on screen
        output = f"Score: {self.score}"
        arcade.draw_text(output, SW - 80, SH - 20, arcade.color.YELLOW, 14)

        # draw gameover screen
        if self.gameover == True:
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text(f"High Score: {self.score}", SW / 2, SH / 2 + 30, arcade.color.NEON_GREEN, 14, anchor_x = "center", anchor_y = "center")
            arcade.draw_text("Game Over! Press P to play again!", SW / 2, SH / 2, arcade.color.NEON_GREEN, 14,anchor_x="center", anchor_y="center")

    def on_update(self, dt):
        # update sprite lists
        self.bullet_list.update()
        self.ebullet_list.update()
        self.player_list.update()
        self.trooper_list.update()
        self.explosions_list.update()

        # game over if all troopers shot
        if len(self.trooper_list) == 0:
            self.gameover = True

        # kill BB8 if trooper runs into it
        BB8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        if len(BB8_hit) > 0 and not self.gameover:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.gameover = True

        # randomly drop enemy bombs/bullets
        for trooper in self.trooper_list:
            if random.randrange(1000) == 0:
                ebullet = Enemy_Bullet()
                ebullet.angle = -90
                ebullet.center_x = trooper.center_x
                ebullet.center_y = trooper.center_y
                self.ebullet_list.append(ebullet)

        # kill BB8 if it gets nuked
        BB8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullet_list)
        if len(BB8_bombed) > 0 and not self.gameover:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.gameover = True

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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.BB8.dx = -BB8_speed

        elif key == arcade.key.D:
            self.BB8.dx = BB8_speed

        elif key == arcade.key.SPACE and not self.gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.center_y
            self.bullet.angle = 90
            self.bullet_list.append(self.bullet)
            self.score -= b_score
            arcade.play_sound(self.BB8.laser_sound)

        elif key == arcade.key.P:
            self.reset()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.BB8.dx = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Enemy Bombs")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
