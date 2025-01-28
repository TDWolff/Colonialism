import arcade
from screeninfo import get_monitors
import math

monitor = get_monitors()[0]
resolutions = [(1920, 1080), (2560, 1440), (1280, 720)]
resolution = {monitor.width, monitor.height}

SCREEN_WIDTH = monitor.width
SCREEN_HEIGHT = monitor.height

HEX_EMPTY = "textures/game/emptyTile.png"
HEX_PLAYER = "textures/game/playerTile.png"
HEX_SELECT = "textures/game/selectTile.png"
HEX_SIZE = 7
ROWS = 5
COLUMNS = 8
OFFSET = 55

if resolution not in resolutions:
    resolutions.append(resolution)
    print("Added new resolution: " + str(resolution))
    
SCREEN_TITLE = "Colonialism"

class Colonialism(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.DIM_GRAY)
        self.selected_hex = None
        self.player_selected = False

    def setup(self):
        self.player_list = arcade.SpriteList()
        image_source = "textures/game/mousepointer.png"
        self.player_sprite = arcade.Sprite(image_source, 0.025)
        self.player_list.append(self.player_sprite)
        self.hex_sprites = arcade.SpriteList()
        self.create_hex_grid()
        self.set_mouse_visible(False)
        
    def get_hex_at_position(self, x, y):
        for hex_sprite in self.hex_sprites:
            if hex_sprite.collides_with_point((x, y)):
                return hex_sprite
        return None
        
    def create_hex_grid(self):
        base_hex_width = 1000
        base_hex_height = 867
        
        scale = HEX_SIZE / 50
        hex_width = base_hex_width * scale
        hex_height = base_hex_height * scale

        x_spacing = hex_width * 0.75
        y_spacing = hex_height * 0.975

        grid_width = (COLUMNS - 1) * x_spacing + hex_width
        grid_height = (ROWS - 1) * y_spacing + hex_height

        start_x = (SCREEN_WIDTH - grid_width) / 2 + OFFSET
        start_y = (SCREEN_HEIGHT - grid_height) / 2 + OFFSET

        for row in range(ROWS):
            for col in range(COLUMNS):
                x = start_x + col * x_spacing
                y = start_y + row * y_spacing
                if col % 2 == 1:
                    y += y_spacing / 2

                hex_sprite = arcade.Sprite(HEX_EMPTY, scale=scale)
                hex_sprite.center_x = x
                hex_sprite.center_y = y
                self.hex_sprites.append(hex_sprite)

    def on_mouse_motion(self, x, y, dx, dy):
        mouseX = x + 11
        mouseY = y - 9
        self.player_sprite.position = mouseX, mouseY

        for hex_sprite in self.hex_sprites:
            if hex_sprite != self.selected_hex:
                hex_sprite.texture = arcade.load_texture(HEX_EMPTY)

        hovered_hex = self.get_hex_at_position(mouseX, mouseY)
        if hovered_hex and hovered_hex != self.selected_hex:
            hovered_hex.texture = arcade.load_texture(HEX_SELECT)
            
    def on_mouse_press(self, x, y, button, modifiers):
        hovered_hex = self.get_hex_at_position(x, y)

        if hovered_hex:
            if not self.player_selected:
                if self.selected_hex:
                    self.selected_hex.texture = arcade.load_texture(HEX_EMPTY)
                
                hovered_hex.texture = arcade.load_texture(HEX_PLAYER)
                self.selected_hex = hovered_hex
                print("Player selected a tile!")
                self.player_selected = True

    def on_draw(self):
        self.clear()
        self.hex_sprites.draw()
        self.player_list.draw()

def main():
    window = Colonialism()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
