from components.ai import HostileEnemy, StandingEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(
    char="@",
    color=(127, 130, 147),
    name="Professor Atwood",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

""""-------NPCs-------"""

"""-------Monster-------"""

rat = Actor(
    char=chr(0x263A), #char="r",
    color=(193, 74, 44),
    name="Rat",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)


hound = Actor(
    char=chr(0x263B), #char="H",
    color=(33, 19, 13),
    name="Hound",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

"""-------Furniture-------"""

door = Actor(
    char=chr(0x2660),
    color=(191, 121, 88),
    name="Door",
    ai_cls=StandingEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=0, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0),
)

"""-------Items-------"""

confusion_scroll = Item(
    char=chr(0x2665), #char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
    char=chr(0x2665), #char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char=chr(0x2665), #char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)


"""-------Equipment-------"""

dagger = Item(
    char=chr(0x2666), color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger()
)

sword = Item(char=chr(0x2666), color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(
    char=chr(0x2663),
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char=chr(0x2663), color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail()
)