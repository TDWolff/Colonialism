import arcade
from screeninfo import get_monitors
import random
from perlin_noise import PerlinNoise
import numpy as np

monitor = get_monitors()[0]
resolutions = [(1920, 1080), (2560, 1440), (1280, 720)]
resolution = (monitor.width, monitor.height)

SCREEN_WIDTH = monitor.width
SCREEN_HEIGHT = monitor.height

HEX_EMPTY = "textures/game/emptyTile.png"
HEX_PLAYER = "textures/game/playerTile.png"
HEX_SELECT = "textures/game/selectTile.png"
HEX_SIZE = 7
ROWS = 6
COLUMNS = 10
OFFSET = 55

TARGET_FPS = 120

# Tile datas
terrains = ["grass", "mountain", "desert", "forest", "beach"]
terrain_resources = {
    "grass": {"wood": 3, "stone": 1, "coal": 2, "water": 2},
    "mountain": {"wood": 0, "stone": 5, "coal": 4, "water": 1},
    "desert": {"wood": 0, "stone": 2, "coal": 1, "water": 0},
    "forest": {"wood": 5, "stone": 1, "coal": 3, "water": 3},
    "beach": {"wood": 1, "stone": 1, "coal": 0, "water": 5}
}

if resolution not in resolutions:
    resolutions.append(resolution)
    print("Added new resolution: " + str(resolution))

SCREEN_TITLE = "Colonialism"

class Colonialism(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.DIM_GRAY)
        arcade.enable_timings()
        self.selected_hex = None
        self.player_selected = False
        self.texture_empty = arcade.load_texture(HEX_EMPTY)
        self.texture_player = arcade.load_texture(HEX_PLAYER)
        self.texture_select = arcade.load_texture(HEX_SELECT)
        self.prev_hovered_hex = None
        self.set_mouse_visible(False)
        self.fps_counter = 0
        self.time_since_last_update = 0  # Track time for FPS control
        self.selected_index = None
        self.hex_data_tile = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        image_source = "textures/game/mousepointer.png"
        self.player_sprite = arcade.Sprite(image_source, 0.025)
        self.mouseInfoX = 0
        self.mouseInfoY = 0
        self.player_list.append(self.player_sprite)
        self.hex_sprites = arcade.SpriteList()
        self.create_hex_grid()
        self.give_hex_data()
        
    def give_hex_data(self):
        scale = 0.5  # Adjust scale for terrain clustering

        for index, hex_sprite in enumerate(self.hex_sprites):
            x, y = hex_sprite.center_x * scale, hex_sprite.center_y * scale
            noise = PerlinNoise(octaves=3, seed=random.randint(0, 1000))
            perlin_value = noise([x, y])
            
            # Adjust thresholds to better distribute terrain types
            if perlin_value < -0.3:
                terrain = "mountain"
            elif perlin_value < -0.1:
                terrain = "forest"
            elif perlin_value < 0.1:
                terrain = "grass"
            elif perlin_value < 0.2:
                terrain = "beach"
            else:
                terrain = "desert"
            
            resources = terrain_resources[terrain]
            
            hex_sprite.data = {
                "id": index,
                "coordinates": (hex_sprite.center_x, hex_sprite.center_y),
                "terrain": terrain,
                "resources": resources
            }
            print(f"Hex {index} data: {hex_sprite.data}")
            self.selected_index = index
            self.hex_data_tile = hex_sprite.data
            
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
        start_x = (SCREEN_WIDTH - grid_width) / 2 + 150
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
        hovered_hex = self.get_hex_at_position(mouseX, mouseY)
        self.player_sprite.position = mouseX, mouseY
        self.mouseInfoX = x
        self.mouseInfoY = y
        
        if hovered_hex != self.prev_hovered_hex:
            if self.prev_hovered_hex and self.prev_hovered_hex != self.selected_hex:
                self.prev_hovered_hex.texture = self.texture_empty
            if hovered_hex and hovered_hex != self.selected_hex:
                hovered_hex.texture = self.texture_select
            self.prev_hovered_hex = hovered_hex

    def on_mouse_press(self, x, y, button, modifiers):
        hovered_hex = self.get_hex_at_position(x, y)
        if hovered_hex:
            if not self.player_selected:
                if self.selected_hex:
                    self.selected_hex.texture = self.texture_empty
                hovered_hex.texture = self.texture_player
                self.selected_hex = hovered_hex
                print("Player selected a tile!")
                print(f"Hex {self.selected_index} data: {self.hex_data_tile}")
                self.player_selected = True
                
    def on_draw(self):
        self.clear()
        self.hex_sprites.draw()
        self.player_list.draw()

        # Draw FPS
        fps_text = arcade.Text(f"FPS: {arcade.get_fps():.1f}", 100, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)
        fps_text.draw()
        
        infoX = 50
        infoY = 600

        # Draw info box background
        info = arcade.draw_lbwh_rectangle_filled(infoX, infoY, 170, 130, arcade.color.GRAY_BLUE)
        info_outline = arcade.draw_lbwh_rectangle_outline(infoX, infoY, 170, 130, arcade.color.BLACK, 10) 

        # Initialize info_text
        info_text = ""  # Initialize info_text here

        # Draw info text for the hovered tile
        hovered_hex = self.get_hex_at_position(self.player_sprite.center_x, self.player_sprite.center_y)
        if hovered_hex:
            info_mouse = arcade.draw_lbwh_rectangle_filled(self.mouseInfoX + 30, self.mouseInfoY - 70, 160, 60, arcade.color.GRAY_BLUE)
            info_mouse_outline = arcade.draw_lbwh_rectangle_outline(self.mouseInfoX + 30, self.mouseInfoY - 70, 160, 60, arcade.color.BLACK, 3)
            info_mouse_text = f"Hex ID: {hovered_hex.data['id']}\n"
            info_mouse_text += f"Terrain: {hovered_hex.data['terrain']}\n"
            arcade.draw_text(info_mouse_text, self.mouseInfoX + 40, self.mouseInfoY - 35, arcade.color.WHITE, 14, width=230, align="left", multiline=True)

            
            info_text += "Resources:\n"  # Now you can safely append text to info_text

            for resource, amount in hovered_hex.data["resources"].items():
                info_text += f"  {resource.capitalize()}: {amount}\n"

            arcade.draw_text(info_text, infoX + 10, infoY + 100, arcade.color.WHITE, 14, width=230, align="left", multiline=True)


    def on_update(self, delta_time):
        self.time_since_last_update += delta_time
        if self.time_since_last_update >= 1 / TARGET_FPS:
            self.time_since_last_update -= 1 / TARGET_FPS
            super().on_update(delta_time)  # Call the default update method for things like movement, etc.

def main():
    window = Colonialism()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
