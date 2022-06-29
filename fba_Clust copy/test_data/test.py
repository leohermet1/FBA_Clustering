import os.path, pkgutil
import tensorly
pkgpath = os.path.dirname(tensorly.__file__)
print([name for _, name, _ in pkgutil.iter_modules([pkgpath])])

tensorly.decomposition()