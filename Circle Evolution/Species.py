from skimage.metrics import structural_similarity as ss
from skimage.draw import circle
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
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
    def __init__(self, size):
        self.size = size
        self.genotype = np.random.rand(150, 4)
        self.phenotype = np.zeros(size)

    def addCircle(self, y, x, radius, adder):
        rr, cc = circle(y, x, radius, self.size)
        self.phenotype[rr, cc] += adder

    def render(self):
        radiusAvg = (self.size[0] + self.size[1]) / 2 / 2
        for row in self.genotype:
            self.addCircle(row[0] * self.size[0], row[1] * self.size[1],
                           row[2] * radiusAvg, row[3])

    def getFitness(self, target):
        return (np.square(self.phenotype - target)).mean(axis=None)
        # return ss(self.phenotype, target)


class Evolution:
    def __init__(self, target, settings):
        self.target = target
        self.settings = settings
        self.species = [Specie((64, 64)) for x in range(1)]
        self.bestfit = 99999
        self.evolution = 1

    def mutate(self, specie):
        ns = copy.deepcopy(specie)
        ra = np.random.rand(150, 4) < random.uniform(0.02, 0.3)
        if random.random() > 0.5:
            ns.genotype[ra] = np.random.rand(len(ns.genotype[ra]))
        else:
            ns.genotype[ra] += (np.random.rand(len(ns.genotype[ra])) - 0.5) / 10
        ns.genotype[ra] = np.clip(ns.genotype[ra], a_min=0, a_max=1)
        return ns

    def evolve(self):
        # Go to next generation
        for specie in self.species:
            specie.render()
            fit = specie.getFitness(self.target)
            if abs(fit) < self.bestfit:
                print(self.evolution, '{0:.16f}'.format(fit))
                self.bestfit = abs(fit)

            specie.phenotype = np.zeros((64, 64))

            ns = self.mutate(specie)
            ns.render()
            nfit = ns.getFitness(self.target)

            if abs(nfit) < abs(fit):
                self.species[0] = ns
                self.species[0].phenotype = np.zeros((64, 64))
        self.evolution += 1
        if self.evolution % 10000 == 0:
            np.savetxt('Checkpoints/' + str(self.evolution) + '.txt',
                       self.species[0].genotype, fmt='%d')


target = Helper.loadTargetImage("Images/Mona Lisa 64.jpg", (64, 64))
e = Evolution(target, None)
while True:
    e.evolve()
