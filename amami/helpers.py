# Copyright 2022 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0
"""
Script created by Davide Marchegiani (davide.marchegiani@anu.edu.au) at ACCESS-NRI.

Miscellaneous module for different utility functions.
"""

import os
from amami import loggers

# TODO: rename to include verification
def get_abspath(fpath: str, check: bool = True, checkdir: bool = False) -> str:
    """
    Return an absolute path from the provided path and optionally check if path or
    directory exists.
    """
    if checkdir:
        check = False
    abspath = os.path.abspath(fpath)
    if check and not os.path.exists(abspath):
        loggers.LOGGER.error(f"File '{abspath}' does not exist.")
    elif checkdir and not os.path.exists(absdir := os.path.dirname(abspath)):
        loggers.LOGGER.error(f"Directory '{absdir}' does not exist.")
    return abspath


# TODO: refactor naming, does not create a file
def create_unexistent_file(path):
    """
    Create a new file.
    """
    n = 1
    newpath = path
    while os.path.exists(newpath):
        n += 1
        newpath = f"{path}_{n}"
    return newpath
