from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import color
import tcod

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width =  int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )

def render_dungeon_level(
    console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")

def render_names_at_mouse_location(console, x, y, engine):
  mouse_x, mouse_y = engine.mouse_location
  # Translate mouse location for viewport
  viewport = engine.game_map.get_viewport()
  map_x = mouse_x + viewport[0]
  map_y = mouse_y + viewport[1]
  names_at_mouse_location = get_names_at_location(x=map_x,y=map_y,game_map=engine.game_map)
  if names_at_mouse_location:
    # Figure out where to render the tool tip.  Make sure we
    # render inside the console bounds
    x = mouse_x - (len(names_at_mouse_location) // 2) - 1
    if x < 0:
      x = 0
    elif x + len(names_at_mouse_location) + 2 > console.width - 1:
      x = console.width - len(names_at_mouse_location) - 3

    if mouse_y <= 3:
      y = mouse_y + 1
    else:
      y = mouse_y - 3

    draw_window(console, x, y, len(names_at_mouse_location) + 2, 3,'')


    console.print(x=x+1,y=y+1, string=names_at_mouse_location)



def draw_window(console, x, y, width, height, title):
  console.draw_frame(
      x=x,
      y=y,
      width=width,
      height=height,
      title='',
      clear=True,
      fg=(255, 255, 255), #color.window_border_dark,
      bg=(0, 0, 0),
  )

  r_bright, g_bright, b_bright = color.window_border_bright
  r_dark, g_dark, b_dark = color.window_border_dark
  #r_step = (r_bright - r_dark) // 10
  #g_step = (g_bright - g_dark) // 10
  #b_step = (b_bright - b_dark) // 10
  x1 = x + width - 1
  y1 = y + height - 1
  #print(f'Step values: {r_step},{g_step},{b_step}')
  for i in range(0, 11):
    r = 255 #r_dark #+ (r_step * i)
    g = 255 #g_dark #+ (g_step * i)
    b = 255 #b_dark #+ (b_step * i)
    #print(f'({x+i},{y+i}) = {r}, {g}, {b}')
    # Horizontal lines
    if i <= width // 2:
      console.tiles_rgb['fg'][x+i,y] = (r,g,b)
      console.tiles_rgb['fg'][x1-i,y] = (r,g,b)
      console.tiles_rgb['fg'][x1-i,y1] = (r,g,b)
      console.tiles_rgb['fg'][x+i,y1] = (r,g,b)

    # Vertical lines
    if i <= height // 2:
      console.tiles_rgb['fg'][x,y+i] = (r,g,b)
      console.tiles_rgb['fg'][x1,y+i] = (r,g,b)
      console.tiles_rgb['fg'][x1,y1-i] = (r,g,b)
      console.tiles_rgb['fg'][x,y1-i] = (r,g,b)

  if title:
    console.print_box(x=x, y=y, width=width, height=1, fg=color.window_border_dark, string=f'┤{title}├', alignment=tcod.CENTER)
