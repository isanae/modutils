import sys
import os
import argparse
from .create import CreateMods, CreateDownloads, Overwrite
from .conflict import Conflict
from .tree import Tree
from .devbuild import DevBuild
from .context import Context, Dump
from .log import *

MO_BASE_DIR = os.path.join(os.getenv("LOCALAPPDATA"), "ModOrganizer")
DEFAULT_INSTANCE = "mo-test"
DEFAULT_INSTANCE_DIR = os.path.join(MO_BASE_DIR, DEFAULT_INSTANCE)

def main_parser():
    p = argparse.ArgumentParser(
        description="==> IMPORTANT: all commands below might empty the " +
                    "mods or downloads directories of the given instance " +
                    "(defaults to " + DEFAULT_INSTANCE_DIR + ")")

    p.add_argument(
        "--dry",
        action="store_true",
        help="simulates all filesystem operations")

    p.add_argument(
        "--log",
        type=int,
        default=2,
        help="logs up to the given level: 0=none, 1=error, 2=warn, 3=info, "
             "4=operations, defaults to info")

    p.add_argument(
        "--base-dir",
        type=str,
        default=MO_BASE_DIR,
        help="base data directory, defaults to " + MO_BASE_DIR)

    p.add_argument(
        "--output-dir",
        type=str,
        default=os.getcwd(),
        help="base output dir (contains build, install, etc.), defaults to " +
             "$pwd (currently '" + os.getcwd() + "')")

    p.add_argument(
        "--instance",
        type=str,
        default=DEFAULT_INSTANCE,
        help="name of the instance to use, should be a directory in " +
             "$basedir, defaults to '" + DEFAULT_INSTANCE + "'")

    p.add_argument(
        "--no-ini",
        action="store_true",
        help="does not use ModOrganizer.ini to get paths, will extrapolate " +
             "them from --base-dir and --instance instead; this might end up " +
             "accessing incorrect directories, try with the 'dump' command " +
             "first to make sure everything is ok")

    return p

def create_parser(commands):
    p = main_parser()
    sp = p.add_subparsers(dest="command")

    for c in commands:
        c.create_parser(sp)

    return p

def main():
    commands = [
        CreateMods(),
        CreateDownloads(),
        Overwrite(),
        Conflict(),
        Tree(),
        DevBuild(),
        Dump()]

    p = create_parser(commands)
    opts = p.parse_args()

    sel = None
    for c in commands:
        if opts.command == c.name():
            sel = c
            break

    if sel is None:
        p.print_help()
        return 1

    set_log_level(LogLevels.NONE)
    if opts.log == 1: set_log_level(LogLevels.ERROR)
    if opts.log == 2: set_log_level(LogLevels.WARN)
    if opts.log == 3: set_log_level(LogLevels.INFO)
    if opts.log == 4: set_log_level(LogLevels.OPERATIONS)


    if opts.dry:
        add_log_level(LogLevels.OP)

    cx = Context(opts)
    return sel.run(cx)


if __name__ == "__main__":
    exit(main())
