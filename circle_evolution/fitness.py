"""Fitness functions responsible for quantifying a specie's performance.

You can make your own fitness functions or use the avaible one's. For
example on making your own fitness functions, please check the available
functions in the source code.
"""

import numpy as np

from skimage.metrics import structural_similarity as ss


class Fitness:
    """Base fitness class

    The Fitness class is responsible for scoring species. You can
    make your own fitness classes by deriving from this base class.

    Attributes:
        target (np.array): target image array
    """

    def __init__(self, target):
        """Initialzes Fitness Class

        Args:
            target (np.array): target image array
        """
        self.target = target

    def score(self, phenotype):
        """Score a Specie

        Args:
            phenotype (np.array): specie image array

        Returns:
            float value, bigger number means better performance

        Raises:
            NotImplementedError: if it has not been overwritten
        """
        raise NotImplementedError


class MSEFitness(Fitness):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_error = (np.square((1 - (self.target >= 127)) * 255 - self.target)).mean(axis=None)

    def score(self, phenotype):
        """Calculates Mean Square Error Fitness for a specie"""
        fit = (np.square(phenotype - self.target)).mean(axis=None)
        fit = (self._max_error - fit) / self._max_error
        return fit


class SSFitness(Fitness):
    def score(self, phenotype):
        """Calculates SS Fitness for a specie"""
        fit = ss(phenotype, self.target)
        return fit
