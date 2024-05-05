import random
import arcade

# --- Constants ---
BB8_scale = 0.3
BB8_speed = 3
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
        self.dx = self.change_x
        self.dy = self.change_y

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

        if self.left < 0 or self.right > SW:
            self.dx = 0
        if self.bottom < 0 or self.top > SH:
            self.dy = 0


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
            arcade.play_sound(self.BB8.explosion)

        if len(self.trooper_list) == 0:
            self.reset()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.BB8.dx = -BB8_speed
        elif key == arcade.key.D:
            self.BB8.dx = BB8_speed
        elif key == arcade.key.W:
            self.BB8.dy = BB8_speed
        elif key == arcade.key.S:
            self.BB8.dy = -BB8_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.BB8.dx = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.BB8.dy = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()