'''
FINAL GAME PROJECT
------------------
Here you will start the beginning of a game that you will be able to update as we
learn more in upcoming chapters. Below are some ideas that you could include:

1.) Find some new sprite images.
2.) Move the player sprite with arrow keys rather than the mouse. Don't let it move off the screen.
3.) Move the other sprites in some way like moving down the screen and then re-spawning above the window.
4.) Use sounds when a sprite is killed or the player hits the sidewall.
5.) See if you can reset the game after 30 seconds. Remember the on_update() method runs every 1/60th of a second.
6.) Try some other creative ideas to make your game awesome. Perhaps collecting good sprites while avoiding bad sprites.
7.) Keep score and use multiple levels. How do you keep track of an all time high score?
8.) Make a two player game.

'''

import random
import arcade

# --- Constants ---
# window dimensions
SW = 800
SH = 600

# player constants
PLAYER_SCALE = 2
PLAYER_SPEED = 3
UPDATES_PER_FRAME = 5
RIGHT_FACING = 0
LEFT_FACING = 1

# slime constants
SLIME_SCALE = 2
SLIME_SPEED = -1

# levels
LEVELS = 3
SLIME_COUNT = [0, 2, 4, 8, 0]
GROUND_LEVEL = SH // 3 + 10

# --- Load Textures ---
def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

# --- Player Class ---
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.character_face_direction = RIGHT_FACING
        self.current_texture = 0
        self.scale = PLAYER_SCALE

        # check what action player is performing
        self.is_attacking = False

        # --- Load Textures ---
        # idle texture
        self.idle_texture_pair = load_texture_pair("Sprites/Adventurer/idle/adventurer-idle-00.png")

        # run texture
        self.run_textures = []
        for i in range(6):
            texture = load_texture_pair(f"Sprites/Adventurer/run/adventurer-run-0{i}.png")
            self.run_textures.append(texture)

        # attack texture
        self.attack_textures = []
        for i in range(5):
            texture = load_texture_pair(f"Sprites/Adventurer/attack/adventurer-attack1-0{i}.png")
            self.attack_textures.append(texture)

    def update_animation(self, dt):
        # if needed, change player's facing direction
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # leftmost boundry of map prob need to check how to loop each frame
        if self.center_x - 15 < 0:
            self.change_x *= 0

        # idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # walking animation
        self.current_texture += 1
        if self.current_texture > 5 * UPDATES_PER_FRAME:
            self.current_texture = 0
        frame = self.current_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.run_textures[frame][direction]

        # attack animation
        if self.is_attacking:
            self.current_texture += 1
            if self.current_texture > 4 * UPDATES_PER_FRAME:
                self.current_texture = 0
            frame = self.current_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.attack_textures[frame][direction]


# --- Slime Class ---
class Slime(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.current_texture = 0
        self.scale = SLIME_SCALE
        self.slime_face_direction = LEFT_FACING
        self.change_x = SLIME_SPEED
        self.death_sound = arcade.load_sound("sounds/slime_death.wav")

        # load textures
        self.hop_textures = []
        for i in range(7):
            texture = load_texture_pair(f"Sprites/slime/slime_{i}.png")
            self.hop_textures.append(texture)

    def update_animation(self, dt):
        self.center_x += self.change_x

        if self.center_x > SW and self.slime_face_direction == RIGHT_FACING:
            self.slime_face_direction = LEFT_FACING
            self.change_x *= -1
        if self.center_x < 0 and self.slime_face_direction == LEFT_FACING:
            self.slime_face_direction = RIGHT_FACING
            self.change_x *= -1

        # HOPPING ANIMATION
        self.current_texture += 1
        if self.current_texture > 6 * UPDATES_PER_FRAME:
            self.current_texture = 0
        frame = self.current_texture // UPDATES_PER_FRAME
        direction = self.slime_face_direction
        self.texture = self.hop_textures[frame][direction]


# --- Explosion Class ---
class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Sprites/Explosion/Explosion_1.png")
        self.textures = texture_list
        self.current_texture = 0
        self.scale = 0.25

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_mouse_visible(False)
        self.current_level = 0
        self.gameover = True
        self.score = 0
        self.background_noise = arcade.load_sound("sounds/droplets.wav")
        arcade.play_sound(self.background_noise)

        # load backgrounds
        self.background = arcade.load_texture("background/cave1.png")

        # Preload the explosion texture list
        self.explosion_texture_list = []
        for i in range(1, 11):
            texture_name = f"Sprites/Explosion/Explosion_{i}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):
        # create Sprite Lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.attack_hitbox_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.enemy_icon_list = arcade.SpriteList()

        # enemy icon next to enemy counter
        self.enemies_left = SLIME_COUNT[self.current_level]
        self.enemy_icon = arcade.Sprite("Sprites/enemy_counter.png", 0.1)
        self.enemy_icon.center_x = 30
        self.enemy_icon.center_y = 35
        self.enemy_icon_list.append(self.enemy_icon)

        # create Player
        self.adventurer = Player()
        self.adventurer.center_x = SW // 2
        self.adventurer.center_y = GROUND_LEVEL
        self.player_list.append(self.adventurer)

        # create Slimes
        for i in range(SLIME_COUNT[self.current_level]):
            slime = Slime()
            if i % 2 == 0:
                slime.center_x = random.randint(SW+100, SW+500)
                slime.center_y = GROUND_LEVEL - 25
            else:
                slime.center_x = random.randint(-500, -50)
                slime.center_y = GROUND_LEVEL - 25
            self.enemy_list.append(slime)


    def on_draw(self):
        arcade.start_render()

        if self.current_level == 0:
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use A and D to move. Use J while moving to attack. Press P to play", SW / 2, SH / 2,
                             arcade.color.NEON_GREEN, 14, anchor_x="center", anchor_y="center")

        elif not self.gameover:
            # draw backgrounds
            for i in range(1, 2):
                arcade.draw_texture_rectangle(SW // 2 * i, SH // 2 * i, SW, SH, self.background)
                arcade.draw_rectangle_filled(SW // 2 * i, SH // 8 * i, SW, SH // 3, arcade.color.BLACK)

            self.player_list.draw()
            self.enemy_list.draw()
            self.attack_hitbox_list.draw()
            self.explosions_list.draw()
            self.enemy_icon_list.draw()

            # draws transparent hit box for sword if player is attacking
            if self.adventurer.character_face_direction == RIGHT_FACING and self.adventurer.is_attacking:
                self.attack_hitbox = arcade.Sprite("Sprites/Adventurer/attack_hitbox1.png", 1)
                self.attack_hitbox.center_x = self.adventurer.center_x + 20
                self.attack_hitbox.center_y = self.adventurer.center_y
                self.attack_hitbox.width = self.adventurer.width - 45
                self.attack_hitbox.height = self.adventurer.height
                self.attack_hitbox_list.append(self.attack_hitbox)
                self.attack_hitbox_list.clear()
            elif self.adventurer.character_face_direction == LEFT_FACING and self.adventurer.is_attacking:
                self.attack_hitbox = arcade.Sprite("Sprites/Adventurer/attack_hitbox1.png", 1)
                self.attack_hitbox.center_x = self.adventurer.center_x - 20
                self.attack_hitbox.center_y = self.adventurer.center_y
                self.attack_hitbox.width = self.adventurer.width - 45
                self.attack_hitbox.height = self.adventurer.height
                self.attack_hitbox_list.append(self.attack_hitbox)
                self.attack_hitbox_list.clear()

            # put the score and enemy counter text on screen
            output = f"Score: {self.score}"
            arcade.draw_text(output, SW - 100, 20, arcade.color.WHITE, 14)

            output = f"{self.enemies_left} left"
            arcade.draw_text(output, 60, 20, arcade.color.WHITE, 14)

        else:
            # Winning screen
            if self.gameover and self.current_level == 4:
                arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
                arcade.draw_text(f"Enemies Killed: {self.score}", SW / 2, SH / 2 + 30, arcade.color.NEON_GREEN, 14,
                                 anchor_x="center", anchor_y="center")
                arcade.draw_text("You Won! Press P to play again!", SW / 2, SH / 2, arcade.color.NEON_GREEN, 14,
                                 anchor_x="center", anchor_y="center")

            # Game over screen if user lost
            if self.current_level != 4 and self.gameover:
                arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
                arcade.draw_text(f"Enemies Killed: {self.score}", SW / 2, SH / 2 + 30, arcade.color.NEON_GREEN, 14,
                                 anchor_x="center", anchor_y="center")
                arcade.draw_text("Game Over! Press P to play again!", SW / 2, SH / 2, arcade.color.NEON_GREEN, 14,
                                 anchor_x="center", anchor_y="center")

    def on_update(self, dt):
        if self.current_level in range(1, LEVELS+1):
            self.gameover = False
        else:
            self.gameover = True

        if not self.gameover:
            self.player_list.update()
            self.player_list.update_animation()
            self.enemy_list.update_animation()
            self.attack_hitbox_list.update_animation()
            self.explosions_list.update()

            # move onto next level if all enemies cleared
            if len(self.enemy_list) == 0 and not self.gameover:
                self.current_level += 1
                self.reset()

            # check if player attacks slime
            if self.adventurer.is_attacking:
                slime_hit = arcade.check_for_collision_with_list(self.attack_hitbox, self.enemy_list)
                if len(slime_hit) > 0 and not self.gameover:
                    for slime in slime_hit:
                        slime.kill()
                        explosion = Explosion(self.explosion_texture_list)
                        explosion.center_x = slime_hit[0].center_x
                        explosion.center_y = slime_hit[0].center_y
                        self.explosions_list.append(explosion)
                        arcade.play_sound(slime.death_sound)
                        self.score += 1
                        self.enemies_left -= 1

            # check if player is hit by slime
            for slime in self.enemy_list:
                player_hit = arcade.check_for_collision_with_list(slime, self.player_list)
                if len(player_hit) > 0 and not self.gameover:
                    self.gameover = True
                    self.current_level = LEVELS + 2
                    self.adventurer.kill()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.adventurer.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.adventurer.change_x = PLAYER_SPEED
        elif key == arcade.key.J:
            self.adventurer.is_attacking = True
        elif key == arcade.key.P and self.gameover:
            self.current_level = 1
            self.score = 0
            self.reset()
        elif key == arcade.key.I and self.gameover:
            self.current_level = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.adventurer.change_x = 0
        elif key == arcade.key.J:
            self.adventurer.is_attacking = False
            self.attack_hitbox_list.clear()


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "Slimevasion")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()