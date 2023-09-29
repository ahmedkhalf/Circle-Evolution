"""CLI for Circle Evolution"""

import argparse

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
    parser.add_argument("-c", "--checkpoint", type=str, default=None)
    parser.add_argument("-l", "--load-checkpoint", type=str, default=None)
    parser.add_argument("-o", "--output-width", type=int, default=None)
    args = parser.parse_args()

    target = helpers.load_target_image(args.image, size=args.width)
    print(f"Image loaded at resolution: {target.shape[1]}x{target.shape[0]}")

    evolution = Evolution(target, genes=args.genes)
    print(f"Using GPU '{evolution.renderer.gpu_name}'")

    starting_generation = 0
    if args.load_checkpoint is not None:
        evolution.specie.load_checkpoint(args.load_checkpoint)
        hyphen_index = args.load_checkpoint.rfind("-")
        dot_index = args.load_checkpoint.rfind(".")
        if hyphen_index != -1 and dot_index != -1:
            try:
                starting_generation = int(args.load_checkpoint[hyphen_index + 1:dot_index])
            except ValueError:
                starting_generation = 0

    if args.max_generations > 0:
        try:
            evolution.evolve(max_generation=args.max_generations)
        except KeyboardInterrupt:
            print("\nEvolution interrupted by user.")
        else:
            print("")

    if args.output_width is not None:
        target = helpers.load_target_image(args.image, size=args.output_width)
        out_evolution = Evolution(target, genes=args.genes)
        out_evolution.specie.genotype = evolution.specie.genotype
        out_evolution.specie.render()
        helpers.show_image(out_evolution.specie.phenotype)
    else:
        evolution.specie.render()
        helpers.show_image(evolution.specie.phenotype)

    if args.checkpoint:
        output_path_checkpoint = f"{args.checkpoint}-{starting_generation + evolution.generation}.txt"
        evolution.specie.save_checkpoint(output_path_checkpoint)


if __name__ == "__main__":
    main()
