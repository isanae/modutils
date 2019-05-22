import sys
import os
import argparse
from .create import CreateMods, CreateDownloads
from .conflict import Conflict
from .tree import Tree
from .dev_build import DevBuild
from .context import Context, Dump

MO_BASE_DIR = os.path.join(os.getenv("LOCALAPPDATA"), "ModOrganizer")
DEFAULT_INSTANCE = "mo-test"
DEFAULT_INSTANCE_DIR = os.path.join(MO_BASE_DIR, DEFAULT_INSTANCE)

def main_parser():
    p = argparse.ArgumentParser(
        description="==> IMPORTANT: all mod commands below might empty the " +
                    "mods or downloads directories of the given instance " +
                    "(defaults to " + DEFAULT_INSTANCE_DIR + ")")

    p.add_argument(
        "--dry", action="store_true",
        help="simulates all filesystem operations")

    p.add_argument(
        "--instance",
        type=str,
        default=DEFAULT_INSTANCE,
        help="name of the instance to use, defaults to '" +
             "" + DEFAULT_INSTANCE + "'")

    p.add_argument(
        "--base-dir",
        type=str,
        default=MO_BASE_DIR,
        help="base data directory, defaults to " + MO_BASE_DIR)

    p.add_argument(
        "--install-dir",
        type=str,
        default=os.path.join(os.getcwd(), "install"),
        help="install directory, defaults to $pwd/install (currently " +
             "" + os.path.join(os.getcwd(), "install") + ")")

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

    cx = Context(opts)
    return sel.run(cx)


if __name__ == "__main__":
    exit(main())
