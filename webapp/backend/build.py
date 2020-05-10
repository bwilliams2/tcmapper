import os
import sys
from pathlib import Path

import numpy as np
from distutils.core import Extension
from Cython.Build import cythonize

from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from distutils.command.build_ext import build_ext

extensions = [
    Extension(
        "distance_calc",
        ["backend/geotools/distance_calc.pyx"],
        libraries=["shp", "proj"],
        library_dirs=["usr/lib64"],
        include_dirs=[
            '/usr/include',
            np.get_include(),
            str(Path("../../tools/cShapeTools/include/PathFinder").absolute())
        ],
    )
]


# class BuildFailed(Exception):

#     pass


class ExtBuilder(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        # try:
        build_ext.run(self)
        # except (DistutilsPlatformError, FileNotFoundError):
        #     pass

    def build_extension(self, ext):
        # try:
        build_ext.build_extension(self, ext)
        self.inplace = 1
        build_ext.build_extension(self, ext)
        # except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
        #     pass


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {"ext_modules": cythonize(extensions), "cmdclass": {"build_ext": ExtBuilder}}
    )
