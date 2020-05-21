import random

import numpy as np

from skimage.metrics import structural_similarity as ss

from circle_evolution.species import Specie


class Evolution:
    """Logic for a Species Evolution.

    Attributes:
        size:
        target:
        genes:
    """

    def __init__(self, size, target, genes=5):
        """Inits Evolution"""
        self.size = size  # Tuple (y, x)
        self.target = target  # Target Image
        self.generation = 1
        self.genes = genes

        self.specie = Specie(size=self.size, genes=genes)
        self.max_error = (np.square((1 - (self.target >= 127)) * 255 - self.target)).mean(axis=None)

    def mutate(self, specie):
        """Mutates specie for evolution"""
        new_specie = Specie(size=self.size, genotype=np.array(specie.genotype))

        # Randomization for Evolution
        y = random.randint(0, self.genes - 1)
        change = random.randint(0, 6)

        if change >= 6:
            change -= 1
            i, j = y, random.randint(0, self.genes - 1)
            i, j, s = (i, j, -1) if i < j else (j, i, 1)
            new_specie.genotype[i : j + 1] = np.roll(new_specie.genotype[i : j + 1], shift=s, axis=0)
            y = j

        selection = np.random.choice(5, size=change, replace=False)

        if random.random() < 0.25:
            new_specie.genotype[y, selection] = np.random.rand(len(selection))
        else:
            new_specie.genotype[y, selection] += (np.random.rand(len(selection)) - 0.5) / 3
            new_specie.genotype[y, selection] = np.clip(new_specie.genotype[y, selection], 0, 1)

        return new_specie

    def get_mse_fitness(self, specie):
        """Calculates MSE Fitness for a specie"""
        # First apply mean squared error and map it values to max at 1
        fit = (np.square(specie.phenotype - self.target)).mean(axis=None)
        fit = (self.max_error - fit) / self.max_error
        return fit

    def get_ss_fitness(self, specie):
        """Calculates SS Fitness for a specie"""
        fit = ss(specie.phenotype, self.target)
        return fit

    def print_progress(self, fit):
        """Progress of Evolution - Current iterations"""
        print("GEN {}, FIT {:.8f}".format(self.generation, fit))

    def evolve(self, max_generation=100000):
        """Genetic Algorithm for evolution"""
        for i in range(max_generation):
            self.generation = i

            self.specie.render()

            fit = self.get_mse_fitness(self.specie)

            mutated = self.mutate(self.specie)
            mutated.render()
            newfit = self.get_mse_fitness(mutated)

            if newfit > fit:
                self.specie = mutated
                self.print_progress(newfit)
