"""A Specie holds information on how the trained image looks.

A specie is the basis of evolution, the genotype represents how the image looks
like, while the phnotype is the image itself.
"""

import numpy as np

from circle_evolution.render import CircleRenderer


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

    def __init__(self, size, renderer: CircleRenderer, genes=128, genotype=None):
        """Initializes Specie with given size.

        Args:
            size (tuple): tuple containing width and height of generated image (w, h).
            genes (int): number of genes/circle in Specie. Dafaults to 128.
            genotype (np.ndarray): optional - initializes Specie with given genotype.
        """
        self.size = size
        self.genotype_width = 5 if len(size) < 3 else 7
        self.genotype = genotype if genotype is not None else np.random.rand(genes, self.genotype_width)
        self.phenotype = np.zeros(size, dtype=np.uint8)
        self.renderer = renderer

    @property
    def genes(self):
        """Number of genes/circles in current Specie."""
        return self.genotype.shape[0]

    def render(self):
        radius_avg = (self.size[0] + self.size[1]) / 2 / 3

        self.phenotype = self.renderer.render(
            self.genes,
            self.genotype[:, 0:2] * (self.size[1], self.size[0]),
            self.genotype[:, 2] * radius_avg,
            self.genotype[:, [3, 3, 3, 4]] if self.genotype_width == 5 else self.genotype[:, 3:7]
        )

    def save_checkpoint(self, fname, text=True):
        """Save genotype to a checkpoint.

        Args:
            fname: the file you would like to save to.
            text (bool): whether to save as text or numpy format. Default: False
        """
        if text:
            np.savetxt(fname, self.genotype)
        else:
            np.save(fname, self.genotype)

    def load_checkpoint(self, fname, text=True):
        """Load genotype from a checkpoint.

        Args:
            fname: the file you would like to load from.
            text (bool): whether to load as text or numpy format. Default: False
        """
        if text:
            self.genotype = np.loadtxt(fname, dtype=np.float64)
        else:
            self.genotype = np.load(fname)
