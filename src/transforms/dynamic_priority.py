from transformations import Transform

from srctools import Entity, conv_int, Vec
from srctools.bsp import BSP
import logging

LOGGER = logging.getLogger("[Transform][Dynamic Priority]")

@Transform("Dynamic Priority - Part 2", ["after_vrad"])
def dynamic_priority(bsp: BSP):

    light: Entity

    # These lights are changed so that VRAD doesn't assign lightmap pages for them.

    for light in bsp.ents.by_class["_dynpr_rt_spot"]:
        light["classname"] = "light_rt_spot"

    for light in bsp.ents.by_class["_dynpr_rt"]:
        light["classname"] = "light_rt"