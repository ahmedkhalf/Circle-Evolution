"""
# Welcome to Circle Evolution's Documentation

<p>
    <img alt="Circle Evolution Logo" src="images/logo.png" width="400">
</p>

# Know your terminology

A specie in Circle Evolution is the object we are optimizing.
A specie has both a genotype and a phenotype.

The specie's genotype tells the renderer how the circles should be rendered.

The specie's phenotype is the rendered image itself.

# Getting Started
## Installation

Clone or download this repository then run this command in the root folder
```bash
python setup.py install
```

## Usage
### Command Line

You can easily start training an image by calling circle_evolution from your terminal

**Example:**
```bash
circle_evolution "Mona Lisa 64.jpg" --size 1 --genes 256 --max-generations 50000
```

| Parameter         | Description                                                          |
| ----------------- | -------------------------------------------------------------------- |
| --size            | Image size {1: (64, 64), 2: (128, 128), 3: (256, 256)}. *Default: 2* |
| --genes           | Number of circle to fit. *Default: 256*                              |
| --max-generations | Number of generations to run. *Default: 500,000*                     |

### Python Example Scripts

This script is the equivalent of running the command mentioned above.

```python
from circle_evolution import evolution
from circle_evolution import helpers
import numpy as np
import cv2

# Load target image of size (64, 64)
target = helpers.load_target_image("Mona Lisa 64.jpg", size=(64, 64))

# Setup evolution
e = evolution.Evolution(target, genes=256)

# Evolve for 50k generations
e.evolve(max_generation=50000)

# Show evolved phenotype
helpers.show_image(e.specie.phenotype)

# Saves genotype to checkpoint
np.savetxt("Checkpoint.txt", e.specie.genotype)

# Saves phenotype
cv2.imwrite("OuputImage.jpg", e.specie.phenotype)
```

Here is how to load and train further from a saved checkpoint.

```python
from circle_evolution import evolution
from circle_evolution import helpers
import numpy as np
import cv2

# Load target image of size (64, 64)
target = helpers.load_target_image("Mona Lisa 64.jpg", size=(64, 64))

# Setup evolution
e = evolution.Evolution(target, genes=256)

# Load from checkpoint
genes = np.loadtxt("Checkpoint.txt")
e.specie.genotype = genes

# Evolve for 50k generations
e.evolve(max_generation=50000)

# Show evolved phenotype
helpers.show_image(e.specie.phenotype)
```

# Contributing

Pull requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.
"""

__version__ = "0.1"
