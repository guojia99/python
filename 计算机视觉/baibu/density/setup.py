from distutils.core import setup
from Cython.Build import cythonize

"""
    $ python setup.py build_ext
"""
setup(ext_modules=cythonize(["density.py"]))
