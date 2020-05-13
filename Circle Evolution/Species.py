from skimage.metrics import structural_similarity as ss
from skimage.draw import circle
import matplotlib.pyplot as plt
import numpy as np
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
        self.img = np.zeros(size)
        self.genotype = np.random.rand(150, 4)

    def addCircle(self, y, x, radius, adder):
        rr, cc = circle(y, x, radius, self.size)
        self.img[rr, cc] += adder

    def render(self):
        radiusAvg = (self.size[0] + self.size[1]) / 2 / 2
        for row in self.genotype:
            self.addCircle(row[0] * self.size[0], row[1] * self.size[1],
                           row[2] * radiusAvg, row[3])

    def getFitness(self, target):
        return ss(self.img, target)


s = Specie((64, 64))
s.render()

Helper.showImage(s.img)
