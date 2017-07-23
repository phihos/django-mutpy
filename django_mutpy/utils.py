"""Contains utility functions."""

import importlib
import pkgutil


def list_all_modules_in_package(package_name, include_list, skip):
    """Get a list of all first level modules/packages within a package."""
    package = importlib.import_module(package_name)
    modlist = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        full_modname = package_name + '.' + modname
        if ispkg:
            modlist += list_all_modules_in_package(full_modname, include_list=include_list, skip=skip)
        elif modname not in skip and (not include_list or full_modname in include_list):
            modlist.append(full_modname)
    return modlist
