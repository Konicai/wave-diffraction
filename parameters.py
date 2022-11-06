from dataclasses import dataclass
from typing import Set
from PIL import Image

from ursina import *

@dataclass
class Parameters:
    tick_distance: float = 1

    wavelength: float = 500
    brightnessFactor: float = 1

    
    occluder: Image = Image.open("images/2slit.png")
    
    visualizerAmount: int = 1

    detectorDistance: float = 3

    lowResolution: int = 64  # For all planes in time simulation
    highResolution: int = 128  # For all planes in final state simulation

    def initParams():
        Instance = Parameters()

Instance: Parameters = None