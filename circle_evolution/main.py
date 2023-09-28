"""CLI for Circle Evolution"""

import argparse

import numpy as np

from circle_evolution import __version__
from circle_evolution.evolution import Evolution

import circle_evolution.helpers as helpers


def main():
    """Entrypoint of application"""
    parser = argparse.ArgumentParser(description=f"Circle Evolution CLI v{__version__}")

    parser.add_argument("image", type=str, help="Image to be processed")
    parser.add_argument("-w", "--width", type=int, default='auto', help="Width of the image used while training")
    parser.add_argument("-g", "--genes", type=int, default=128, help="Number of genes / circles")
    parser.add_argument("-m", "--max-generations", type=int, default=50000)
    args = parser.parse_args()

    print(args.width)

    target = helpers.load_target_image(args.image, size=args.width)
    print(f"Image loaded at resolution: {target.shape[1]}x{target.shape[0]}")

    evolution = Evolution(target, genes=args.genes)
    print(f"Using GPU '{evolution.renderer.gpu_name}'")

    evolution.evolve(max_generation=args.max_generations)

    evolution.specie.render()
    helpers.show_image(evolution.specie.phenotype)

    output_path_checkpoint = "checkpoint-{}.txt".format(evolution.generation)
    np.savetxt(output_path_checkpoint, evolution.specie.genotype)


if __name__ == "__main__":
    main()
