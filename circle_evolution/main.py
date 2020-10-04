"""CLI for Circle Evolution"""

import argparse

import numpy as np

from circle_evolution import __version__
from circle_evolution.evolution import Evolution

import circle_evolution.helpers as helpers


SIZE_OPTIONS = {1: (64, 64), 2: (128, 128), 3: (256, 256), 'auto': None}


def main():
    """Entrypoint of application"""
    parser = argparse.ArgumentParser(description=f"Circle Evolution CLI v{__version__}")

    parser.add_argument("image", type=str, help="Image to be processed")
    parser.add_argument("--size", choices=SIZE_OPTIONS.keys(), default='auto', help="Dimension of the image")
    parser.add_argument("--genes", default=256, type=int, help="Number of genes")
    parser.add_argument("--max-generations", type=int, default=500000)
    args = parser.parse_args()

    target = helpers.load_target_image(args.image, size=SIZE_OPTIONS[args.size])

    evolution = Evolution(target, genes=args.genes)
    evolution.evolve(max_generation=args.max_generations)

    evolution.specie.render()
    evolution.specie.show_img()

    output_path_checkpoint = "checkpoint-{}.txt".format(evolution.generation)
    np.savetxt(output_path_checkpoint, evolution.specie.genotype)


if __name__ == "__main__":
    main()
