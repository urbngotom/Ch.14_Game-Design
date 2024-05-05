# 14.0 BB8 ATTACK GAME   Name:________________
 
# You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 14.


import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
SW = 800
SH = 600


# --- Player Class ---
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.wav")
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        pass


# --- Trooper Class ---
class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        pass


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_mouse_visible(False)

    def reset(self):
        # create Sprite Lists
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()

        # initiate the score
        self.score = 0

        # create Player
        self.BB8 = Player()
        self.BB8.center_x = SW / 2
        self.BB8.center_y = SH / 2
        self.player_list.append(self.BB8)

        # create Troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randint(trooper.w, SW - trooper.w)
            trooper.center_y = random.randint(trooper.h, SH - trooper.h)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.trooper_list.draw()

        # put the text on screen
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def on_update(self, dt):
        self.player_list.update()
        self.trooper_list.update()

        trooper_hit_list = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        for trooper in trooper_hit_list:
            trooper.kill()
            self.score += 1
            arcade.play_sound(self.BB8.laser_sound)

        if len(self.trooper_list) == 0:
            self.reset()

    def on_mouse_motion(self, x, y, dx, dy):
        self.BB8.center_x = x
        self.BB8.center_y = y


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
