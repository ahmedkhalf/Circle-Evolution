"""CLI for Circle Evolution"""

import argparse

import numpy as np

from circle_evolution.evolution import Evolution

import circle_evolution.helpers as helpers


def main():
    """Entrypoint of application"""
    parser = argparse.ArgumentParser(description="Circle Evolution CLI")

    parser.add_argument("image", type=str, help="Image to be processed")
    parser.add_argument("--genes", default=256, type=int, help="Number of genes")
    parser.add_argument("--max-generations", type=int, default=500000)
    args = parser.parse_args()

    target = helpers.load_target_image(args.image)

    evolution = Evolution(target.shape, target, genes=args.genes)
    evolution.evolve(max_generation=args.max_generations)

    evolution.specie.render()

    helpers.show_image(evolution.specie.phenotype)

    output_path_checkpoint = "checkpoint-{}.txt".format(evolution.generation)
    np.savetxt(output_path_checkpoint, evolution.specie.genotype)


if __name__ == "__main__":
    main()
