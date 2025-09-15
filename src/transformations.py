"""Handles the transformations"""

from srctools.bsp import BSP
from pathlib import Path
import importlib
import logging
import pkgutil

TRANSFORMATIONS: dict[str, list] = {}
LOGGER = logging.getLogger("[Transformations]")

def Transform(name: str, tags: list[str] = []):
    """Add a function to the transformations list"""
    
    if type(tags) == str:
        tags = [tags]

    def dec(func):
        func = (name, func)
        global TRANSFORMATIONS
        

        for tag in tags:
            try:
                l = TRANSFORMATIONS[tag]
                l.append(func)
            except KeyError:
                TRANSFORMATIONS[tag] = [func]
        
        return func

    LOGGER.info(f"Loading module '{name}'")

    return dec




def load_transforms(transforms_path: Path):
    for item in pkgutil.iter_modules([transforms_path]):
        importlib.import_module(transforms_path.name + "." + item.name)

def run_transforms(bsp_file: BSP, tags:list[str]):

    already_ran = set()
    for tag in tags:
        if not tag in TRANSFORMATIONS.keys():
            continue

        for name, func in TRANSFORMATIONS[tag]:
            if not name in already_ran:
                LOGGER.info(f"Running transform |{name}|")
                func(bsp_file)
                already_ran.add(name)
    