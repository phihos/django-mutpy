"""Contains utility functions."""

import importlib
import pkgutil


def list_all_modules_in_package(package_name, skip):
    """Get a list of all first level modules/packages within a package."""
    package = importlib.import_module(package_name)
    return [package_name + '.' + modname for importer, modname, ispkg in pkgutil.iter_modules(package.__path__)
            if modname not in skip]
