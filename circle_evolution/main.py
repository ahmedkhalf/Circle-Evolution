import argparse

import numpy as np

from circle_evolution.evolution import Evolution

import circle_evolution.helpers as helpers


def main():
    """Entrypoint of application"""
    parser = argparse.ArgumentParser(description="Circle Evolution CLI")

    parser.add_argument("image", type=str, help="Image to be processed")
    size_options = {1: (64, 64), 2: (128, 128), 3: (256, 256)}
    parser.add_argument("size", choices=size_options.keys(), default=2, help="Dimension of the image")
    parser.add_argument("--genes", default=256, type=int, help="Number of genes")
    parser.add_argument("--max-generations", type=int, default=500000)
    args = parser.parse_args()

    target = helpers.load_target_image(args.image, size_options[args.size])

    evolution = Evolution(size_options[args.size], target, genes=args.genes)
    evolution.evolve(max_generation=args.max_generation)

    evolution.specie.render()

    helpers.show_image(evolution.specie.phenotype)

    output_path_checkpoint = "checkpoint-{}.txt".format(evolution.generation)
    np.savetxt(output_path_checkpoint, evolution.specie.genotype)


if __name__ == "__main__":
    main()
