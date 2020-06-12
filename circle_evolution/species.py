"""A Specie holds information on how the trained image looks.

A specie is the basis of evolution, the genotype represents how the image looks
like, while the phnotype is the image itself.
"""

import cv2

import numpy as np


class Specie:
    """Specie defitinion for Genetic Algorithm.

    Attributes:
        size (tuple): tuple containing height and width of generated image (h, w)
        genotype (np.ndarray): array containing parameters of the specie.
            Each row in the genotype represents a circle. First column represents
            y position of circle. Second column represents x position of circle.
            Third column represents radius, fourth is color, and last column is
            transparency (alpha).
        phenotype (np.ndarray): image array of how the specie looks like when
            rendered. Call render() before accessing it.
    """

    def __init__(self, size, genes=128, genotype=None):
        """Initializes Specie with given size.

        Args:
            size (tuple): tuple containing height and width of generated image (h, w).
            genes (int): number of genes/circle in Specie. Dafaults to 128.
            genotype (np.ndarray): optional - initializes Specie with given genotype.
        """
        self.size = size
        self.genotype_width = 5 if len(size) < 3 else 7
        self.genotype = genotype if genotype is not None else np.random.rand(genes, self.genotype_width)
        self.phenotype = np.zeros(size)

    @property
    def genes(self):
        """Number of genes/circles in current Specie."""
        return self.genotype.shape[0]

    def render(self):
        """Renders image using the species definition.

        Performing the Evolution, this function renders the image for current
        iteration given the genotype. After render() is done executing, the
        Specie phenotype it set to reflect latest changes in the genotype.
        """
        self.phenotype.fill(0)
        radius_avg = (self.size[0] + self.size[1]) / 2 / 6
        for row in self.genotype:
            overlay = self.phenotype.copy()
            color = (row[3:-1] * 255).astype(int).tolist()
            cv2.circle(
                overlay,
                center=(int(row[1] * self.size[1]), int(row[0] * self.size[0])),
                radius=int(row[2] * radius_avg),
                color=color,
                thickness=-1,
            )

            alpha = row[-1]
            self.phenotype = cv2.addWeighted(overlay, alpha, self.phenotype, 1 - alpha, 0)
