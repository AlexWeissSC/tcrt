from __future__ import annotations

import lzma
import pickle
import color
import tcod

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from message_log import  MessageLog
import render_functions
if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld

class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player


    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.


    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored"-
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        info_pane_x = self.game_world.viewport_width
        info_pane_width = console.width - info_pane_x
        info_pane_height = self.game_world.viewport_height
        # This is debug info.  Remove it later
        info_pane_title = f'({self.player.x},{self.player.y})'
        # control info
        #info_pane_title = f'Controls'

        #Side Window
        render_functions.draw_window(console, info_pane_x, 0, info_pane_width, info_pane_height, info_pane_title)

        sub_pane_x = info_pane_x + 1
        sub_pane_width = info_pane_width - 2

        bar_pane_x = sub_pane_x
        bar_pane_y = 1
        bar_pane_width = sub_pane_width
        bar_pane_height = 5
        #render_functions.draw_window(console, bar_pane_x, bar_pane_y, bar_pane_width, bar_pane_height, '')
        console.print_box(x=sub_pane_x, y=2, width=sub_pane_width, height=1, fg=color.window_border_bright, string=f'i....Inventory',
                          alignment=tcod.CENTER)
        console.print_box(x=sub_pane_x, y=4, width=sub_pane_width, height=1, fg=color.window_border_bright,
                          string=f'o....Look around',
                          alignment=tcod.CENTER)
        console.print_box(x=sub_pane_x, y=6, width=sub_pane_width, height=1, fg=color.window_border_bright,
                          string=f'g....Pickup',
                          alignment=tcod.CENTER)
        console.print_box(x=sub_pane_x, y=8, width=sub_pane_width, height=1, fg=color.window_border_bright,
                          string=f'd....Drop',
                          alignment=tcod.CENTER)
        console.print_box(x=sub_pane_x, y=10, width=sub_pane_width, height=1, fg=color.window_border_bright,
                          string=f'c....Character information',
                          alignment=tcod.CENTER)
        console.print_box(x=sub_pane_x, y=12, width=sub_pane_width, height=1, fg=color.window_border_bright,
                          string=f'v....Message history',
                          alignment=tcod.CENTER)
        console.print_box(x=sub_pane_x, y=14, width=sub_pane_width, height=1, fg=color.window_border_bright,
                          string=f'. ....Wait',
                          alignment=tcod.CENTER)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47),
        )

        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)



