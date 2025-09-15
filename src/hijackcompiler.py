from sys import argv, stdout, exit
from pathlib import Path
import logging
from logging import FileHandler
from transformations import run_transforms, load_transforms

import argparse

from srctools.bsp import BSP


OUR_PATH = Path(argv[0]).parent
TRANSFORMS_PATH = OUR_PATH / "transforms"

def main():
    parser = argparse.ArgumentParser("HijackCompiler", description="A simple tool used to run postcompiler-like transforms in each compilation step.")

    parser.add_argument("map")

    parser.add_argument(
        "tags",
        action="extend",
        nargs=argparse.REMAINDER,
        default=[]
        )

    
    result = parser.parse_args(argv[1:])

    map_file = Path(result.map)
    
    handlers = [logging.StreamHandler(stdout), 
                FileHandler(map_file.with_suffix(".log"))]
    
    logging.basicConfig(handlers=handlers, level=logging.INFO)
    LOGGER = logging.getLogger("[Main]")

    LOGGER.info("HijackCompiler started.")

    LOGGER.info(f"Loading map file: {map_file}")

    if not map_file.suffix == ".bsp":
        LOGGER.error(f"Unsupported file type: {map_file.suffix}")
        exit(1)


    loaded_map = BSP(map_file)

    LOGGER.info("Loaded!")
    LOGGER.info(f"Loading transforms from {TRANSFORMS_PATH}")

    load_transforms(TRANSFORMS_PATH)

    tags = [x.casefold() for x in result.tags]

    LOGGER.info(f"Running transforms with tags: {tags}")

    run_transforms(loaded_map, tags)

    LOGGER.info("Finished! Saving map...")
    loaded_map.save()



    


if __name__ == "__main__":
    main()
