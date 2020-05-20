import cv2

import numpy as np


class Specie:
    """Specie defitinion for Genetic Algorithm.

    Attributes:
        size:
        genes:
        genotype:
    """

    def __init__(self, size, genes=5, genotype=None):
        """Inits Specie with given size."""
        self.size = size
        self.genotype = genotype if genotype is not None else np.random.rand(genes, 5)
        self.phenotype = np.zeros(size)

    @property
    def genes(self):
        """Number of genes in current Species."""
        # Returns number of genes
        return self.genotype.shape[0]

    def render(self):
        """Renders image using the species definition.

        Performing the Evolution, this function renders the image for current
        iteration given the genotype and phenotype.
        """
        self.phenotype[:, :] = 0
        radius_avg = (self.size[0] + self.size[1]) / 2 / 6
        for row in self.genotype:
            overlay = self.phenotype.copy()
            cv2.circle(
                overlay,
                center=(int(row[1] * self.size[1]), int(row[0] * self.size[0])),
                radius=int(row[2] * radius_avg),
                color=(int(row[3] * 255)),
                thickness=-1,
            )

            alpha = row[4]
            self.phenotype = cv2.addWeighted(overlay, alpha, self.phenotype, 1 - alpha, 0)
