'''
Escape Room
-----------
Attempt to create an Escape Room Game.
'''

import random
import arcade

# --- Constants ---
SW = 800
SH = 600

#------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()

    def on_update(self, dt):
        pass


#-----Main Function--------
def main():
    window = MyGame(SW,SH,"My Escape Room")
    arcade.run()

#------Run Main Function-----
if __name__ == "__main__":
    main()
