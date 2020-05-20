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
        target = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        target = cv2.resize(target, size, interpolation=cv2.INTER_AREA)
        return target

    @staticmethod
    def showImage(arr):
        plt.imshow(arr, cmap='gray', vmin=0, vmax=255)
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

    def genes(self):
        # Returns number of genes
        return self.genotype.shape[0]

    def render(self):
        self.phenotype[:, :] = 0
        radiusAvg = (self.size[0] + self.size[1]) / 2 / 6
        for row in self.genotype:
            overlay = self.phenotype.copy()
            cv2.circle(overlay, (int(row[1] * self.size[1]),
                       int(row[0] * self.size[0])), int(row[2] * radiusAvg),
                       (int(row[3]*255)), -1)

            alpha = row[4]

            self.phenotype = cv2.addWeighted(overlay, alpha, self.phenotype, 1 - alpha, 0)


class Evolution:
    def __init__(self, size, target, genes=5):
        self.size = size  # Tuple (y, x)
        self.target = target  # Target image
        self.specie = Specie(self.size, genes=genes)
        self.maxError = (np.square((1-(self.target >= 127)) * 255 - self.target)).mean(axis=None)
        self.generation = 1
        self.genes = genes

    def mutate(self, specie):
        newSpecie = Specie(self.size, genotype=np.array(specie.genotype))

        y = random.randint(0, self.genes - 1)
        change = random.randint(0, 6)
        if change >= 6:
            change -= 1
            i, j = y, random.randint(0, self.genes - 1)
            i, j, s = (i, j, -1) if i < j else (j, i, 1)
            newSpecie.genotype[i:j+1] = np.roll(newSpecie.genotype[i:j+1], shift=s, axis=0)
            y = j

        selection = np.random.choice(5, size=change, replace=False)

        if random.random() < 0.25:
            newSpecie.genotype[y, selection] = np.random.rand(len(selection))
        else:
            newSpecie.genotype[y, selection] += (np.random.rand(len(selection)) - 0.5) / 3
            newSpecie.genotype[y, selection] = np.clip(newSpecie.genotype[y, selection], 0, 1)

        return newSpecie

    def getMseFitness(self, specie):
        # First apply mean squared error and map it values to max at 1
        fit = (np.square(specie.phenotype - self.target)).mean(axis=None)
        fit = (self.maxError - fit) / self.maxError
        return fit

    def getSsFitness(self, specie):
        fit = ss(specie.phenotype, self.target)
        return fit

    def printProgress(self, fit):
        print("GEN {}, FIT {:.8f}".format(self.generation, fit))

    def evolve(self, maxGeneration=100000):
        for i in range(maxGeneration):
            self.generation = i

            self.specie.render()
            fit = self.getMseFitness(self.specie)

            mutated = self.mutate(self.specie)
            mutated.render()
            newfit = self.getMseFitness(mutated)

            if newfit > fit:
                self.specie = mutated
                self.printProgress(newfit)


if __name__ == "__main__":
    target = Helper.loadTargetImage("Images/Mona Lisa 256.jpg", (128, 128))
    e = Evolution((128, 128), target, genes=256)
    e.evolve(maxGeneration=500000)
    e.specie.render()
    Helper.showImage(e.specie.phenotype)
    np.savetxt('Checkpoints/' + str(e.generation) + '.txt', e.specie.genotype)
    # 0.985634
