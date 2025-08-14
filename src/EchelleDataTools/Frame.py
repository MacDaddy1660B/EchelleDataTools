#!/usr/bin/env python3

import astropy.io.fits as fits
from dataclasses import dataclass, field
import numpy as np


@dataclass(kw_only=True)
class BaseFrame:
    data : np.ndarray = field(repr=False)
    name : str = None


@dataclass(kw_only=True)
class Frame(BaseFrame):
    header : fits.Header = field(repr=False)


@dataclass(kw_only=True)
class SuperFrame(BaseFrame):
    biasSubtracted : bool = None
    darkSubtracted : bool = None
    combineMethod : str = 'median'
