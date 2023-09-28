"""Responsible for evolving a specie to look like target image."""

import random

import numpy as np

from circle_evolution.species import Specie
from circle_evolution.render import CircleRenderer
import circle_evolution.fitness as fitness


class Evolution:
    """Logic for a Species Evolution.

    Use the Evolution class when you want to train a Specie to look like
    a target image.

    Attributes:
        size (tuple): tuple containing np.shape of target image.
        target (np.ndarray): target image for evolution.
        genes (int): the amount of circle to train the target image on.
        generation (int): amount of generations Evolution class has trained.
        specie (species.Specie): the Specie that is getting trained.
    """

    def __init__(self, target, genes=100):
        """Initializes Evolution class.

        Args:
            target (np.ndarray): target image for evolution.
            genes (int): the amount of circle to train the target image on.
        """
        self.size = target.shape
        self.target = target  # Target Image
        self.generation = 1
        self.genes = genes
        self.renderer = CircleRenderer((self.size[0], self.size[1]), gray=len(self.size) < 3)

        self.specie = Specie(size=self.size, renderer=self.renderer, genes=genes)

    def mutate(self, specie):
        """Mutates specie for evolution.

        Args:
            specie (species.Specie): Specie to mutate.

        Returns:
            New Specie class, that has been mutated.
        """
        new_specie = Specie(size=self.size, renderer=self.renderer, genotype=np.array(specie.genotype))

        # Randomization for Evolution
        y = random.randint(0, self.genes - 1)
        change = random.randint(0, new_specie.genotype_width + 1)

        if change >= new_specie.genotype_width + 1:
            change -= 1
            i, j = y, random.randint(0, self.genes - 1)
            i, j, s = (i, j, -1) if i < j else (j, i, 1)
            new_specie.genotype[i : j + 1] = np.roll(new_specie.genotype[i : j + 1], shift=s, axis=0)
            y = j

        selection = np.random.choice(new_specie.genotype_width, size=change, replace=False)

        if random.random() < 0.25:
            new_specie.genotype[y, selection] = np.random.rand(len(selection))
        else:
            new_specie.genotype[y, selection] += (np.random.rand(len(selection)) - 0.5) / 3
            new_specie.genotype[y, selection] = np.clip(new_specie.genotype[y, selection], 0, 1)

        return new_specie

    def print_progress(self, fit):
        """Prints progress of Evolution.

        Args:
            fit (float): fitness value of specie.
        """
        print("GEN {}, FIT {:.8f}".format(self.generation, fit))

    def evolve(self, fitness=fitness.MSEFitness, max_generation=100000):
        """Genetic Algorithm for evolution.

        Call this function to begin evolving a Specie.

        Args:
            fitness (fitness.Fitness): fitness class to score species preformance.
            max_generation (int): amount of generations to train for.
        """
        fitness = fitness(self.target)

        self.specie.render()
        fit = fitness.score(self.specie.phenotype)

        for i in range(max_generation):
            self.generation = i + 1

            mutated = self.mutate(self.specie)
            mutated.render()
            newfit = fitness.score(mutated.phenotype)

            if newfit > fit:
                fit = newfit
                self.specie = mutated
                self.print_progress(newfit)
