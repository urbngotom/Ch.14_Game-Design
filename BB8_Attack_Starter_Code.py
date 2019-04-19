import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
SW = 800
SH = 600

#------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        arcade.start_render()

    def update(self, dt):
        pass



#-----Main Class--------
def main():
    window = MyGame(SW,SH,"BB8 Attack")
    arcade.run()



#------Run Main----------
if __name__ == "__main__":
    main()