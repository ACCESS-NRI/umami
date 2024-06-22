# Copyright 2022 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

"""
Module to define the parser for the 'um2nc' command.
"""

import argparse
from typing import List
from amami.helpers import create_unexistent_file
from amami.parsers import ParserWithCallback
from amami.exceptions import ParsingError


DESCRIPTION = """\
Convert UM fieldsfile to netCDF.
For more information about UM fieldsfiles, please refer to \
https://code.metoffice.gov.uk/doc/um/latest/papers/umdp_F03.pdf (MOSRS account needed).

Examples:
`um2nc [-i] INPUT_FILE`
Converts INPUT_FILE to netCDF and saves the output as INPUT_FILE.nc.

`um2nc [-i] INPUT_FILE [-o] OUTPUT_FILE -v`
Converts INPUT_FILE to netCDF and saves the output as OUTPUT_FILE. Verbosity is enabled.

`um2nc [-i] INPUT_FILE [-o] OUTPUT_FILE --format NETCDF3_CLASSIC --simple`
Converts INPUT_FILE to a NETCDF3 CLASSIC netCDF, using "simple" variable names
(in the form "fld_s01i123"), and saves the output as OUTPUT_FILE.
"""


def callback_function(known_args: argparse.Namespace, unknown_args: List[str]) -> argparse.Namespace:
    """
    Preprocessing for `um2nc` parser.
    Does the following tasks:
    -   Checks optional and positional parameters to understand input and output;
    -   Checks if the output path has been provided, otherwise generates it by
        appending '.nc' to the input file.
    """

    # Convert known_args to dict to be able to modify them
    known_args_dict = vars(known_args)
    # Check optional and positional parameters to determine input and output paths.
    if (
        len(unknown_args) > 2
    ) or (
        (None not in [known_args_dict['infile'], known_args_dict['outfile']])
        and
        (len(unknown_args) > 0)
    ) or (
        ((known_args_dict['infile'] is None) ^
         (known_args_dict['outfile'] is None))
        and
        (len(unknown_args) > 1)
    ):
        raise ParsingError("Too many arguments.")
    elif (known_args_dict['infile'] is None) and (len(unknown_args) == 0):
        raise ParsingError("No input file provided.")
    elif known_args_dict['infile'] is None:
        known_args_dict['infile'] = unknown_args[0]
        if known_args_dict['outfile'] is None:
            if len(unknown_args) == 2:
                known_args_dict['outfile'] = unknown_args[1]
            else:
                known_args_dict['outfile'] = create_unexistent_file(
                    f"{known_args_dict['infile']}.nc")
    elif known_args_dict['outfile'] is None:
        if len(unknown_args) == 1:
            known_args_dict['outfile'] = unknown_args[0]
        else:
            known_args_dict['outfile'] = create_unexistent_file(
                f"{known_args_dict['infile']}.nc")
    return argparse.Namespace(**known_args_dict)


# Create parser
PARSER = ParserWithCallback(
    description=DESCRIPTION,
    callback=callback_function,
)
# Add arguments
PARSER.add_argument(
    '-i', '--input',
    dest='infile',
    required=False,
    type=str,
    metavar="INPUT_FILE",
    help="""Path to the UM fieldsfile to be converted.
Note: Can also be inserted as a positional argument.

"""
)
PARSER.add_argument(
    '-o', '--output',
    required=False,
    dest='outfile',
    type=str,
    metavar="OUTPUT_FILE",
    help="""Path for the converted netCDF in output.
If not provided, the output will be generated by appending '.nc' to the input file.
Note: Can also be inserted as a positional argument.

"""
)
PARSER.add_argument(
    '-f', '--format',
    dest='format',
    required=False,
    type=str,
    default='NETCDF4',
    choices=['NETCDF4', 'NETCDF4_CLASSIC', 'NETCDF3_CLASSIC',
             'NETCDF3_64BIT', '1', '2', '3', '4'],
    help="""Specify netCDF format among 1 ('NETCDF4'), 2 ('NETCDF4_CLASSIC'),
3 ('NETCDF3_CLASSIC') or 4 ('NETCDF3_64BIT').
Either numbers or strings are accepted. 
Default: 1 ('NETCDF4').

"""
)
PARSER.add_argument(
    '-c', '--compression',
    dest='compression',
    required=False,
    type=int,
    default=4,
    help="""Compression level (0=none, 9=max). Default 4.

"""
)
PARSER.add_argument(
    '--64bit',
    dest='use64bit',
    action='store_true',
    help="""Use 64 bit netCDF for 64 bit input.

"""
)
PARSER.add_argument(
    '--nohist',
    dest='nohist',
    action='store_true',
    help="""Don't update history attribute.

"""
)
PARSER.add_argument(
    '--simple',
    dest='simple',
    action='store_true',
    help="""Use 'simple' variable names of form 'fld_s01i123'.

"""
)
mutual1 = PARSER.add_mutually_exclusive_group()
mutual1.add_argument(
    '--nomask',
    dest='nomask',
    action='store_true',
    help="""Don't apply heavyside function mask to pressure level fields.
Cannot be used together with --hcrit.

"""
)
mutual1.add_argument(
    '--hcrit',
    dest='hcrit',
    type=float,
    default=0.5,
    help="""Critical value of heavyside function for pressure level masking.
Default: 0.5.
Cannot be used together with --nomask.

"""
)
mutual2 = PARSER.add_mutually_exclusive_group()
mutual2.add_argument(
    '--include',
    dest='include_list',
    type=int,
    metavar=("STASH_CODE1", "STASH_CODE2"),
    nargs='+',
    help="""List of STASH codes to include in the netCDF conversion.
Only the variables with the included STASH codes will be converted.
Cannot be used together with --exclude.

"""
)
mutual2.add_argument(
    '--exclude',
    dest='exclude_list',
    type=int,
    metavar=("STASH_CODE1", "STASH_CODE2"),
    nargs='+',
    help="""List of STASH codes to exclude from the netCDF conversion.
The variables with the excluded STASH codes will not be converted.
Cannot be used together with --include.

"""
)
