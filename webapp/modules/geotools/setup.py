
import os
import sys
from setuptools import Extension, setup
from pathlib import Path

import numpy as np
from distutils.core import Extension
from Cython.Build import cythonize

from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from distutils.command.build_ext import build_ext

# extensions = [
#     Extension(
#         "distance_calc",
#         ["geotools/distance_calc.pyx"],
#         libraries=["shp", "proj"],
#         library_dirs=["usr/lib64"],
#         include_dirs=[
#             '/usr/include',
#             np.get_include(),
#             str(Path("../../tools/cShapeTools/include/PathFinder").absolute())
#         ],
#     )
# ]

setup(
    name="geotools",
    version="0.0.1",
    # ext_modules=cythonize(extensions),
)