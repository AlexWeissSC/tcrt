from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

import engine # for tiles

import tcod

import entity_factories

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

max_items_by_floor = [
    (1, 3),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

max_doors_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.health_potion, 5), (entity_factories.fireball_scroll, 5), (entity_factories.bookcase, 90)],
    2: [(entity_factories.confusion_scroll, 10)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.sword, 5)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.rat, 80)],
    3: [(entity_factories.hound, 15)],
    5: [(entity_factories.hound, 30)],
    7: [(entity_factories.hound, 60)],
}

door_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.wooden_door, 100)],
    3: [(entity_factories.metal_door, 100)],
    5: [(entity_factories.wooden_door, 100)],
    7: [(entity_factories.wooden_door, 100)],
}
def get_max_value_for_floor(
    max_value_by_floor: List[Tuple[int, int]], floor: int
) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value

def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities

class RectangularRoom:

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property

    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 +1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int,) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def place_doors(room: RectangularRoom, dungeon: GameMap, floor_number: int,) -> None:
    number_of_doors = 3#random.randint(
        #0, get_max_value_for_floor(max_doors_by_floor, floor_number)
    #)

    doors: List[Entity] = get_entities_at_random(
        door_chances, number_of_doors, floor_number
    )

    for entity in doors:
        x = int # random.randint(room.x1, room.x2)
        y = int # random.randint(room.y1, room.y2)

        x1 = room.x1
        x2 = room.x2
        y1 = room.y1
        y2 = room.y2
        width = x2 - x1
        height = y2 - x1

        x = int((x1 + x2) / 2) #x1
        y = y1
        #center_x = int((self.x1 + self.x2) / 2)
        #center_y = int((self.y1 + self.y2) / 2)
        #if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.

        #if engine.GameMap.tiles["walkable"][x, y]:
            # Destination is blocked by a tile.
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)
            dungeon.tiles[x, y] = tile_types.closed_door

def place_open_doors(dungeon: GameMap, x: int, y: int) -> None:
    dungeon.tiles[x, y] = tile_types.open_door

def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int],
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
        # roomexit y1 x1+width/2
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2
        # roomexit x1 y1+height/2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def draw_street(
    start: Tuple[int, int], end: Tuple[int, int],
) -> Iterator[Tuple[int, int]]:
    #"""Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
        # roomexit y1 x1+width/2
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2
        # roomexit x1 y1+height/2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])


    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.game_world.current_floor)
        place_doors(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon

def generate_arkham(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for r in range(max_rooms):
        room_width = 10#10
        room_height = 15#15

        x = 20 + r
        y = 15

        new_x = x + room_width
        new_y = y + room_height

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)
        #new_room = RectangularRoom(x+9, y+10, room_width, room_height)

        #new street horizontal
        dungeon.tiles[10:70, 30] = tile_types.pavement
        dungeon.tiles[10:70, 31] = tile_types.street
        dungeon.tiles[10:70, 32] = tile_types.streetline_h
        #dungeon.tiles[12, 32] = tile_types.streetline_t_u
        dungeon.tiles[10:70, 33] = tile_types.street
        dungeon.tiles[10:70, 34] = tile_types.pavement

        #new street vertival
        dungeon.tiles[10, 10:34] = tile_types.pavement
        dungeon.tiles[11, 10:31] = tile_types.street
        dungeon.tiles[12, 10:32] = tile_types.streetline_v
        dungeon.tiles[13, 10:31] = tile_types.street
        dungeon.tiles[14, 10:31] = tile_types.pavement

        # new street horizontal
        dungeon.tiles[10:70, 10] = tile_types.pavement
        dungeon.tiles[10:70, 11] = tile_types.street
        dungeon.tiles[10:70, 12] = tile_types.streetline_h
        #dungeon.tiles[12, 12] = tile_types.streetline_t_d
        dungeon.tiles[10:70, 13] = tile_types.street
        dungeon.tiles[10:70, 14] = tile_types.pavement
        #dungeon.tiles[12, 13] = tile_types.streetline_v

        # new street vertikal
        dungeon.tiles[66, 10:35] = tile_types.pavement
        dungeon.tiles[67, 10:35] = tile_types.street
        dungeon.tiles[68, 10:35] = tile_types.streetline_v
        dungeon.tiles[69, 10:35] = tile_types.street
        dungeon.tiles[70, 10:35] = tile_types.pavement

        # new corner ul

        dungeon.tiles[66:71, 30:35] = tile_types.pavement
        dungeon.tiles[67:70, 30:34] = tile_types.street
        dungeon.tiles[66:70, 31:34] = tile_types.street
        dungeon.tiles[68, 30:32] = tile_types.streetline_v
        dungeon.tiles[66:68, 32] = tile_types.streetline_h
        dungeon.tiles[68, 32] = tile_types.streetline_c_ul

        # new corner dl
        dungeon.tiles[66:71, 10:15] = tile_types.pavement
        dungeon.tiles[67:70, 11:15] = tile_types.street
        dungeon.tiles[66:70, 11:14] = tile_types.street
        dungeon.tiles[68, 12:15] = tile_types.streetline_v
        dungeon.tiles[66:68, 12] = tile_types.streetline_h
        dungeon.tiles[68, 12] = tile_types.streetline_c_dl

        # new corner dr
        dungeon.tiles[10:15, 10:15] = tile_types.pavement
        dungeon.tiles[11:14, 11:15] = tile_types.street
        dungeon.tiles[11:15, 11:14] = tile_types.street
        dungeon.tiles[12, 13:15] = tile_types.streetline_v
        dungeon.tiles[12:15, 12] = tile_types.streetline_h
        dungeon.tiles[12, 12] = tile_types.streetline_c_dr

        # new corner dr
        dungeon.tiles[10:15, 30:34] = tile_types.pavement
        dungeon.tiles[11:14, 30:34] = tile_types.street
        dungeon.tiles[11:15, 31:34] = tile_types.street
        dungeon.tiles[12:15, 32] = tile_types.streetline_h
        dungeon.tiles[12, 30:32] = tile_types.streetline_v
        dungeon.tiles[12, 32] = tile_types.streetline_c_ur

        #grass
        dungeon.tiles[15:20, 15:30] = tile_types.grass
        entity_factories.health_potion.spawn(dungeon, 15, 15)

        #flower
        dungeon.tiles[17, 16] = tile_types.flowers
        dungeon.tiles[19, 17:20] = tile_types.flowers

        #windows
        dungeon.tiles[20, 18] = tile_types.window

        #fence
        dungeon.tiles[15:20, 29] = tile_types.fence

        # grass
        dungeon.tiles[10:70, 35] = tile_types.grass

        #water
        dungeon.tiles[10:70, 36:40] = tile_types.water





        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.game_world.current_floor)
        place_doors(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        # Finally, append the new room to the list.
        rooms.append(new_room)


    return dungeon
