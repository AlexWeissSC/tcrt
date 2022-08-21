from typing import Tuple

import numpy as np # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32), # Unicode codepoint.
        ("fg", "3B"), # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool), # True if this tile can be walked over.
        ("transparent", np.bool), # True if this tile doesn't block FOV.
        ("dark", graphic_dt), # Graphics for when this tile is not in FOV.
        ("light", graphic_dt), # Graphics for when the tile is in FOV
    ]
)

def new_tile(
        *, # Enforce the use of keywords, so that parameter order doesn't matter.
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable= True,
    transparent=True,
    #dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    dark=(ord(" "), (255, 255, 255), (71, 45, 60)),
    #light=(ord(" "), (255, 255, 255), (200, 180, 50)),
    light=(ord(" "), (255, 255, 255), (104, 69, 89)),
)

grass = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x25AC)), (13, 51, 26), (26, 99, 51)),
    light=(ord(chr(0x25AC)), (21, 81, 42), (36, 135, 70)),
)

flowers = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x21A8)), (255, 255, 255), (26, 99, 51)),
    light=(ord(chr(0x21A8)), (255, 255, 255), (36, 135, 70)),
)

tree1 = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(chr(0x2591)), (13, 51, 26), (26, 99, 51)),
    light=(ord(chr(0x2591)), (21, 81, 42), (36, 135, 70)),
)

oldtree = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(chr(0x2194)), (191, 121, 88), (26, 99, 51)),
    light=(ord(chr(0x2194)), (191, 121, 88), (36, 135, 70)),
)

pavement = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x2593)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0x2593)), (122, 68, 74), (71, 45, 60)),
)

stonepath = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x25BC)), (71, 45, 60), (26, 99, 51)),
    light=(ord(chr(0x25BC)), (104, 69, 89), (36, 135, 70)),
)

street = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (0, 0, 0), (0, 0, 0)),
    light=(ord(" "), (0, 0, 0), (71, 45, 60)),
)

streetline_v = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x2248)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0x2248)), (122, 68, 74), (71, 45, 60)),
)

streetline_h = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x25A0)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0x25A0)), (122, 68, 74), (71, 45, 60)),
)

streetline_c_ur = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0xB0)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0xB0)), (122, 68, 74), (71, 45, 60)),
)

streetline_c_ul = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0xA0)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0xA0)), (122, 68, 74), (71, 45, 60)),
)

streetline_c_dr = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0xB2)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0xB2)), (122, 68, 74), (71, 45, 60)),
)

streetline_c_dl = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x207F)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0x207F)), (122, 68, 74), (71, 45, 60)),
)

streetline_t_u = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x2219)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0x2219)), (122, 68, 74), (71, 45, 60)),
)

streetline_t_d = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x221A)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0x221A)), (122, 68, 74), (71, 45, 60)),
)

streetline_t_l = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0xF7)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0xF7)), (122, 68, 74), (71, 45, 60)),
)

streetline_t_r = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0x2321)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0x2321)), (122, 68, 74), (71, 45, 60)),
)

streetline_cross = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0xB7)), (73, 41, 45), (0, 0, 0)),
    light=(ord(chr(0xB7)), (122, 68, 74), (71, 45, 60)),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    #dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    dark=(ord(chr(0x2591)), (160, 153, 142), (102, 102, 102)),
    #light=(ord(" "), (255, 255, 255), (130, 110, 50)),
    light=(ord(chr(0x2591)), (160, 153, 142), (102, 102, 102)),
)

closed_door = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord(chr(0xD1)), (160, 153, 142), (71, 45, 60)),
    light=(ord(chr(0xD1)), (160, 153, 142), (104, 69, 89)),
)

open_door = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(chr(0xAA)), (160, 153, 142), (71, 45, 60)),
    light=(ord(chr(0xAA)), (160, 153, 142), (104, 69, 89)),
)

window = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(chr(0x2592)), (160, 153, 142), (102, 102, 102)),
    light=(ord(chr(0x2592)), (160, 153, 142), (102, 102, 102)),
)

fence = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(chr(0xF3)), (191, 121, 88), (26, 99, 51)),
    light=(ord(chr(0xF3)), (191, 121, 88), (26, 99, 51)),
)

water = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(chr(0x2568)), (37, 109, 135), (50, 146, 181)),
    light=(ord(chr(0x2568)), (47, 135, 168), (60, 172, 215)),
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (191, 121, 88), (71, 45, 60)),
    light=(ord(">"), (191, 121, 88), (104, 69, 89)),
)

# Wall with glyph chr(0x2550)
#wall_n = new_tile(
#    walkable=False, transparent=False, dark=(ord(chr(0x2550)), (255, 0, 0), (0, 0, 100)),
#)
