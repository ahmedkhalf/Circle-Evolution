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
        if genotype is not None:
            self.genotype = genotype
        else:
            self.genotype = np.random.rand(genes, 5)
        self.phenotype = np.zeros(size)

    def _addCircle(self, y, x, radius, color, transparency):
        rr, cc = circle(y, x, radius, self.size)
        self.phenotype[rr, cc] = self.phenotype[rr, cc] * transparency + color

    def addGene(self):
        self.genotype = np.vstack([self.genotype, np.random.rand(5)])

    def genes(self):
        # Returns number of genes
        return self.genotype.shape[0]

    def render(self):
        self.phenotype = np.zeros(self.size)
        radiusAvg = (self.size[0] + self.size[1]) / 2 / 2
        for row in self.genotype:
            self._addCircle(row[0] * self.size[0], row[1] * self.size[1],
                            row[2] * radiusAvg, row[3], row[4])


class Evolution:
    def __init__(self, size, target, genes=5, mseConstant=4):
        self.size = size  # Tuple (y, x)
        self.target = target  # Target image
        self.specie = Specie(self.size, genes=genes)

        self.maxError = (np.square((1-(self.target >= 0.5)) - self.target)).mean(axis=None)
        self.mseConstant = mseConstant

        self.generation = 1

    def mutate(self, specie):
        newSpecie = Specie(self.size, genotype=np.array(specie.genotype))

        # Select random feature in random genes
        ra = np.random.rand(newSpecie.genes(), 5) < random.uniform(0.02, 0.4)
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

    def getFitness(self, specie):
        # First apply mean squared error and map it values to max at 1
        v1 = (np.square(specie.phenotype - self.target)).mean(axis=None)
        v1 = v1 * self.mseConstant
        v1 = (self.maxError - v1) / self.maxError
        # Then apply structural similarity
        v2 = ss(specie.phenotype, self.target)
        return (v1 + v2) / 2

    def printProgress(self, fit):
        print("GEN {}, FIT {:.6f}, GENES {}".format(self.generation, fit, self.specie.genes()))

    def evolve(self, maxGenes=250, maxGeneration=100000,
               improveLen=100, improveMin=0.025, saveFreq=10000):
        improvement = []
        for i in range(maxGeneration):
            self.generation = i

            self.specie.render()
            fit = self.getFitness(self.specie)

            mutated = self.mutate(self.specie)
            mutated.render()
            newfit = self.getFitness(mutated)

            if newfit > fit:
                self.specie = mutated
                self.printProgress(newfit)
                improvement.append(1)
            else:
                improvement.append(0)

            if len(improvement) >= improveLen:
                # TODO research this vs numpy (speed)
                if sum(improvement) < improveMin:
                    improvement = []
                    if self.specie.genes() < maxGenes:
                        self.specie.addGene()
                        if self.generation > 60000:
                            self.specie.render()
                            Helper.showImage(self.specie.phenotype)
                else:
                    improvement.pop(0)


target = Helper.loadTargetImage("Images/Mona Lisa 128.jpg", (128, 128))
e = Evolution((128, 128), target, genes=150)
e.evolve(maxGenes=150, maxGeneration=20000)
e.specie.render()
Helper.showImage(e.specie.phenotype)
