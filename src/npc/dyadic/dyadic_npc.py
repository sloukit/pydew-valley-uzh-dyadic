from dataclasses import dataclass, field
from math import isnan
from typing import Callable

import numpy as np
import pygame

from src.enums import FarmingTool, SeedType, Color
from src.gui.interface import NPCEmoteManager
from src.npc.behaviour.ai_behaviour_tree_base import Context
from src.npc.npc import NPC
from src.overlay.soil import SoilManager
from src.settings import Coordinate
from src.sprites.entities.character import Character
from src.sprites.setup import EntityAsset


class DyadicNPC(NPC):
    partner: Character | None = None

    def __init__(self, pos: Coordinate, assets: EntityAsset, groups: tuple[pygame.sprite.Group, ...],
                 collision_sprites: pygame.sprite.Group,
                 apply_tool: Callable[[FarmingTool, tuple[float, float], Character], None],
                 plant_collision: Callable[[Character], None], soil_manager: SoilManager,
                 emote_manager: NPCEmoteManager, tree_sprites: pygame.sprite.Group,
                 special_features: str | None,
                 is_dyad_main: bool,
                 partner_id: int,
                 npc_id: int = 0,
                 is_v3: bool = False,
                 hat: Color | None = None,
                 necklace: Color | None = None,
                 ):
        super().__init__(pos, assets, groups, collision_sprites, apply_tool, plant_collision, soil_manager,
                         emote_manager, tree_sprites, special_features, npc_id, is_v3, hat, necklace)
        self.is_dyad_main = is_dyad_main
        self.partner_id = partner_id



    def follow_partner(self):
        current = np.asarray(self.get_tile_pos())
        partner = np.asarray(self.partner.get_tile_pos())
        direction = current - partner
        length = np.linalg.norm(direction)
        target = partner + direction / length * 1 # stay 1 tile away from partner
        x, y = target
        if not isnan(x) and not isnan(y):
            self.create_path_to_tile((int(x), int(y)))



@dataclass
class DyadicNPCContext(Context):
    npc: DyadicNPC
    # list of available seeds depending on game version and round number
    allowed_seeds: list[SeedType] = field(default_factory=list)
    adhering_to_measures: bool = field(default=False)
    timing_for_bathhouse: float = field(default=0.0)
    going_to_bathhouse: bool = field(default=False)

    def set_behaviour(self, new_behaviour):
        self.npc.conditional_behaviour_tree = new_behaviour
