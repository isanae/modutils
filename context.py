import os
import configparser
from .operations import DryOperations, RealOperations
from .log import *

class Context:
    def __init__(self, opts):
        self.ops_ = None
        self.options = opts
        self.mods_ = None
        self.dl_ = None
        self.overwrite_ = None

        if self.options.dry:
            info("this is a dry run")
            self.ops_ = DryOperations()
        else:
            self.ops_ = RealOperations()

        if not self.options.no_ini:
            self.read_ini()

    def read_ini(self):
        # hack: don't throw for 'dump', let it run and warn the user instead
        if self.options.command == "dump":
            try:
                self.read_ini_impl()
            except:
                pass
        else:
            self.read_ini_impl()

    def read_ini_impl(self):
        cp = configparser.ConfigParser()
        cp.read_file(open(self.settings_ini()))

        self.dl_ = self.read_path(cp, "download_directory")
        self.mods_ = self.read_path(cp, "mod_directory")
        self.overwrite_ = self.read_path(cp, "overwrite_directory")

    def read_path(self, cp, which):
        if which in cp["Settings"]:
            return os.path.normpath(cp["Settings"][which])
        else:
            return None

    def settings_ini(self):
        return os.path.join(self.instance_directory(), "ModOrganizer.ini")

    def instance_directory(self):
        return os.path.join(self.options.base_dir, self.options.instance)

    def mods_directory(self):
        if self.mods_ is not None:
            return self.mods_

        return os.path.join(self.instance_directory(), "mods")

    def downloads_directory(self):
        if self.dl_ is not None:
            return self.dl_

        return os.path.join(self.instance_directory(), "downloads")

    def overwrite_directory(self):
        if self.overwrite_ is not None:
            return self.overwrite_

        return os.path.join(self.instance_directory(), "overwrite")

    def install_directory(self):
        return os.path.join(self.options.output_dir, "install")

    def super_directory(self):
        return os.path.join(
            self.options.output_dir, "build", "modorganizer_super")

    def clear_directory(self, path):
        path = os.path.normpath(path)
        log_op("clearing directory {}", path)
        self.ops_.clear_directory(path)

    def create_directory(self, path):
        path = os.path.normpath(path)
        log_op("creating directory {}", path)
        self.ops_.create_directory(path)

    def write_file(self, path, content):
        path = os.path.normpath(path)
        log_op("writing to {}", path)
        self.ops_.write_file(path, content)

    def archive(self, input, output):
        input = os.path.normpath(input)
        output = os.path.normpath(output)
        log_op("archiving {} into {}", input, output)
        self.ops_.archive(input, output)

    def archive_string(self, path, content):
        log_op("archiving data into archive, archived filename is {}", path)
        return self.ops_.archive_string(path, content)

    def dump(self):
        info("options:")
        info(make_table(vars(self.options).items()))
        info("\npaths:")
        info(make_table(self.make_paths()))

    def make_paths(self):
        return [
            ("instance", self.dump_instance()),
            ("ini", self.dump_ini()),
            ("mods", self.dump_mods()),
            ("downloads", self.dump_downloads()),
            ("overwrite", self.dump_overwrite()),
            ("install", self.dump_install()),
            ("super", self.dump_super())]

    def dump_instance(self):
        return self.dump_path(False, self.instance_directory())

    def dump_ini(self):
        return self.dump_path(False, self.settings_ini())

    def dump_mods(self):
        return self.dump_path(self.mods_ is not None, self.mods_directory())

    def dump_downloads(self):
        return self.dump_path(self.dl_ is not None, self.downloads_directory())

    def dump_overwrite(self):
        return self.dump_path(self.overwrite_ is not None, self.overwrite_directory())

    def dump_install(self):
        p = self.install_directory()
        ok = os.path.exists(os.path.join(p, "bin", "ModOrganizer.exe"))
        return self.dump_path_string(ok, False, p)

    def dump_super(self):
        p = self.super_directory()
        ok = (os.path.exists(os.path.join(p, "check_fnis")) and
              os.path.exists(os.path.join(p, "modorganizer")) and
              os.path.exists(os.path.join(p, "game_skyrim")))

        return self.dump_path_string(ok, False, p)

    def dump_path(self, ini, p):
        return self.dump_path_string(os.path.exists(p), ini, p)

    def dump_path_string(self, ok, ini, p):
        s = ""

        if ok:
            s = "[OK] "
        else:
            s = "[BAD]"

        s += " "

        if ini:
            s += "[INI] "
        else:
            s += "      "

        return p + " " + s


class Dump:
    def name(self):
        return "dump"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="dumps all settings used by this script",
            description="dumps all settings used by this script")

        return p

    def run(self, cx):
        cx.dump()
        return 0
