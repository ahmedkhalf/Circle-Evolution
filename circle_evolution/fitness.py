import numpy as np

from skimage.metrics import structural_similarity as ss


class Fitness:
    """Base fitness class

    Attributes:
        target: target image array
    """

    def __init__(self, target):
        """Init Fitness Class"""
        self.target = target

    def score(self, phenotype):
        """Score a Specie

        Args:
            phenotype: specie image array

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
