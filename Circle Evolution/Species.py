from skimage.metrics import structural_similarity as ss
from skimage.draw import circle
import matplotlib.pyplot as plt
import numpy as np
import random
import cv2


class Helper:
    @staticmethod
    def loadTargetImage(directory, size):
        img = cv2.imread(directory)
        target = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) / 255
        target = cv2.resize(target, size, interpolation=cv2.INTER_AREA)
        return target

    @staticmethod
    def showImage(arr):
        plt.imshow(arr, cmap='gray', vmin=0, vmax=1)
        plt.show()


class Specie:
    def __init__(self, size, genes=5, genotype=None):
        self.size = size
        if genotype:
            self.genotype = genotype
        else:
            self.genotype = np.random.rand(genes, 4)
        self.phenotype = np.zeros(size)

    def _addCircle(self, y, x, radius, adder):
        rr, cc = circle(y, x, radius, self.size)
        self.phenotype[rr, cc] += adder

    def addGene(self):
        self.genotype = np.vstack(self.genotype, np.random.rand(4))

    def genes(self):
        # Returns number of genes
        return self.genotype.shape[0]

    def render(self):
        self.phenotype = np.zeros(self.size)
        radiusAvg = (self.size[0] + self.size[1]) / 2 / 2
        for row in self.genotype:
            self._addCircle(row[0] * self.size[0], row[1] * self.size[1],
                            row[2] * radiusAvg, row[3])


class Evolution:
    def __init__(self, settings):
        self.size = settings["size"]  # Tuple (y, x)
        self.target = settings["target"]  # Target image
        self.specie = Specie(self.size)
        self.bestfit = -99999
        self.generation = 1

    def mutate(self, specie):
        newSpecie = Specie(self.size, genotype=specie.genotype)

        # Select random feature in random genes
        ra = np.random.rand(newSpecie.genes(), 4) < random.uniform(0.02, 0.4)
        # Get selection scope
        scope = np.random.rand(len(newSpecie.genotype[ra]))

        if random.random() < 0.25:
            # 25% Complete replacement
            newSpecie.genotype[ra] = scope
        else:
            # 75% Soft adition
            newSpecie.genotype[ra] += (scope - 0.5) / random.randint(4, 12)

        newSpecie.genotype[ra] = np.clip(newSpecie.genotype[ra], 0, 1)
        return newSpecie

    def getFitness(self, target):
        if self.maxError is None:
            self.maxError = (np.square((1-(target >= 0.5)) - target)).mean(axis=None)
        v1 = (np.square(self.phenotype - target)).mean(axis=None)
        v1 = (self.maxError - v1) / self.maxError
        v2 = ss(self.phenotype, target)
        return (v1 + v2) / 2
